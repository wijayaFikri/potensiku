# Generated by Django 3.2.4 on 2021-07-02 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('potensiku', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]