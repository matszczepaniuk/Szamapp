# Generated by Django 4.2.3 on 2023-07-24 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Szamapp', '0009_favouriterecipes_user_statistics_recipes_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Statistics',
        ),
    ]
