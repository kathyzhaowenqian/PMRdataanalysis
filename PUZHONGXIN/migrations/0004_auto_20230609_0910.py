# Generated by Django 3.2 on 2023-06-09 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PUZHONGXIN', '0003_pzxafterchangebranddetail_pzxbeforechangebranddetail_pzxcalculate_pzxchangebrandstatus_pzxchangechan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pzxoverall',
            name='thisyeargpgrowthtotal',
        ),
        migrations.AlterField(
            model_name='pzxnegotiationdetail',
            name='productid',
            field=models.ForeignKey(blank=True, db_column='productid', null=True, on_delete=django.db.models.deletion.CASCADE, to='PUZHONGXIN.pzxmenu', verbose_name='产品信息:名称_规格_单位_采购价_供应商_品牌'),
        ),
        migrations.AlterField(
            model_name='pzxoverall',
            name='whygrowth',
            field=models.CharField(help_text='（增量来源可以多选, 选后请在下方填写明细）', max_length=25, verbose_name='增量来源'),
        ),
    ]
