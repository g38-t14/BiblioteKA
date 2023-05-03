# Generated by Django 4.2 on 2023-05-03 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("copies", "0002_alter_copy_book"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("loans", "0003_alter_loan_loaner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="copy",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="copy_loan",
                to="copies.copy",
            ),
        ),
        migrations.AlterField(
            model_name="loan",
            name="loaner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_copy_loan",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="loan",
            name="return_date",
            field=models.DateTimeField(),
        ),
    ]
