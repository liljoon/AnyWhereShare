from django.db import models
import bcrypt


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

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))