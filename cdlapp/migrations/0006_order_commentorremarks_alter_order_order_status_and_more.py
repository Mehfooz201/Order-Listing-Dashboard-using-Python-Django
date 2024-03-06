# Generated by Django 4.2.3 on 2024-01-26 07:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cdlapp", "0005_remove_order_product_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="commentOrRemarks",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("review", "Review"),
                    ("pending", "Pending"),
                    ("RX-Report", "RX Report"),
                    ("approved", "Approved"),
                    ("completed", "Completed"),
                    ("cancelled", "Cancelled"),
                ],
                default="review",
                max_length=12,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]