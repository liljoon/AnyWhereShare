

class AwAccount(models.Model):
    account_id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    account_type = models.CharField(max_length=20, blank=True, null=True)
    expiration_time = models.DateTimeField(blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    remark = models.CharField(max_length=100, blank=True, null=True)
    valid = models.CharField(max_length=1, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aw_account'


class AwResource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    parent_resource_id = models.IntegerField(blank=True, null=True)
    resource_name = models.CharField(max_length=100, blank=True, null=True)
    resource_type = models.CharField(max_length=30, blank=True, null=True)
    suffix_name = models.CharField(max_length=20, blank=True, null=True)
    path = models.CharField(max_length=300, blank=True, null=True)
    bookmark_type = models.CharField(max_length=20, blank=True, null=True)
    account_id = models.IntegerField(blank=True, null=True)
    valid = models.CharField(max_length=1, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aw_resource'


class AwResourceLog(models.Model):
    resource_id = models.IntegerField(blank=True, null=True)
    modify_type = models.CharField(max_length=100, blank=True, null=True)
    orginal_value = models.CharField(max_length=300, blank=True, null=True)
    new_value = models.CharField(max_length=300, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aw_resource_log'


class AwUrl(models.Model):
    url_id = models.AutoField(primary_key=True)
    resource_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    url_type = models.CharField(max_length=100, blank=True, null=True)
    expiration_time = models.DateTimeField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aw_url'

