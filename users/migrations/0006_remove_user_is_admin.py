# Generated by Django 4.2 on 2023-05-02 18:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_user_role"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_admin",
        ),
    ]
