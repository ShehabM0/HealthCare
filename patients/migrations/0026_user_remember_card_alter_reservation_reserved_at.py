# Generated by Django 5.0.3 on 2024-04-27 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0025_alter_reservation_reserved_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='remember_card',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reserved_at',
            field=models.CharField(default='2024-04-27 20:27:30', max_length=30),
        ),
    ]