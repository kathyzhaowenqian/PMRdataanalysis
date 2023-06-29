# Generated by Django 3.2 on 2023-06-25 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PUZHONGXIN', '0015_pzxnegotiationdetail_skuhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='pzxchangechanneldetail',
            name='productid',
            field=models.ForeignKey(blank=True, db_column='productid', null=True, on_delete=django.db.models.deletion.CASCADE, to='PUZHONGXIN.pzxmenu', verbose_name='产品信息:名称_规格_单位_采购价_供应商_品牌'),
        ),
        migrations.AddField(
            model_name='pzxchangechanneldetail',
            name='skuhistory',
            field=models.JSONField(blank=True, null=True, verbose_name='历史sku'),
        ),
        migrations.AlterField(
            model_name='pzxchangechanneldetail',
            name='costfeepercent',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=25, null=True, verbose_name='原采购价占收费比例'),
        ),
        migrations.AlterField(
            model_name='pzxchangechanneldetail',
            name='gppercent',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=25, null=True, verbose_name='毛利率'),
        ),
        migrations.AlterField(
            model_name='pzxchangechanneldetail',
            name='marketpricefeepercent',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=25, null=True, verbose_name='市场价占收费比例'),
        ),
        migrations.AlterField(
            model_name='pzxchangechanneldetail',
            name='newcostdroprate',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=25, null=True, verbose_name='新采购价下降比例'),
        ),
        migrations.AlterField(
            model_name='pzxchangechanneldetail',
            name='newcostfeepercent',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=25, null=True, verbose_name='新采购价占收费比例'),
        ),
        migrations.AlterField(
            model_name='pzxchangechanneldetail',
            name='newgppercent',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=25, null=True, verbose_name='新毛利率'),
        ),
        migrations.AlterField(
            model_name='pzxchangechanneldetail',
            name='targetdropdate',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=25, null=True, verbose_name='谈判下降比例'),
        ),
        migrations.AlterField(
            model_name='pzxmenu',
            name='theoreticalgppercent',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='理论毛利率'),
        ),
    ]
