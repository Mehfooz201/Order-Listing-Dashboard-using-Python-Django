# Generated by Django 4.2.3 on 2023-07-28 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amruloapp', '0003_order_order_date_alter_order_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_material',
            field=models.CharField(choices=[('OCOR', 'OCOR'), ('OCOR_2', 'OCOR_2')], max_length=50),
        ),
    ]
