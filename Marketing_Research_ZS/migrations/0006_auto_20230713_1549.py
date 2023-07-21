# Generated by Django 3.2 on 2023-07-13 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Marketing_Research_ZS', '0005_auto_20230713_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='gsmrresearchdetail',
            name='machinemodel',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='仪器型号'),
        ),
        migrations.AlterField(
            model_name='gsmrresearchdetail',
            name='testprice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='GSMR卖给代理商的价格', max_digits=25, null=True, verbose_name='代理商价格'),
        ),
    ]