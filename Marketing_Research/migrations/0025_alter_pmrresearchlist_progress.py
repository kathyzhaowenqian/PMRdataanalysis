# Generated by Django 3.2 on 2023-05-08 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Marketing_Research', '0024_pmrresearchlist_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pmrresearchlist',
            name='progress',
            field=models.TextField(blank=True, choices=[('初期了解中', '初期了解中'), ('待拜访', '待拜访'), ('已拜访', '已拜访'), ('招标准备中', '招标准备中'), ('招标完成', '招标完成'), ('审批中', '审批中'), ('已审批', '已审批'), ('审批中', '审批中'), ('仪器已开票', '仪器已开票'), ('仪器&试剂已开票', '仪器&试剂已开票')], help_text='仅选择目标新项目的状态', max_length=255, null=True, verbose_name='状态'),
        ),
    ]