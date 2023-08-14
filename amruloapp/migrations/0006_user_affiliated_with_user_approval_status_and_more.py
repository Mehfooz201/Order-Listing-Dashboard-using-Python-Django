# Generated by Django 4.2.3 on 2023-08-11 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amruloapp', '0005_staffuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='affiliated_with',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='approval_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='StaffUser',
        ),
    ]