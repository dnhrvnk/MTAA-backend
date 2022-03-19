from django.db import models
from rest_framework import serializers
from django.contrib.auth.base_user import AbstractBaseUser
import uuid

class Users(AbstractBaseUser):
    REQUIRED_FIELDS = ('password',)
    USERNAME_FIELD = 'username'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    displayName = models.CharField(max_length=200)
    last_login = None

    @property
    def is_anonymous(self):
        return False

    class Meta:
        managed=False
        db_table = 'users'

