# Generated by Django 3.2.4 on 2021-07-06 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('potensiku', '0002_participant_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]
