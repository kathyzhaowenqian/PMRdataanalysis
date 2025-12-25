"""
数据迁移：将英文活动类型值转换为中文值
"""

from django.db import migrations


def convert_to_chinese(apps, schema_editor):
    """将英文活动类型值转换为中文值"""
    SalesReport = apps.get_model('SALESREPORT', 'SalesReport')

    # 英文值 -> 中文值的映射
    mapping = {
        'customer': '客户活动',
        'internal': '内部工作',
        'stage_advance': '阶段推进',
    }

    # 批量更新
    updated_count = 0
    for old_value, new_value in mapping.items():
        count = SalesReport.objects.filter(type=old_value).update(type=new_value)
        if count > 0:
            print(f'  转换 {old_value} -> {new_value}: {count} 条记录')
            updated_count += count

    print(f'总计更新了 {updated_count} 条销售日报记录')


def convert_to_english(apps, schema_editor):
    """反向迁移：将中文值转换回英文值"""
    SalesReport = apps.get_model('SALESREPORT', 'SalesReport')

    # 中文值 -> 英文值的映射
    reverse_mapping = {
        '客户活动': 'customer',
        '内部工作': 'internal',
        '阶段推进': 'stage_advance',
    }

    updated_count = 0
    for old_value, new_value in reverse_mapping.items():
        count = SalesReport.objects.filter(type=old_value).update(type=new_value)
        if count > 0:
            print(f'  恢复 {old_value} -> {new_value}: {count} 条记录')
            updated_count += count

    print(f'总计恢复了 {updated_count} 条销售日报记录')


class Migration(migrations.Migration):

    dependencies = [
        ('SALESREPORT', '0004_alter_salesreport_type'),
    ]

    operations = [
        migrations.RunPython(
            convert_to_chinese,
            reverse_code=convert_to_english
        ),
    ]
