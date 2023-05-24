# Generated by Django 3.2 on 2023-05-15 05:15

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Marketing_Research', '0030_alter_pmrresearchlist_saleschannel'),
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
            name='SWWSalesmanPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=255, null=True, verbose_name='岗位')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
            ],
            options={
                'verbose_name_plural': '员工职位列表',
                'db_table': 'marketing_research_v2"."SalesmanPosition',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SWWSPDList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier', models.CharField(blank=True, max_length=255, null=True, verbose_name='供应商')),
                ('brand', models.CharField(blank=True, max_length=255, null=True, verbose_name='品牌')),
                ('department', models.CharField(blank=True, max_length=255, null=True, verbose_name='科室')),
                ('product', models.CharField(blank=True, max_length=255, null=True, verbose_name='产品')),
                ('machinemodel', models.CharField(blank=True, max_length=255, null=True, verbose_name='仪器型号')),
                ('listotal', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='LIS收入')),
                ('salestotal', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='年开票额')),
                ('salestotalpercent', models.DecimalField(blank=True, decimal_places=6, max_digits=25, null=True, verbose_name='开票占比')),
                ('purchasetotal', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='年采购额')),
                ('gppercent', models.DecimalField(blank=True, decimal_places=6, max_digits=25, null=True, verbose_name='毛利率')),
                ('relation', models.CharField(blank=True, max_length=255, null=True, verbose_name='关系点')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
            ],
            options={
                'verbose_name_plural': 'SPD战略地图',
                'db_table': 'marketing_research_v2"."SPDList',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SWWUserInfo',
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
    ]