# Generated by Django 5.1.2 on 2024-10-13 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0006_alter_details_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="details",
            name="images",
            field=models.ImageField(
                blank=True, default="default.png", null=True, upload_to="profile-photo/"
            ),
        ),
    ]
