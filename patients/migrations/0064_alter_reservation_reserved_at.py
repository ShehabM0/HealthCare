# Generated by Django 5.0.3 on 2024-06-03 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0063_alter_reservation_reserved_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reserved_at',
            field=models.CharField(default='2024-06-03 10:37:46', max_length=30),
        ),
    ]
