from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Team, TeamMember, TeamTip
from apps.users.serializers import UserBasicSerializer
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TeamMemberSerializer(serializers.ModelSerializer):
    user_details = UserBasicSerializer(source='user', read_only=True)

    class Meta:
        model = TeamMember
        fields = ['id', 'team', 'user', 'user_details', 'role', 'joined_at']
        read_only_fields = ['joined_at', 'team']

class TeamSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True, read_only=True)
    created_by_details = UserBasicSerializer(source='created_by', read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_by', 'created_by_details', 
                 'created_at', 'members']
        read_only_fields = ['created_by', 'created_at']

    def create(self, validated_data):
        logger.debug(f"Creating team with data: {validated_data}")
        try:
            team = super().create(validated_data)
            logger.debug(f"Team created successfully: {team}")
            return team
        except Exception as e:
            logger.error(f"Error in create method: {str(e)}")
            raise

class TeamTipSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    upvote_count = serializers.SerializerMethodField()
    has_upvoted = serializers.SerializerMethodField()

    class Meta:
        model = TeamTip
        fields = ['id', 'content', 'author_name', 'upvote_count', 'has_upvoted', 'created_at']
        read_only_fields = ['author', 'upvotes', 'created_at']

    def get_upvote_count(self, obj):
        return obj.upvotes.count()

    def get_has_upvoted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.upvotes.filter(id=request.user.id).exists()
        return False 

class TeamProgressSerializer(serializers.Serializer):
    total_applications = serializers.IntegerField()
    status_breakdown = serializers.ListField(child=serializers.DictField())
    active_members = serializers.IntegerField()
    interview_rate = serializers.FloatField()
    offer_rate = serializers.FloatField() 