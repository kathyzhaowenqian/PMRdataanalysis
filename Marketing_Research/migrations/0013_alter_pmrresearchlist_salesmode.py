# Generated by Django 3.2 on 2023-03-27 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Marketing_Research', '0012_auto_20230327_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pmrresearchlist',
            name='salesmode',
            field=models.CharField(max_length=25, verbose_name='销售模式'),
        ),
    ]
