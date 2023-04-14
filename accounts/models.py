from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class AccountManager(BaseUserManager):
    def create_user(self, userId, password=None, **kwargs):
        if not userId:
            raise ValueError('Users must have a userId')

        account = self.model(userId=userId, **kwargs)
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, userId, password, **kwargs):
        account = self.create_user(userId, password, **kwargs)
        account.is_staff = True
        account.is_superuser = True
        account.save()

        return account

class Account(AbstractBaseUser, PermissionsMixin):
    accountTypes = [
        ('RE', 'regular'),
        ('GU', 'guest'),
    ]
    userId = models.CharField(max_length=20, primary_key=True, unique=True)
    password = models.CharField(max_length=300)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=30, unique=True)
    url = models.CharField(max_length=100, null=True)
    accountType = models.CharField(max_length=2, choices=accountTypes)
    expirationTime = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = ['email', 'username']

    def __str__(self):
        return self.userId

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
