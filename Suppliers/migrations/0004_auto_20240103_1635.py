# Generated by Django 3.2 on 2024-01-03 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Suppliers', '0003_nq_product_rank_nq_supplier_product_summary_nq_supplier_rank_pzx_product_rank_pzx_supplier_product_s'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pzx_supplier_product_summary',
            options={'managed': False, 'verbose_name_plural': '普中心供应商采购明细'},
        ),
        migrations.AlterModelOptions(
            name='pzx_supplier_rank',
            options={'managed': False, 'verbose_name_plural': '普中心供应商采购排行'},
        ),
    ]