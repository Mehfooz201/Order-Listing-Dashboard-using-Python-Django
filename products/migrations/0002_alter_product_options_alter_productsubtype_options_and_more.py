# Generated by Django 4.2.3 on 2023-12-26 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdlapp', '0005_remove_order_product_type_and_more'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Products Infromation'},
        ),
        migrations.AlterModelOptions(
            name='productsubtype',
            options={'verbose_name': 'All Products', 'verbose_name_plural': 'All Products'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_type',
        ),
        migrations.DeleteModel(
            name='ProductType',
        ),
    ]
