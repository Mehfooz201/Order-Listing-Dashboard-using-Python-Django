# Generated by Django 4.2.3 on 2023-08-30 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amruloapp', '0019_order_num_brackets_order_num_crowns_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(blank=True, choices=[('review', 'Review'), ('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='review', max_length=12, null=True),
        ),
    ]