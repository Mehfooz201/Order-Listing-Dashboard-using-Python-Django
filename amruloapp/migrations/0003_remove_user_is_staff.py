# Generated by Django 4.2.3 on 2023-09-20 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amruloapp', '0002_user_groups_user_is_superuser_user_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]