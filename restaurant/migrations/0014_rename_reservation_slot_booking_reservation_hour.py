# Generated by Django 4.2.5 on 2023-10-01 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0013_remove_booking_table_delete_table"),
    ]

    operations = [
        migrations.RenameField(
            model_name="booking",
            old_name="reservation_slot",
            new_name="reservation_hour",
        ),
    ]
