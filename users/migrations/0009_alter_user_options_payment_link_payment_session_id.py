# Generated by Django 4.2 on 2024-09-25 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_rename_payment_amount_payment_amount_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ["-id"], "verbose_name": "Пользователи"},
        ),
        migrations.AddField(
            model_name="payment",
            name="link",
            field=models.URLField(blank=True, max_length=400, null=True, verbose_name="Ссылка на оплату"),
        ),
        migrations.AddField(
            model_name="payment",
            name="session_id",
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="id сессии"),
        ),
    ]
