# Generated by Django 5.1.3 on 2024-12-04 08:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_manager", "0008_alter_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaign",
            name="mail_content",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="campaign",
            name="mail_subject",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]