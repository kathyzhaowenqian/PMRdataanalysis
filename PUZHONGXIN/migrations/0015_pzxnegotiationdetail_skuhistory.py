# Generated by Django 3.2 on 2023-06-25 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PUZHONGXIN', '0014_auto_20230625_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='pzxnegotiationdetail',
            name='skuhistory',
            field=models.JSONField(blank=True, null=True, verbose_name='历史sku'),
        ),
    ]