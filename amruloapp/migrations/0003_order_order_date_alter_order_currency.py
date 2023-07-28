# Generated by Django 4.2.3 on 2023-07-28 10:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('amruloapp', '0002_alter_order_options_alter_order_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='currency',
            field=models.CharField(choices=[('USA', 'USA'), ('INR', 'INR (Indian Rupees)')], default='USD', max_length=10),
        ),
    ]