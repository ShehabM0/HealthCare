# Generated by Django 5.0.3 on 2024-04-23 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0020_alter_reservation_reserved_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reserved_at',
            field=models.CharField(default='2024-04-23 17:59:37', max_length=30),
        ),
    ]