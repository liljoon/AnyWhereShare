from django.db import models
import account.models as account


class Resource(models.Model):
    resourceTypes = [
        ('F', 'file'),
        ('D', 'folder'),
    ]
    resource_id = models.AutoField(primary_key=True)
    parent_resource_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    resource_name = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=1, choices=resourceTypes)
    suffix_name = models.CharField(max_length=10)
    path = models.TextField()
    is_bookmark = models.IntegerField(default=0)
    is_valid = models.IntegerField(default=0)  # true -> valid, false -> soft delete 상태
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    size = models.IntegerField()
    user_account_id = models.ForeignKey(account.User, on_delete=models.CASCADE)


class Url(models.Model):
    url_id = models.AutoField(primary_key=True)
    resource_id = models.ForeignKey(Resource, on_delete=models.CASCADE)
    url = models.TextField()
    expiration_time = models.DateTimeField()
