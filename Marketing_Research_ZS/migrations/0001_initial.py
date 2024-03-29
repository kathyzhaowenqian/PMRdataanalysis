# Generated by Django 3.2 on 2023-07-12 03:15

import Marketing_Research_ZS.models
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Marketing_Research', '0031_alter_pmrresearchlist_progress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(blank=True, max_length=255, null=True, verbose_name='仪器品牌')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
            ],
            options={
                'verbose_name_plural': '品牌列表',
                'db_table': 'marketing_research_v2"."Brand',
                'managed': False,
            },
        ),
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
            name='GSMRSalesmanPosition',
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
            name='GSMRUserInfo',
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
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(choices=[('黄浦', '黄浦'), ('徐汇', '徐汇'), ('长宁', '长宁'), ('静安', '静安'), ('普陀', '普陀'), ('虹口', '虹口'), ('杨浦', '杨浦'), ('浦东', '浦东'), ('闵行', '闵行'), ('宝山', '宝山'), ('嘉定', '嘉定'), ('金山', '金山'), ('松江', '松江'), ('青浦', '青浦'), ('奉贤', '奉贤'), ('崇明', '崇明')], max_length=255, verbose_name='区域')),
                ('hospitalclass', models.CharField(choices=[('三级', '三级'), ('二级', '二级'), ('一级', '一级'), ('未定级', '未定级')], max_length=255, verbose_name='医院级别')),
                ('hospitalname', models.CharField(max_length=255, verbose_name='医院名称')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
            ],
            options={
                'verbose_name_plural': '医院列表',
                'db_table': 'marketing_research_v2"."Hospital',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(blank=True, max_length=255, null=True, verbose_name='项目名称')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
            ],
            options={
                'verbose_name_plural': '项目列表',
                'db_table': 'marketing_research_v2"."Project',
                'ordering': ['project'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GSMRResearchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director', models.CharField(blank=True, max_length=255, null=True, verbose_name='科室主任')),
                ('saleschannel', models.TextField(blank=True, max_length=255, null=True, verbose_name='销售路径')),
                ('support', models.TextField(blank=True, max_length=500, null=True, verbose_name='所需支持')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('uniquestring', models.CharField(blank=True, max_length=255, null=True, verbose_name='联合唯一值')),
                ('company', models.ForeignKey(db_column='company', default=Marketing_Research_ZS.models.get_compmany_default_value, on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research_ZS.company', verbose_name='公司')),
                ('hospital', models.ForeignKey(db_column='hospital', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research_ZS.hospital', verbose_name='医院')),
                ('operator', models.ForeignKey(db_column='operator', on_delete=django.db.models.deletion.CASCADE, related_name='operatorzs', to='Marketing_Research_ZS.gsmruserinfo', verbose_name='最后操作人')),
                ('project', models.ForeignKey(db_column='project', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research_ZS.project', verbose_name='项目')),
                ('salesman1', models.ForeignKey(db_column='salesman1', on_delete=django.db.models.deletion.CASCADE, related_name='salesman1zs', to='Marketing_Research_ZS.gsmruserinfo', verbose_name='第一负责人')),
                ('salesman2', models.ForeignKey(db_column='salesman2', on_delete=django.db.models.deletion.CASCADE, related_name='salesman2zs', to='Marketing_Research_ZS.gsmruserinfo', verbose_name='第二负责人')),
            ],
            options={
                'verbose_name_plural': '招商调研列表',
                'db_table': 'marketing_research_v2"."GSMRResearchList',
            },
        ),
        migrations.CreateModel(
            name='GSMRSalesTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('2023', '2023'), ('2024', '2024')], default=2023, max_length=25, verbose_name='年份')),
                ('q1target', models.DecimalField(decimal_places=2, default=0, max_digits=25, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Q1目标额/元')),
                ('q2target', models.DecimalField(decimal_places=2, default=0, max_digits=25, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Q2目标额/元')),
                ('q3target', models.DecimalField(decimal_places=2, default=0, max_digits=25, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Q3目标额/元')),
                ('q4target', models.DecimalField(decimal_places=2, default=0, max_digits=25, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Q4目标额/元')),
                ('q1completemonth', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3')], default=3, max_length=25, null=True, verbose_name='Q1目标完成月')),
                ('q2completemonth', models.CharField(blank=True, choices=[('4', '4'), ('5', '5'), ('6', '6')], default=6, max_length=25, null=True, verbose_name='Q2目标完成月')),
                ('q3completemonth', models.CharField(blank=True, choices=[('7', '7'), ('8', '8'), ('9', '9')], default=9, max_length=25, null=True, verbose_name='Q3目标完成月')),
                ('q4completemonth', models.CharField(blank=True, choices=[('10', '10'), ('11', '11'), ('12', '12')], default=12, max_length=25, null=True, verbose_name='Q4目标完成月')),
                ('q1actualsales', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, verbose_name='Q1实际销售额')),
                ('q2actualsales', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, verbose_name='Q2实际销售额')),
                ('q3actualsales', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, verbose_name='Q3实际销售额')),
                ('q4actualsales', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, verbose_name='Q4实际销售额')),
                ('q1finishrate', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='Q1完成率')),
                ('q2finishrate', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='Q2完成率')),
                ('q3finishrate', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='Q3完成率')),
                ('q4finishrate', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='Q4完成率')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('researchlist', models.ForeignKey(db_column='researchlist', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research_ZS.gsmrresearchlist', verbose_name='调研列表')),
            ],
            options={
                'verbose_name_plural': '销售目标及完成率表',
                'db_table': 'marketing_research_v2"."GSMRSalesTarget',
            },
        ),
        migrations.CreateModel(
            name='GSMRResearchDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testspermonth', models.PositiveIntegerField(default=0, verbose_name='月总测试数(人份)')),
                ('testprice', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='单价')),
                ('sumpermonth', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='单价')),
                ('machinenumber', models.PositiveIntegerField(default=0, verbose_name='仪器数量')),
                ('installdate', models.DateField(blank=True, help_text='例: 2023/07/01,如有多台填最老的那台', null=True, verbose_name='装机日期')),
                ('endsupplier', models.CharField(blank=True, max_length=255, null=True, verbose_name='终端商')),
                ('expiration', models.CharField(blank=True, max_length=255, null=True, verbose_name='装机时效')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('brand', models.ForeignKey(db_column='brand', null=True, on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research_ZS.brand', verbose_name='品牌')),
                ('researchlist', models.ForeignKey(db_column='researchlist', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research_ZS.gsmrresearchlist', verbose_name='调研列表')),
            ],
            options={
                'verbose_name_plural': '市场调研详情表',
                'db_table': 'marketing_research_v2"."GSMRResearchDetail',
            },
        ),
        migrations.CreateModel(
            name='GSMRDetailCalculate',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('totalmachinenumber', models.PositiveIntegerField(default=0, verbose_name='仪器总数')),
                ('ownmachinenumber', models.PositiveIntegerField(default=0, verbose_name='我司仪器总数')),
                ('ownmachinepercent', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='我司仪器数占比')),
                ('newold', models.CharField(blank=True, max_length=255, null=True, verbose_name='业务类型')),
                ('totaltestspermonth', models.PositiveIntegerField(default=0, verbose_name='总月测试数')),
                ('owntestspermonth', models.PositiveIntegerField(default=0, verbose_name='我司业务月测试数')),
                ('owntestspercent', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='我司测试数占比')),
                ('brandscombine', models.CharField(blank=True, max_length=255, null=True, verbose_name='品牌集合')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('researchlist', models.OneToOneField(db_column='researchlist', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research_ZS.gsmrresearchlist', verbose_name='调研列表')),
            ],
            options={
                'verbose_name_plural': '项目统计结果表',
                'db_table': 'marketing_research_v2"."GSMRDetailCalculate',
            },
        ),
    ]
