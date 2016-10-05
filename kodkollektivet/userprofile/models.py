from django.db import models
from django.contrib.auth.models import User


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
    return '{}'.format(str(datetime.now().strftime('%Y-%m-%d'))+'-'+instance.first_name+instance.last_name)+'.jpg'


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_type = models.CharField(max_length=200, choices=MEMBER_TYPES, default='Student')
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    valid_to = models.DateField(auto_now=False, auto_now_add=False)
    board_position = models.CharField(max_length=200, choices=BOARD_TYPES, default='None')
    picture = models.ImageField(upload_to=get_upload_file_name, blank=True)
