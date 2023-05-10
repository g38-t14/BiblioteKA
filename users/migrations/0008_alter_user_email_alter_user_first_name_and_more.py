# Generated by Django 4.2.1 on 2023-05-09 13:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_user_block_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=150),
        ),
    ]