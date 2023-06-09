# Generated by Django 3.2 on 2023-03-08 15:19

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
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
            },
        ),
        migrations.CreateModel(
            name='CompetitionRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competitionrelation', models.CharField(blank=True, max_length=255, null=True, verbose_name='竞品关系点')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
            ],
            options={
                'verbose_name_plural': '竞品关系列表',
                'db_table': 'marketing_research_v2"."CompetitionRelation',
            },
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(choices=[('黄浦区', '黄浦区'), ('徐汇区', '徐汇区'), ('长宁区', '长宁区'), ('静安区', '静安区'), ('普陀区', '普陀区'), ('虹口区', '虹口区'), ('杨浦区', '杨浦区'), ('浦东区', '浦东区'), ('闵行区', '闵行区'), ('宝山区', '宝山区'), ('嘉定区', '嘉定区'), ('金山区', '金山区'), ('松江区', '松江区'), ('青浦区', '青浦区'), ('奉贤区', '奉贤区'), ('崇明区', '崇明区')], max_length=255, verbose_name='区域')),
                ('hospitalclass', models.CharField(choices=[('三级', '三级'), ('二级', '二级'), ('一级', '一级'), ('未定级', '未定级')], max_length=255, verbose_name='医院级别')),
                ('hospitalname', models.CharField(max_length=255, verbose_name='医院名称')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
            ],
            options={
                'verbose_name_plural': '医院列表',
                'db_table': 'marketing_research_v2"."Hospital',
            },
        ),
        migrations.CreateModel(
            name='PMRResearchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testspermonth', models.PositiveIntegerField(default=0, verbose_name='月测试数')),
                ('contactname', models.CharField(blank=True, max_length=255, null=True, verbose_name='主任姓名')),
                ('contactmobile', models.CharField(blank=True, max_length=255, null=True, verbose_name='联系方式')),
                ('saleschannel', models.TextField(blank=True, max_length=255, null=True, verbose_name='销售路径')),
                ('support', models.TextField(blank=True, max_length=500, null=True, verbose_name='所需支持')),
                ('adminmemo', models.TextField(blank=True, max_length=500, null=True, verbose_name='备注')),
                ('olddata', models.BooleanField(default=False, max_length=255, verbose_name='原始数据')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('uniquestring', models.CharField(blank=True, max_length=255, null=True, verbose_name='联合唯一值')),
                ('company', models.ForeignKey(db_column='company', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research.company', verbose_name='公司')),
                ('hospital', models.ForeignKey(db_column='hospital', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research.hospital', verbose_name='医院')),
            ],
            options={
                'verbose_name_plural': '市场调研列表',
                'db_table': 'marketing_research_v2"."PMRResearchList',
            },
        ),
        migrations.CreateModel(
            name='ProjectDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailedproject', models.CharField(blank=True, max_length=255, null=True, verbose_name='项目明细')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
            ],
            options={
                'verbose_name_plural': '项目细分列表',
                'db_table': 'marketing_research_v2"."ProjectDetail',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('chinesename', models.CharField(max_length=255, null=True, verbose_name='中文名')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户表',
                'db_table': 'django_admin_v2"."auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SalesTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('2023', '2023'), ('2024', '2024'), ('2025', '2025')], default=2023, max_length=25, verbose_name='年份')),
                ('q1target', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Q1目标额/元')),
                ('q2target', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Q2目标额/元')),
                ('q3target', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Q3目标额/元')),
                ('q4target', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Q4目标额/元')),
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
                ('researchlist', models.ForeignKey(db_column='researchlist', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research.pmrresearchlist', verbose_name='调研列表')),
            ],
            options={
                'verbose_name_plural': '销售目标及完成率表',
                'db_table': 'marketing_research_v2"."SalesTarget',
            },
        ),
        migrations.CreateModel(
            name='SalesmanPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=255, null=True, verbose_name='岗位')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('company', models.ForeignKey(db_column='company', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research.company', verbose_name='公司')),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '员工职位列表',
                'db_table': 'marketing_research_v2"."SalesmanPosition',
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
                ('company', models.ForeignKey(db_column='company', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research.company')),
            ],
            options={
                'verbose_name_plural': '项目列表',
                'db_table': 'marketing_research_v2"."Project',
                'ordering': ['project'],
            },
        ),
        migrations.AddField(
            model_name='pmrresearchlist',
            name='operator',
            field=models.ForeignKey(db_column='operator', on_delete=django.db.models.deletion.CASCADE, related_name='operator', to=settings.AUTH_USER_MODEL, verbose_name='最后操作人'),
        ),
        migrations.AddField(
            model_name='pmrresearchlist',
            name='project',
            field=models.ForeignKey(db_column='project', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research.project', verbose_name='项目'),
        ),
        migrations.AddField(
            model_name='pmrresearchlist',
            name='salesman1',
            field=models.ForeignKey(db_column='salesman1', on_delete=django.db.models.deletion.CASCADE, related_name='salesman1', to=settings.AUTH_USER_MODEL, verbose_name='第一负责人'),
        ),
        migrations.AddField(
            model_name='pmrresearchlist',
            name='salesman2',
            field=models.ForeignKey(db_column='salesman2', on_delete=django.db.models.deletion.CASCADE, related_name='salesman2', to=settings.AUTH_USER_MODEL, verbose_name='第二负责人'),
        ),
        migrations.CreateModel(
            name='PMRResearchDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ownbusiness', models.BooleanField(choices=[(True, '是'), (False, '否')], default=False, verbose_name='是否我司业务')),
                ('machinemodel', models.CharField(blank=True, max_length=255, null=True, verbose_name='仪器型号')),
                ('machineseries', models.CharField(blank=True, max_length=255, null=True, verbose_name='序列号(我司仪器必填)')),
                ('machinenumber', models.PositiveIntegerField(default=0, verbose_name='仪器数量')),
                ('installdate', models.DateField(blank=True, help_text='例: 2023/02/01', null=True, verbose_name='装机日期')),
                ('testprice', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='单价')),
                ('sumpermonth', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, verbose_name='22年我司月均销售额')),
                ('expiration', models.CharField(blank=True, max_length=255, null=True, verbose_name='装机时间')),
                ('endsupplier', models.CharField(blank=True, max_length=255, null=True, verbose_name='终端商(医院收票供应商)')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('brand', models.ForeignKey(db_column='brand', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research.brand', verbose_name='品牌')),
                ('competitionrelation', models.ForeignKey(db_column='competitionrelation', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research.competitionrelation', verbose_name='竞品关系点')),
                ('detailedproject', models.ForeignKey(db_column='detailedproject', help_text='注意:根据本页主项目填报', null=True, on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research.projectdetail', verbose_name='项目细分')),
                ('researchlist', models.ForeignKey(db_column='researchlist', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research.pmrresearchlist', verbose_name='调研列表')),
            ],
            options={
                'verbose_name_plural': '市场调研详情表',
                'db_table': 'marketing_research_v2"."PMRResearchDetail',
            },
        ),
        migrations.CreateModel(
            name='DetailCalculate',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('totalmachinenumber', models.PositiveIntegerField(default=0, verbose_name='仪器总数')),
                ('ownmachinenumber', models.PositiveIntegerField(default=0, verbose_name='我司仪器总数')),
                ('ownmachinepercent', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='我司仪器数占比')),
                ('newold', models.CharField(blank=True, max_length=255, null=True, verbose_name='业务类型')),
                ('totalsumpermonth', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25, null=True, verbose_name='22年我司月均销售额总计')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='是否呈现')),
                ('researchlist', models.OneToOneField(db_column='researchlist', on_delete=django.db.models.deletion.CASCADE, to='Marketing_Research.pmrresearchlist', verbose_name='调研列表')),
            ],
            options={
                'verbose_name_plural': '项目统计结果表',
                'db_table': 'marketing_research_v2"."DetailCalculate',
            },
        ),
    ]
