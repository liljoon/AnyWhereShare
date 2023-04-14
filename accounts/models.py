from django.db import models


class Account(models.Model):
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