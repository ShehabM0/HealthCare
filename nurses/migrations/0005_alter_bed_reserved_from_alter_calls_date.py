# Generated by Django 5.0.3 on 2024-06-10 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nurses', '0004_alter_bed_reserved_from_alter_calls_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bed',
            name='reserved_from',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='calls',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]