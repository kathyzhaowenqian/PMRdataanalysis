# Generated by Django 3.2 on 2023-03-19 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Marketing_Research_JC', '0005_auto_20230319_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jcresearchlist',
            name='brand',
            field=models.ForeignKey(blank=True, db_column='brand', null=True, on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research_JC.brand', verbose_name='品牌'),
        ),
    ]