from django.db import models

# Create your models here.

class GuestUser(models.Model):
	passwd = models.CharField(max_length=10, unique=True)
	create_at = models.DateTimeField(auto_now_add=True)

class FileInfo(models.Model):
	owner = models.ForeignKey(GuestUser, on_delete=models.CASCADE)
	file_name = models.CharField(max_length=20)
	download_url = models.TextField()
