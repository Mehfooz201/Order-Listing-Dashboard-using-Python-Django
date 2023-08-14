# Generated by Django 4.2.3 on 2023-08-10 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amruloapp', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, choices=[('India', 'India'), ('USA', 'USA'), ('Pakistan', 'Pakistan'), ('Bangladesh', 'Bangladesh'), ('Russia', 'Russia'), ('China', 'China')], default='India', max_length=20, null=True),
        ),
    ]