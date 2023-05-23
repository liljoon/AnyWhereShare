# Generated by Django 3.2 on 2023-05-22 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_auto_20230518_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('resource_id', models.AutoField(primary_key=True, serialize=False)),
                ('resource_name', models.CharField(max_length=255)),
                ('resource_type', models.CharField(choices=[('F', 'file'), ('D', 'folder')], max_length=1)),
                ('suffix_name', models.CharField(max_length=10)),
                ('path', models.TextField()),
                ('is_bookmark', models.BooleanField()),
                ('is_valid', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('size', models.IntegerField()),
                ('parent_resource_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='file.resource')),
                ('user_account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user')),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('url_id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.TextField()),
                ('expiration_time', models.DateTimeField()),
                ('resource_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file.resource')),
            ],
        ),
    ]