from rest_framework import serializers
from .models import User
import os

class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user information without related fields"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'title', 'avatar', 'location')
        read_only_fields = ('email',)

class UserProfileSerializer(serializers.ModelSerializer):
    """Full user profile with all fields"""
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'avatar', 'avatar_url', 'tagline', 'bio']
        read_only_fields = ['email']

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
        return None

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user 

class AvatarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar']

    def validate_avatar(self, value):
        if value:
            # Check file size (limit to 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image file too large ( > 5MB )")
            
            # Check file extension
            ext = os.path.splitext(value.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.svg']:
                raise serializers.ValidationError(
                    "Unsupported file format. Please use JPG, PNG or SVG"
                )
        return value