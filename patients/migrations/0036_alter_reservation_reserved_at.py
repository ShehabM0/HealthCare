# Generated by Django 5.0.3 on 2024-04-28 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0035_alter_reservation_reserved_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reserved_at',
            field=models.CharField(default='2024-04-28 17:07:33', max_length=30),
        ),
    ]
