from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Check if username is actually an email
            if '@' in str(username):
                user = UserModel.objects.get(email=username)
            else:
                user = UserModel.objects.get(username=username)
                
            if user.check_password(password):
                return user
                
        except UserModel.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None 