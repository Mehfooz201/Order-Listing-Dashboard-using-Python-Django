# Generated by Django 4.2.3 on 2023-12-25 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdlapp', '0003_remove_user_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_password',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
