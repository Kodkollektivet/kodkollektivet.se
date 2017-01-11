from time import timezone
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlquote


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_straff, is_superuser, **kwargs):
        """Creates and saves a User with the given email and password."""
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set.')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_straff=is_straff,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now, **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        return self._create_user(email, password, False, False, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        return self._create_user(email, password, False, False, **kwargs)


MEMBER_TYPES = (
    ('Student', 'Student'),
    ('Board', 'Board'),
    ('Support', 'Support')
)


BOARD_TYPES = (
    ('None', 'None'),
    ('President', 'President'),
    ('Vice President', 'Vice President'),
    ('Treasurer', 'Treasurer'),
    ('Internal Relations', 'Internal Relations'),
    ('External Relations', 'External Relations'),
)


def get_upload_file_name(instance, filename):
    return '{}'.format(
        str(datetime.now().strftime('%Y-%m-%d')) +
        '-' +
        instance.first_name+instance.last_name)+'.jpg'


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    member_type = models.CharField(max_length=200, choices=MEMBER_TYPES, default='Student')
    email = models.EmailField(blank=False, unique=False)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    valid_to = models.DateField(auto_now=False, auto_now_add=False)
    board_position = models.CharField(max_length=200, choices=BOARD_TYPES, default='None')
    picture = models.ImageField(upload_to=get_upload_file_name, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class META:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/{}/".format(urlquote(self.email))

    def get_full_name(self):
        """Returns the first_name and last_name with spaces."""
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        """Returns a short name."""
        return '{}'.format(self.first_name)

    def email_user(self, subject, message, from_email=None):
        """Send email to user."""
        send_mail(subject, message, from_email, [self.email])









































# from django.db import models
# from django.contrib.auth.models import User






# class Member(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     member_type = models.CharField(max_length=200, choices=MEMBER_TYPES, default='Student')
#     phone = models.CharField(max_length=200)
#     address = models.CharField(max_length=200)
#     valid_to = models.DateField(auto_now=False, auto_now_add=False)
#     board_position = models.CharField(max_length=200, choices=BOARD_TYPES, default='None')
#     picture = models.ImageField(upload_to=get_upload_file_name, blank=True)
