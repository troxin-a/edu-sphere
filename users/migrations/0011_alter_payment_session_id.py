# Generated by Django 4.2 on 2024-09-25 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_alter_payment_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="session_id",
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name="id сессии"),
        ),
    ]
