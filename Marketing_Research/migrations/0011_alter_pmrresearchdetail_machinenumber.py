# Generated by Django 3.2 on 2023-03-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Marketing_Research', '0010_auto_20230324_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pmrresearchdetail',
            name='machinenumber',
            field=models.PositiveIntegerField(default=1, verbose_name='仪器数量'),
        ),
    ]
