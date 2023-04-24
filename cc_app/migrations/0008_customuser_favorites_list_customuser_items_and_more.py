# Generated by Django 4.2 on 2023-04-24 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cc_app', '0007_items_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='favorites_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cc_app.favoriteslist'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='items',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cc_app.items'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='wishlist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cc_app.wishlist'),
        ),
    ]