# Generated by Django 3.2 on 2024-08-13 07:50

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Marketing_Research', '0031_alter_pmrresearchlist_progress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=255, null=True, verbose_name='公司')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
            ],
            options={
                'verbose_name_plural': '公司列表',
                'db_table': 'marketing_research_v2"."Company',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ReportUserInfo',
            fields=[
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户表',
                'db_table': 'django_admin_v2"."auth_user',
                'managed': False,
                'proxy': True,
            },
            bases=('Marketing_Research.userinfo',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SalesReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date1', models.DateField(verbose_name='填报日期')),
                ('project', models.CharField(blank=True, max_length=255, null=True, verbose_name='项目')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='主要人员')),
                ('desc', models.TextField(blank=True, max_length=255, null=True, verbose_name='工作简述')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='工作类型')),
                ('state', models.CharField(blank=True, max_length=255, null=True, verbose_name='最新推进状态')),
                ('stage', models.CharField(blank=True, max_length=255, null=True, verbose_name='已完成阶段')),
                ('date2', models.DateField(blank=True, null=True, verbose_name='上一阶段反馈时间')),
                ('date3', models.DateField(blank=True, null=True, verbose_name='最近计划反馈时间')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('company', models.ForeignKey(db_column='company', on_delete=django.db.models.deletion.CASCADE, to='SALESREPORT.company', verbose_name='公司')),
                ('operator', models.ForeignKey(db_column='operator', on_delete=django.db.models.deletion.CASCADE, related_name='operatorreport', to='SALESREPORT.reportuserinfo', verbose_name='最后操作人')),
                ('salesman', models.ForeignKey(db_column='salesman', on_delete=django.db.models.deletion.CASCADE, related_name='salesmanreport', to='SALESREPORT.reportuserinfo', verbose_name='负责人')),
            ],
            options={
                'verbose_name_plural': '集成业务日报',
                'db_table': 'marketing_research_v2"."JcReport',
            },
        ),
    ]
