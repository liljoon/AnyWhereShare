from django.db import models


class User(models.Model):
    accountTypes = [
        ('RE', 'regular'),
        ('GU', 'guest'),
    ]
    userId = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    accountType = models.CharField(max_length=2, choices=accountTypes, default='RE')
    url = models.URLField(null=True)
    expirationTime = models.IntegerField(null=True)
