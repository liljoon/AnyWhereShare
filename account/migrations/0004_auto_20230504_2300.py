# Generated by Django 3.2 on 2023-05-04 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20230504_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='expirationTime',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
