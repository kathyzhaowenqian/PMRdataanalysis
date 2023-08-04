# Generated by Django 3.2 on 2023-07-31 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ANTING', '0002_auto_20230727_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atmenu',
            name='purchaseqty',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='1-6月销售数量'),
        ),
        migrations.AlterField(
            model_name='atmenu',
            name='purchasesum',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='1-6月销售成本'),
        ),
        migrations.AlterField(
            model_name='atmenu',
            name='theoreticalgp',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='毛利润'),
        ),
        migrations.AlterField(
            model_name='atmenu',
            name='theoreticalgppercent',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='毛利率'),
        ),
        migrations.AlterField(
            model_name='atmenu',
            name='theoreticalvalue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='1-6月销售金额'),
        ),
        migrations.AlterField(
            model_name='atmenuforinline',
            name='purchaseqty',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='1-6月销售数量'),
        ),
        migrations.AlterField(
            model_name='atmenuforinline',
            name='purchasesum',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='1-6月销售成本'),
        ),
        migrations.AlterField(
            model_name='atmenuforinline',
            name='theoreticalgp',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='毛利润'),
        ),
        migrations.AlterField(
            model_name='atmenuforinline',
            name='theoreticalgppercent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='毛利率'),
        ),
        migrations.AlterField(
            model_name='atmenuforinline',
            name='theoreticalvalue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='1-6月销售金额'),
        ),
        migrations.AlterField(
            model_name='atoverall',
            name='department',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='科室'),
        ),
        migrations.AlterField(
            model_name='atoverall',
            name='purchasesum',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='项目1-6月销售成本'),
        ),
        migrations.AlterField(
            model_name='atoverall',
            name='purchasesumpercent',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='该项目占总成本占比'),
        ),
        migrations.AlterField(
            model_name='atoverall',
            name='purchasesumpercentinproject',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='项目中各供应商成本占比'),
        ),
        migrations.AlterField(
            model_name='atoverall',
            name='supplierpurchasesum',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='供应商1-6月销售成本'),
        ),
        migrations.AlterField(
            model_name='atoverall',
            name='suppliertheoreticalgp',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='供应商毛利润'),
        ),
        migrations.AlterField(
            model_name='atoverall',
            name='suppliertheoreticalgppercent',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='供应商毛利率'),
        ),
        migrations.AlterField(
            model_name='atoverall',
            name='suppliertheoreticalvalue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='供应商销售额'),
        ),
        migrations.AlterField(
            model_name='atoverall',
            name='theoreticalgp',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='项目毛利润'),
        ),
        migrations.AlterField(
            model_name='atoverall',
            name='theoreticalgppercent',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=25, verbose_name='项目毛利率'),
        ),
        migrations.AlterField(
            model_name='atoverall',
            name='theoreticalvalue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='项目销售额'),
        ),
    ]
