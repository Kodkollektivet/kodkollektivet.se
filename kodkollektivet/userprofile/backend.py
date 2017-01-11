from models import CustomUser


class CustomUserAuth(object):

    def authenticate(self, username=None, password=None):
        try:
            user = CustomUser.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                return None
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            else:
                return None
        except CustomUser.DoesNotExist:
            return None
