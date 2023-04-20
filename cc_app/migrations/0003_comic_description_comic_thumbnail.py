# Generated by Django 4.2 on 2023-04-20 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc_app', '0002_comic'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='description',
            field=models.CharField(default=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='comic',
            name='thumbnail',
            field=models.URLField(default=True),
        ),
    ]