# Generated by Django 4.2 on 2024-10-01 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0012_alter_payment_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="payment",
            options={"ordering": ["-id"], "verbose_name": "Платежи"},
        ),
    ]
