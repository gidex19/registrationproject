# Generated by Django 2.2.2 on 2019-12-01 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registerapp', '0005_auto_20191128_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='bio',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]