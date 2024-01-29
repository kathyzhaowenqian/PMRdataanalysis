# Generated by Django 3.2 on 2024-01-29 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Suppliers', '0005_anting_product_rank_anting_supplier_product_summary_anting_supplier_rank_nanxiang_product_rank_nanxi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Total_Product_Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.BigIntegerField(verbose_name='排行')),
                ('project', models.CharField(max_length=255, verbose_name='项目')),
                ('productcode', models.CharField(max_length=255, verbose_name='产品编码')),
                ('productname', models.CharField(max_length=255, verbose_name='产品名称')),
                ('spec', models.CharField(max_length=255, verbose_name='规格')),
                ('unit', models.CharField(max_length=255, verbose_name='单位')),
                ('supplier', models.CharField(max_length=255, verbose_name='供应商')),
                ('brand', models.CharField(max_length=255, verbose_name='品牌')),
                ('recentdate', models.DateField(verbose_name='最近发票日期')),
                ('price', models.DecimalField(decimal_places=2, max_digits=25, verbose_name='单价')),
                ('qty21', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='21年数量')),
                ('qty22', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='22年数量')),
                ('qty23', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='23年数量')),
                ('qty24', models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='24年数量')),
                ('totalqty', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='总数量')),
                ('sum21', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='21年采购额')),
                ('sum22', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='22年采购额')),
                ('sum23', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='23年采购额')),
                ('sum24', models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='24年采购额')),
                ('totalsum', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='总采购额')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': '所有项目产品排行',
                'db_table': 'SUPPLIERS"."productrankcombine',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Total_Supplier_Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.SmallIntegerField(verbose_name='排行')),
                ('project', models.CharField(max_length=255, verbose_name='项目')),
                ('supplier', models.CharField(max_length=255, verbose_name='供应商')),
                ('qty21', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='21年数量')),
                ('qty22', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='22年数量')),
                ('qty23', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='23年数量')),
                ('qty24', models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='24年数量')),
                ('totalqty', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='总数量')),
                ('sum21', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='21年采购额')),
                ('sum22', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='22年采购额')),
                ('sum23', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='23年采购额')),
                ('sum24', models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='24年采购额')),
                ('totalsum', models.DecimalField(decimal_places=2, max_digits=25, null=True, verbose_name='总采购额')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': '所有项目供应商采购排行',
                'db_table': 'SUPPLIERS"."supplierrankcombine',
                'managed': False,
            },
        ),
    ]
