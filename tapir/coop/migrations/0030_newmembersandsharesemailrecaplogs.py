# Generated by Django 3.2.15 on 2022-09-04 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coop", "0029_auto_20220617_1056"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewMembersAndSharesEmailRecapLogs",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sent_recap_up_to", models.DateField()),
            ],
        ),
    ]
