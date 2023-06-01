from django.db import models


class User(models.Model):
    account_types = [
        ('RE', 'regular'),
        ('GU', 'guest'),
    ]
    user_id = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    account_type = models.CharField(max_length=2, choices=account_types, default='RE')
    url = models.URLField(null=True)
    expiration_time = models.IntegerField(null=True)
