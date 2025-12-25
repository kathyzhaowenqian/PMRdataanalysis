"""
数据迁移：将旧的活动类型转换为简化的新活动类型
"""

from django.db import migrations


def migrate_activity_types(apps, schema_editor):
    """将旧的详细活动类型映射到新的简化活动类型"""
    SalesReport = apps.get_model('SALESREPORT', 'SalesReport')

    # 旧类型 -> 新类型的映射
    mapping = {
        'customer_visit': 'customer',
        'phone_call': 'customer',
        'tech_demo': 'customer',
        'negotiation': 'customer',
        'proposal_prep': 'internal',
        'internal_coord': 'internal',
        'bid_prep': 'internal',
        'other': 'internal',
        'stage_advance': 'stage_advance',  # 保持不变
    }

    # 批量更新
    updated_count = 0
    for old_type, new_type in mapping.items():
        count = SalesReport.objects.filter(type=old_type).update(type=new_type)
        if count > 0:
            print(f'  转换 {old_type} -> {new_type}: {count} 条记录')
            updated_count += count

    print(f'总计更新了 {updated_count} 条销售日报记录')


def reverse_migrate_activity_types(apps, schema_editor):
    """
    反向迁移：将简化的活动类型恢复为默认的旧类型
    注意：这是有损的，无法完全恢复原始数据
    """
    SalesReport = apps.get_model('SALESREPORT', 'SalesReport')

    # 新类型 -> 默认旧类型的映射
    reverse_mapping = {
        'customer': 'customer_visit',     # 默认恢复为客户拜访
        'internal': 'proposal_prep',      # 默认恢复为方案准备
        'stage_advance': 'stage_advance', # 保持不变
    }

    updated_count = 0
    for new_type, old_type in reverse_mapping.items():
        count = SalesReport.objects.filter(type=new_type).update(type=old_type)
        if count > 0:
            print(f'  恢复 {new_type} -> {old_type}: {count} 条记录')
            updated_count += count

    print(f'总计恢复了 {updated_count} 条销售日报记录（注意：这是有损恢复）')


class Migration(migrations.Migration):

    dependencies = [
        ('SALESREPORT', '0002_project_actual_amount_project_competitor_info_and_more'),
    ]

    operations = [
        migrations.RunPython(
            migrate_activity_types,
            reverse_code=reverse_migrate_activity_types
        ),
    ]
