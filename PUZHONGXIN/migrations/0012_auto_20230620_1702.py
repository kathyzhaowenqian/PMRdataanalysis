# Generated by Django 3.2 on 2023-06-20 09:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PUZHONGXIN', '0011_rename_usagedepartment_pzxoverall_semidepartment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pzxafterchangebranddetail',
            options={'verbose_name_plural': '品牌替换后明细'},
        ),
        migrations.AlterModelOptions(
            name='pzxbeforechangebranddetail',
            options={'verbose_name_plural': '品牌替换前明细'},
        ),
        migrations.AlterModelOptions(
            name='pzxcalculate',
            options={'verbose_name_plural': '作战计划计算表'},
        ),
        migrations.AlterModelOptions(
            name='pzxchangebrandstatus',
            options={'verbose_name_plural': '品牌替换状态'},
        ),
        migrations.AlterModelOptions(
            name='pzxchangechanneldetail',
            options={'verbose_name_plural': '渠道变更明细'},
        ),
        migrations.AlterModelOptions(
            name='pzxchangechannelstatus',
            options={'verbose_name_plural': '渠道变更状态'},
        ),
        migrations.AlterModelOptions(
            name='pzxmenu',
            options={'verbose_name_plural': '普中心大菜单作筛选'},
        ),
        migrations.AlterModelOptions(
            name='pzxmenuforinline',
            options={'verbose_name_plural': '普中心大菜单作展示'},
        ),
        migrations.AlterModelOptions(
            name='pzxnegotiationdetail',
            options={'verbose_name_plural': '供应商重新谈判明细'},
        ),
        migrations.AlterModelOptions(
            name='pzxnegotiationstatus',
            options={'verbose_name_plural': '供应商重新谈判状态'},
        ),
        migrations.AlterModelOptions(
            name='pzxnewprojectdetail',
            options={'verbose_name_plural': '新开项目明细'},
        ),
        migrations.AlterModelOptions(
            name='pzxnewprojectstatus',
            options={'verbose_name_plural': '新开项目状态'},
        ),
        migrations.AlterModelOptions(
            name='pzxoverall',
            options={'verbose_name_plural': '作战计划'},
        ),
        migrations.AlterModelOptions(
            name='pzxsetdetail',
            options={'verbose_name_plural': '套餐绑定明细'},
        ),
        migrations.AlterModelOptions(
            name='pzxsetstatus',
            options={'verbose_name_plural': '套餐绑定状态'},
        ),
        migrations.RemoveField(
            model_name='pzxoverall',
            name='purchasesum',
        ),
        migrations.RemoveField(
            model_name='pzxoverall',
            name='suppliers',
        ),
        migrations.RemoveField(
            model_name='pzxoverall',
            name='theoreticalgp',
        ),
        migrations.RemoveField(
            model_name='pzxoverall',
            name='theoreticalgppercent',
        ),
        migrations.RemoveField(
            model_name='pzxoverall',
            name='theoreticalvalue',
        ),
        migrations.AddField(
            model_name='pzxmenu',
            name='overallid',
            field=models.ForeignKey(db_column='overallid', default=1, on_delete=django.db.models.deletion.CASCADE, to='PUZHONGXIN.pzxoverall', verbose_name='主表id'),
        ),
        migrations.AddField(
            model_name='pzxoverall',
            name='projectvalueid',
            field=models.IntegerField(default=1, unique=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='项目大类id'),
        ),
        migrations.AddField(
            model_name='pzxoverall',
            name='relation',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='关系点'),
        ),
        migrations.AddField(
            model_name='pzxoverall',
            name='supplier',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='供应商'),
        ),
        migrations.AlterField(
            model_name='pzxoverall',
            name='thisyeargpgrowthdetail',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='23年毛利额增量预估'),
        ),
        migrations.CreateModel(
            name='SupplierValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchasesum', models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='采购金额')),
                ('purchasesumpercentinproject', models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='项目中各供应商采购额占比')),
                ('theoreticalvalue', models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='理论销售金额')),
                ('theoreticalgp', models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='理论毛利润')),
                ('theoreticalgppercent', models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='理论毛利率')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('suppliervalueid', models.OneToOneField(db_column='suppliervalueid', on_delete=django.db.models.deletion.CASCADE, to='PUZHONGXIN.pzxoverall', verbose_name='供应商相关金额')),
            ],
            options={
                'verbose_name_plural': '普中心项目大类-供应商金额',
                'db_table': 'marketing_research_v2"."SPDPZXSupplierValue',
            },
        ),
        migrations.CreateModel(
            name='ProjectValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchasesum', models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='采购金额')),
                ('purchasesumpercent', models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='该项目占总采购额占比')),
                ('theoreticalvalue', models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='理论销售金额')),
                ('theoreticalgp', models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='理论毛利润')),
                ('theoreticalgppercent', models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='理论毛利率')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('projectvalueid', models.OneToOneField(db_column='projectvalueid', on_delete=django.db.models.deletion.CASCADE, to='PUZHONGXIN.pzxoverall', to_field='projectvalueid', verbose_name='项目大类相关金额')),
            ],
            options={
                'verbose_name_plural': '普中心项目大类金额',
                'db_table': 'marketing_research_v2"."SPDPZXProjectValue',
            },
        ),
    ]
