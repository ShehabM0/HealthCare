# Generated by Django 5.0.3 on 2024-05-13 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0039_remove_user_remember_card_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reserved_at',
            field=models.CharField(default='2024-05-13 19:31:14', max_length=30),
        ),
    ]