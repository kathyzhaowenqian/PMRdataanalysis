# Generated by Django 3.2 on 2023-03-30 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Marketing_Research_ZS', '0002_auto_20230330_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gsmrresearchdetail',
            old_name='is_goldesite',
            new_name='is_goldsite',
        ),
    ]