# Generated by Django 4.2.3 on 2023-07-30 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amruloapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_timing_prices',
            field=models.JSONField(default={'12HRS': 0.0, '2HRS': 0.0, '6HRS': 0.0}),
        ),
        migrations.AlterField(
            model_name='order',
            name='currency',
            field=models.CharField(choices=[('USA', 'USA ($)'), ('INR', 'INR (Indian Rupees)')], default='USA', max_length=10),
        ),
    ]