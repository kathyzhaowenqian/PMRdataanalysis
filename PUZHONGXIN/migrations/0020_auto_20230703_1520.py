# Generated by Django 3.2 on 2023-07-03 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PUZHONGXIN', '0019_auto_20230627_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pzxnegotiationstatus',
            name='whygrowth',
            field=models.CharField(default='供应商重新谈判', max_length=255, verbose_name='增量来源'),
        ),
        migrations.AlterField(
            model_name='pzxnewprojectstatus',
            name='whygrowth',
            field=models.CharField(default='新开项目', max_length=255, verbose_name='增量来源'),
        ),
        migrations.AlterField(
            model_name='pzxoverall',
            name='supplier',
            field=models.CharField(max_length=255, verbose_name='供应商'),
        ),
    ]
