# Generated by Django 4.2.3 on 2023-08-12 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amruloapp', '0007_companyinformation_frameworkagreement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='agreement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='amruloapp.frameworkagreement'),
        ),
    ]
