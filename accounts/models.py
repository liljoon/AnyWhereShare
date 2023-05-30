from django.db import models
class Account(models.Model):
    userId = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    username = models.CharField(max_length = 20)
    email = models.CharField(max_length = 30)
    createDate = models.DateTimeField(auto_now_add=True)