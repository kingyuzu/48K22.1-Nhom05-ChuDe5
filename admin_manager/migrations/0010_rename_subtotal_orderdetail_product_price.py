# Generated by Django 5.1.3 on 2024-12-05 04:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("admin_manager", "0009_campaign_mail_content_campaign_mail_subject"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderdetail",
            old_name="subtotal",
            new_name="product_price",
        ),
    ]
