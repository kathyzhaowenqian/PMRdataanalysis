# Generated by Django 3.2 on 2023-06-27 13:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PUZHONGXIN', '0018_auto_20230626_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='pzxchangebrandstatus',
            name='statushistory',
            field=models.JSONField(blank=True, null=True, verbose_name='历史status'),
        ),
        migrations.AddField(
            model_name='pzxchangechannelstatus',
            name='statushistory',
            field=models.JSONField(blank=True, null=True, verbose_name='历史status'),
        ),
        migrations.AddField(
            model_name='pzxnegotiationstatus',
            name='statushistory',
            field=models.JSONField(blank=True, null=True, verbose_name='历史status'),
        ),
        migrations.AddField(
            model_name='pzxnewprojectstatus',
            name='statushistory',
            field=models.JSONField(blank=True, null=True, verbose_name='历史status'),
        ),
        migrations.AddField(
            model_name='pzxsetstatus',
            name='statushistory',
            field=models.JSONField(blank=True, null=True, verbose_name='历史status'),
        ),
        migrations.AlterField(
            model_name='pzxafterchangebranddetail',
            name='lissettleprice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='LIS结算价(必填)'),
        ),
        migrations.AlterField(
            model_name='pzxbeforechangebranddetail',
            name='lissettleprice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='LIS结算价(必填)'),
        ),
        migrations.AlterField(
            model_name='pzxchangebrandstatus',
            name='monthgpgrowth',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='月毛利额增量预估/元'),
        ),
        migrations.AlterField(
            model_name='pzxchangechanneldetail',
            name='lissettleprice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='LIS结算价(必填)'),
        ),
        migrations.AlterField(
            model_name='pzxchangechannelstatus',
            name='monthgpgrowth',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='月毛利额增量预估/元'),
        ),
        migrations.AlterField(
            model_name='pzxnegotiationdetail',
            name='lissettleprice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='LIS结算价(必填)'),
        ),
        migrations.AlterField(
            model_name='pzxnegotiationstatus',
            name='monthgpgrowth',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='月毛利额增量预估/元'),
        ),
        migrations.AlterField(
            model_name='pzxnewprojectstatus',
            name='monthgpgrowth',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='月毛利额增量预估/元'),
        ),
        migrations.AlterField(
            model_name='pzxsetdetail',
            name='lissettleprice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='LIS结算价(必填)'),
        ),
        migrations.AlterField(
            model_name='pzxsetstatus',
            name='monthgpgrowth',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='月毛利额增量预估/元'),
        ),
    ]
