# Generated by Django 5.0.3 on 2024-04-21 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification_code', '0017_alter_verificationcode_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='created_at',
            field=models.CharField(default=' 2024-04-21 20:34:33', max_length=30),
        ),
    ]
