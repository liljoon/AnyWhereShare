# Generated by Django 3.2 on 2023-05-18 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='accountType',
            new_name='account_type',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='expirationTime',
            new_name='expiration_time',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='userId',
            new_name='user_id',
        ),
    ]