# Generated by Django 4.2.3 on 2023-07-28 19:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('amruloapp', '0004_alter_order_product_material'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='production',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('Regular', 'Regular order'), ('Simple', 'Simple Order'), ('Urgent', 'Urgent order')], default='Regular', max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='product_material',
            field=models.CharField(choices=[('OCOR', 'OCOR')], max_length=50),
        ),
    ]