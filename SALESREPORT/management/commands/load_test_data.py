"""
销售日报测试数据生成命令（重构版）
为两个不同区域的销售创建完全差异化的测试数据

Salesman 1: 江苏区域 - IVD检验设备
Salesman 48: 浙沪区域 - IVD检验设备

用法:
  python manage.py load_test_data --clean --salesman 1 --company 4
  python manage.py load_test_data --clean --salesman 48 --company 4
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from datetime import date, timedelta
from decimal import Decimal

from SALESREPORT.models import (
    Customer, Project, ProjectStageHistory, SalesReport,
    ReportUserInfo, Company
)


class Command(BaseCommand):
    help = '为SALESREPORT模块生成差异化的测试数据（两个不同区域）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='清理旧的测试数据'
        )
        parser.add_argument(
            '--salesman',
            type=int,
            default=1,
            help='指定销售人员ID（默认为1）'
        )
        parser.add_argument(
            '--company',
            type=int,
            default=4,
            help='指定公司ID（默认为4）'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('开始生成差异化测试数据...'))

        # 获取参数
        salesman_id = options['salesman']
        company_id = options['company']

        # 确认 salesman 和 company 存在
        try:
            salesman = ReportUserInfo.objects.get(id=salesman_id)
            company = Company.objects.get(id=company_id)
        except ReportUserInfo.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'错误：找不到 ID={salesman_id} 的销售人员'))
            return
        except Company.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'错误：找不到 ID={company_id} 的公司'))
            return

        self.stdout.write(f'销售人员: {salesman.chinesename or salesman.username} (ID={salesman_id})')
        self.stdout.write(f'公司: {company.company} (ID={company_id})')

        # 清理旧的测试数据（可选）
        if options['clean']:
            self.cleanup_test_data()

        # 创建测试数据
        self.create_customers(salesman_id)
        self.create_projects(salesman, company)

        self.stdout.write(self.style.SUCCESS('[成功] 测试数据生成完成！'))

    def cleanup_test_data(self):
        """清理所有测试数据（两个区域）"""
        self.stdout.write('清理旧数据中...')

        # 定义需要清理的客户名称列表
        customer_names = [
            # Salesman 1 - 江苏区域
            '南京市第二人民医院',
            '苏州大学附属第一医院',
            '江苏省人民医院',
            '无锡市人民医院',
            '南京鼓楼医院',
            '苏州市立医院',
            # Salesman 48 - 浙沪区域
            '杭州市第一人民医院',
            '浙江大学医学院附属第一医院',
            '上海交通大学医学院附属瑞金医院',
            '宁波市第二医院',
            '温州医科大学附属第一医院',
            '浙江省人民医院',
        ]

        # 查找测试客户
        test_customers = Customer.objects.filter(
            Q(name__contains='测试') | Q(name__in=customer_names)
        )
        customer_count = test_customers.count()

        # 先删除这些客户的所有项目（会级联删除ProjectStageHistory和SalesReport）
        test_projects = Project.objects.filter(customer__in=test_customers)
        project_count = test_projects.count()
        test_projects.delete()

        # 再删除客户
        test_customers.delete()

        self.stdout.write(f'已删除 {project_count} 个测试项目和 {customer_count} 个测试客户及相关数据')

    def create_customers(self, salesman_id):
        """根据 salesman_id 创建对应区域的客户"""
        self.stdout.write(f'创建 Salesman {salesman_id} 的客户数据...')

        if salesman_id == 1:
            # 江苏区域医院
            customers_data = [
                {
                    'name': '南京市第二人民医院',
                    'region': '江苏省南京市',
                    'customer_type': 'hospital',
                    'level': 'A',
                    'contact_person': '王主任',
                    'contact_phone': '138****1001',
                    'address': '南京市鼓楼区钟阜路1号',
                    'remark': '三甲医院，检验科规模大，年采购预算充足'
                },
                {
                    'name': '苏州大学附属第一医院',
                    'region': '江苏省苏州市',
                    'customer_type': 'hospital',
                    'level': 'A',
                    'contact_person': '李主任',
                    'contact_phone': '139****2001',
                    'address': '苏州市姑苏区十梓街188号',
                    'remark': '江苏省重点三甲医院，中心实验室设备先进'
                },
                {
                    'name': '江苏省人民医院',
                    'region': '江苏省南京市',
                    'customer_type': 'hospital',
                    'level': 'A',
                    'contact_person': '陈主任',
                    'contact_phone': '137****3001',
                    'address': '南京市广州路300号',
                    'remark': '省级三甲医院，检验中心实力雄厚'
                },
                {
                    'name': '无锡市人民医院',
                    'region': '江苏省无锡市',
                    'customer_type': 'hospital',
                    'level': 'B',
                    'contact_person': '刘主任',
                    'contact_phone': '136****4001',
                    'address': '无锡市清扬路299号',
                    'remark': '地市级三甲医院，老客户关系良好'
                },
                {
                    'name': '南京鼓楼医院',
                    'region': '江苏省南京市',
                    'customer_type': 'hospital',
                    'level': 'A',
                    'contact_person': '张主任',
                    'contact_phone': '135****5001',
                    'address': '南京市中山路321号',
                    'remark': '综合性三甲医院，设备采购标准高'
                },
                {
                    'name': '苏州市立医院',
                    'region': '江苏省苏州市',
                    'customer_type': 'hospital',
                    'level': 'B',
                    'contact_person': '赵主任',
                    'contact_phone': '134****6001',
                    'address': '苏州市姑苏区道前街26号',
                    'remark': '市属三甲医院，微生物室正在升级改造'
                },
            ]
        elif salesman_id == 48:
            # 浙沪区域医院
            customers_data = [
                {
                    'name': '杭州市第一人民医院',
                    'region': '浙江省杭州市',
                    'customer_type': 'hospital',
                    'level': 'A',
                    'contact_person': '陈主任',
                    'contact_phone': '138****1048',
                    'address': '杭州市上城区浣纱路261号',
                    'remark': '浙江省重点三甲医院，检验科设备更新频繁'
                },
                {
                    'name': '浙江大学医学院附属第一医院',
                    'region': '浙江省杭州市',
                    'customer_type': 'hospital',
                    'level': 'A',
                    'contact_person': '徐主任',
                    'contact_phone': '139****2048',
                    'address': '杭州市上城区庆春路79号',
                    'remark': '大学附属医院，检验中心科研实力强'
                },
                {
                    'name': '上海交通大学医学院附属瑞金医院',
                    'region': '上海市',
                    'customer_type': 'hospital',
                    'level': 'A',
                    'contact_person': '林主任',
                    'contact_phone': '137****3048',
                    'address': '上海市黄浦区瑞金二路197号',
                    'remark': '国内顶级三甲医院，对设备性能要求极高'
                },
                {
                    'name': '宁波市第二医院',
                    'region': '浙江省宁波市',
                    'customer_type': 'hospital',
                    'level': 'B',
                    'contact_person': '张主任',
                    'contact_phone': '136****4048',
                    'address': '宁波市西北街41号',
                    'remark': '市级三甲医院，老客户合作多年'
                },
                {
                    'name': '温州医科大学附属第一医院',
                    'region': '浙江省温州市',
                    'customer_type': 'hospital',
                    'level': 'A',
                    'contact_person': '周主任',
                    'contact_phone': '135****5048',
                    'address': '温州市鹿城区府学巷96号',
                    'remark': '医学院附属医院，预算审批流程严格'
                },
                {
                    'name': '浙江省人民医院',
                    'region': '浙江省杭州市',
                    'customer_type': 'hospital',
                    'level': 'A',
                    'contact_person': '钱主任',
                    'contact_phone': '134****6048',
                    'address': '杭州市上塘路158号',
                    'remark': '省级三甲医院，微生物室正在进行实验室改造'
                },
            ]
        else:
            self.stdout.write(self.style.WARNING(f'未知的 salesman_id: {salesman_id}'))
            return

        for data in customers_data:
            customer, created = Customer.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  [OK] 创建客户: {customer.name}')

    def create_projects(self, salesman, company):
        """根据 salesman.id 路由到不同的项目创建方法"""
        self.stdout.write('创建项目数据...')

        if salesman.id == 1:
            self.create_salesman1_projects(salesman, company)
        elif salesman.id == 48:
            self.create_salesman48_projects(salesman, company)
        else:
            self.stdout.write(self.style.WARNING(f'未知的 salesman.id: {salesman.id}'))

    # ==================== Salesman 1 (江苏区域) 的项目创建方法 ====================

    def create_salesman1_projects(self, salesman, company):
        """创建 Salesman 1 的江苏区域项目"""
        # 获取客户
        customers = {}
        customer_names = [
            '南京市第二人民医院',
            '苏州大学附属第一医院',
            '江苏省人民医院',
            '无锡市人民医院',
            '南京鼓楼医院',
            '苏州市立医院',
        ]

        for name in customer_names:
            try:
                customers[name] = Customer.objects.get(name=name)
            except Customer.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'错误：找不到客户 {name}'))
                return

        # 项目1：血凝分析仪（早期）
        self.create_s1_project1_hemagglutination(customers['南京市第二人民医院'], salesman, company)

        # 项目2：生化分析仪（中期）
        self.create_s1_project2_biochemistry(customers['苏州大学附属第一医院'], salesman, company)

        # 项目3：免疫分析系统（后期）
        self.create_s1_project3_immunity(customers['江苏省人民医院'], salesman, company)

        # 项目4：尿液分析仪（已赢单）
        self.create_s1_project4_urine_won(customers['无锡市人民医院'], salesman, company)

        # 项目5：血细胞分析仪（已输单）
        self.create_s1_project5_blood_lost(customers['南京鼓楼医院'], salesman, company)

        # 项目6：质谱鉴定系统（暂停）
        self.create_s1_project6_mass_suspended(customers['苏州市立医院'], salesman, company)

    def create_s1_project1_hemagglutination(self, customer, salesman, company):
        """Salesman 1 - 项目1: 血凝分析仪采购（早期阶段）"""
        self.stdout.write('\n[S1-P1] 创建项目: 血凝分析仪采购（早期）...')

        today = date.today()
        start_date = today - timedelta(days=20)

        project = Project.objects.create(
            name='CA-7000血凝分析仪采购项目',
            project_code=f'S1-PRJ{today.strftime("%y%m%d")}001',
            customer=customer,
            company=company,
            salesman=salesman,
            current_stage='线索验证/建档',
            status='active',
            win_probability=15,
            estimated_amount=Decimal('250000.00'),
            expected_close_date=today + timedelta(days=75),
            description='检验科凝血组设备更新，现有设备已使用8年，故障率高',
            operator=salesman,
            createtime=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        )
        self.stdout.write(f'  [OK] 项目: {project.name} ({project.project_code})')

        # 阶段历史
        ProjectStageHistory.objects.create(
            project=project,
            from_stage=None,
            to_stage='线索获取',
            change_time=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time())),
            change_reason='检验科主任咨询血凝设备升级方案',
            operator=salesman
        )

        stage_2_date = start_date + timedelta(days=6)
        ProjectStageHistory.objects.create(
            project=project,
            from_stage='线索获取',
            to_stage='线索验证/建档',
            change_time=timezone.make_aware(timezone.datetime.combine(stage_2_date, timezone.datetime.min.time())),
            change_reason='完成初次拜访，确认有真实采购需求，预算约25万',
            operator=salesman
        )

        # 销售日报
        reports = [
            {
                'date': start_date,
                'type': '客户活动',
                'desc': '首次拜访检验科王主任，了解现有Stago血凝仪使用情况。设备已使用8年，年故障次数5-6次，影响日常检测。',
                'state': '【客户活动】阶段保持：线索获取'
            },
            {
                'date': start_date + timedelta(days=3),
                'type': '客户活动',
                'desc': '电话跟进，王主任确认已向院长申请设备更新预算，要求了解CA-7000的技术参数和价格范围。',
                'state': '【客户活动】阶段保持：线索获取'
            },
            {
                'date': stage_2_date,
                'type': '阶段推进',
                'desc': '项目从【线索获取】推进到【线索验证/建档】。完成初次拜访，确认客户有真实采购需求，预算约25万元。',
                'state': '阶段推进：线索获取 → 线索验证/建档，赢单概率提升至15%'
            },
            {
                'date': today - timedelta(days=10),
                'type': '内部工作',
                'desc': '准备CA-7000技术资料和参数对比表，重点突出与Stago的性能差异和性价比优势。',
                'state': '【内部工作】阶段保持：线索验证/建档'
            },
            {
                'date': today - timedelta(days=5),
                'type': '客户活动',
                'desc': '二次拜访，展示CA-7000技术资料，王主任对检测速度（60测试/小时）和试剂开放性表示认可。',
                'state': '【客户活动】阶段保持：线索验证/建档'
            },
            {
                'date': today - timedelta(days=2),
                'type': '客户活动',
                'desc': '电话沟通，了解到竞争对手希森美康也在跟进，客户要求下周提供详细报价方案。',
                'state': '【客户活动】阶段保持：线索验证/建档'
            },
        ]

        for report_data in reports:
            SalesReport.objects.create(
                project=project,
                salesman=salesman,
                company=company,
                date1=report_data['date'],
                type=report_data['type'],
                desc=report_data['desc'],
                state=report_data['state'],
                next_plan_date=report_data['date'] + timedelta(days=3),
                operator=salesman
            )

        self.stdout.write(f'  [OK] 创建了 {len(reports)} 条日报记录')

    def create_s1_project2_biochemistry(self, customer, salesman, company):
        """Salesman 1 - 项目2: 生化分析仪升级（中期阶段）"""
        self.stdout.write('\n[S1-P2] 创建项目: 生化分析仪升级（中期）...')

        today = date.today()
        start_date = today - timedelta(days=50)

        project = Project.objects.create(
            name='BS-2000M生化分析仪升级项目',
            project_code=f'S1-PRJ{today.strftime("%y%m%d")}002',
            customer=customer,
            company=company,
            salesman=salesman,
            current_stage='方案/报价',
            status='active',
            win_probability=40,
            estimated_amount=Decimal('680000.00'),
            expected_close_date=today + timedelta(days=50),
            description='中心实验室生化分析能力不足，计划升级为高通量设备',
            operator=salesman,
            createtime=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        )
        self.stdout.write(f'  [OK] 项目: {project.name} ({project.project_code})')

        # 阶段历史
        stages = [
            {'from': None, 'to': '线索获取', 'date': start_date, 'reason': '中心实验室主任主动咨询生化仪升级方案'},
            {'from': '线索获取', 'to': '线索验证/建档', 'date': start_date + timedelta(days=4), 'reason': '完成初访，确认预算充足'},
            {'from': '线索验证/建档', 'to': '商机立项', 'date': start_date + timedelta(days=12), 'reason': '设备科确认已列入年度采购计划'},
            {'from': '商机立项', 'to': '需求调研', 'date': start_date + timedelta(days=25), 'reason': '组织需求调研会，确定日样本量800+'},
            {'from': '需求调研', 'to': '方案/报价', 'date': start_date + timedelta(days=40), 'reason': '提交完整技术方案和商务报价'},
        ]

        for stage in stages:
            ProjectStageHistory.objects.create(
                project=project,
                from_stage=stage['from'],
                to_stage=stage['to'],
                change_time=timezone.make_aware(timezone.datetime.combine(stage['date'], timezone.datetime.min.time())),
                change_reason=stage['reason'],
                operator=salesman
            )

        # 销售日报
        reports = [
            {'date': start_date, 'type': '客户活动', 'desc': '首次拜访中心实验室李主任，了解现有罗氏c701生化仪使用情况，日样本量约800例，处理能力接近饱和。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=4), 'type': '阶段推进', 'desc': '项目从【线索获取】推进到【线索验证/建档】。完成初访，确认预算充足，客户有明确升级计划。', 'state': '阶段推进：线索获取 → 线索验证/建档，赢单概率提升至10%'},
            {'date': start_date + timedelta(days=8), 'type': '客户活动', 'desc': '电话沟通，李主任确认医院计划在Q2完成采购，预算约70万元，要求了解BS-2000M的处理能力。', 'state': '【客户活动】阶段保持：线索验证/建档'},
            {'date': start_date + timedelta(days=12), 'type': '阶段推进', 'desc': '项目从【线索验证/建档】推进到【商机立项】。设备科张科长确认已列入年度采购计划。', 'state': '阶段推进：线索验证/建档 → 商机立项，赢单概率提升至20%'},
            {'date': start_date + timedelta(days=18), 'type': '客户活动', 'desc': '拜访实验室，现场查看设备使用情况和空间布局，确认BS-2000M安装条件满足。', 'state': '【客户活动】阶段保持：商机立项'},
            {'date': start_date + timedelta(days=25), 'type': '阶段推进', 'desc': '项目从【商机立项】推进到【需求调研】。组织需求调研会，参会人员：李主任、检验科副主任、设备科张科长。', 'state': '阶段推进：商机立项 → 需求调研，赢单概率提升至30%'},
            {'date': start_date + timedelta(days=26), 'type': '客户活动', 'desc': '需求调研会详细讨论：日样本量800+，检测项目80+，需要ISE模块和自动进样系统。', 'state': '【客户活动】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=32), 'type': '内部工作', 'desc': '根据调研结果制定技术方案，选定BS-2000M型号+ISE模块+2个试剂位扩展仓。', 'state': '【内部工作】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=40), 'type': '阶段推进', 'desc': '项目从【需求调研】推进到【方案/报价】。正式提交技术方案和商务报价，总价68万元。', 'state': '阶段推进：需求调研 → 方案/报价，赢单概率提升至40%'},
            {'date': today - timedelta(days=7), 'type': '客户活动', 'desc': '方案讨论会，客户对技术方案认可，但希望优惠幅度能达到8%，我方表示需要内部申请。', 'state': '【客户活动】阶段保持：方案/报价'},
            {'date': today - timedelta(days=3), 'type': '内部工作', 'desc': '内部协调商务部门，获批优惠6%+延长保修期1年的方案。', 'state': '【内部工作】阶段保持：方案/报价'},
            {'date': today, 'type': '客户活动', 'desc': '电话告知客户优惠方案，李主任表示基本接受，需要向院领导汇报后确定，预计下周给答复。', 'state': '【客户活动】阶段保持：方案/报价'},
        ]

        for report_data in reports:
            SalesReport.objects.create(
                project=project,
                salesman=salesman,
                company=company,
                date1=report_data['date'],
                type=report_data['type'],
                desc=report_data['desc'],
                state=report_data['state'],
                next_plan_date=report_data['date'] + timedelta(days=4),
                operator=salesman
            )

        self.stdout.write(f'  [OK] 创建了 {len(reports)} 条日报记录')

    def create_s1_project3_immunity(self, customer, salesman, company):
        """Salesman 1 - 项目3: 化学发光免疫分析系统（后期阶段）"""
        self.stdout.write('\n[S1-P3] 创建项目: 化学发光免疫分析系统（后期）...')

        today = date.today()
        start_date = today - timedelta(days=90)

        project = Project.objects.create(
            name='CL-6000i化学发光免疫分析系统集采项目',
            project_code=f'S1-PRJ{today.strftime("%y%m%d")}003',
            customer=customer,
            company=company,
            salesman=salesman,
            current_stage='招采/挂网/比选',
            status='active',
            win_probability=80,
            estimated_amount=Decimal('1200000.00'),
            expected_close_date=today + timedelta(days=20),
            description='省级医院检验中心免疫分析系统升级，已进入公开招标评审阶段',
            operator=salesman,
            createtime=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        )
        self.stdout.write(f'  [OK] 项目: {project.name} ({project.project_code})')

        # 阶段历史（完整的8个阶段）
        stages = [
            {'from': None, 'to': '线索获取', 'date': start_date, 'reason': '省人民医院院长办公会确定免疫系统升级项目'},
            {'from': '线索获取', 'to': '商机立项', 'date': start_date + timedelta(days=7), 'reason': '列入医院年度重点采购计划'},
            {'from': '商机立项', 'to': '需求调研', 'date': start_date + timedelta(days=18), 'reason': '组织多部门需求调研会'},
            {'from': '需求调研', 'to': '方案/报价', 'date': start_date + timedelta(days=35), 'reason': '提交初步技术方案'},
            {'from': '方案/报价', 'to': '测试/验证', 'date': start_date + timedelta(days=50), 'reason': '客户现场测试样本，验证设备性能'},
            {'from': '测试/验证', 'to': '准入/关键人认可', 'date': start_date + timedelta(days=62), 'reason': '检验中心主任和分管副院长认可方案'},
            {'from': '准入/关键人认可', 'to': '商务谈判', 'date': start_date + timedelta(days=70), 'reason': '进入价格谈判，商定最终价格120万'},
            {'from': '商务谈判', 'to': '招采/挂网/比选', 'date': start_date + timedelta(days=80), 'reason': '进入公开招标流程，已提交投标文件'},
        ]

        for stage in stages:
            ProjectStageHistory.objects.create(
                project=project,
                from_stage=stage['from'],
                to_stage=stage['to'],
                change_time=timezone.make_aware(timezone.datetime.combine(stage['date'], timezone.datetime.min.time())),
                change_reason=stage['reason'],
                operator=salesman
            )

        # 销售日报（覆盖90天周期）
        reports = [
            {'date': start_date, 'type': '客户活动', 'desc': '首次拜访检验中心陈主任，了解到医院计划升级化学发光免疫分析系统，现有设备日样本量300+，需要提升到500+。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=3), 'type': '客户活动', 'desc': '电话跟进，确认项目已在院长办公会通过，预算充足，时间表为Q1完成招标。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=7), 'type': '阶段推进', 'desc': '项目从【线索获取】推进到【商机立项】。医院正式将免疫系统升级列入年度重点采购计划。', 'state': '阶段推进：线索获取 → 商机立项，赢单概率提升至25%'},
            {'date': start_date + timedelta(days=12), 'type': '客户活动', 'desc': '拜访检验中心和设备科，了解现有罗氏e411使用情况，设备已使用7年，需要更换。', 'state': '【客户活动】阶段保持：商机立项'},
            {'date': start_date + timedelta(days=18), 'type': '阶段推进', 'desc': '项目从【商机立项】推进到【需求调研】。组织多部门需求调研会，参会人员：检验中心主任、免疫室主任、设备科、财务科。', 'state': '阶段推进：商机立项 → 需求调研，赢单概率提升至35%'},
            {'date': start_date + timedelta(days=20), 'type': '客户活动', 'desc': '需求调研深入讨论，客户要求检测项目100+，通量500测试/小时，配备自动装载系统和冷藏模块。', 'state': '【客户活动】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=28), 'type': '内部工作', 'desc': '根据需求调研结果，制定技术方案，选定CL-6000i型号，配置全自动装载系统和试剂冷藏模块。', 'state': '【内部工作】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=35), 'type': '阶段推进', 'desc': '项目从【需求调研】推进到【方案/报价】。正式提交初步技术方案和商务报价，预算120万元。', 'state': '阶段推进：需求调研 → 方案/报价，赢单概率提升至45%'},
            {'date': start_date + timedelta(days=42), 'type': '客户活动', 'desc': '方案讨论会，检验中心对技术方案表示认可，要求补充试剂成本分析和售后服务方案。', 'state': '【客户活动】阶段保持：方案/报价'},
            {'date': start_date + timedelta(days=50), 'type': '阶段推进', 'desc': '项目从【方案/报价】推进到【测试/验证】。客户现场测试样本，验证设备性能指标。', 'state': '阶段推进：方案/报价 → 测试/验证，赢单概率提升至60%'},
            {'date': start_date + timedelta(days=53), 'type': '客户活动', 'desc': '现场测试验证，运行150例临床样本，结果与参考方法相关性达0.99，客户非常满意。', 'state': '【客户活动】阶段保持：测试/验证'},
            {'date': start_date + timedelta(days=62), 'type': '阶段推进', 'desc': '项目从【测试/验证】推进到【准入/关键人认可】。检验中心主任和分管副院长正式认可技术方案。', 'state': '阶段推进：测试/验证 → 准入/关键人认可，赢单概率提升至70%'},
            {'date': start_date + timedelta(days=70), 'type': '阶段推进', 'desc': '项目从【准入/关键人认可】推进到【商务谈判】。进入价格谈判阶段，商定最终价格120万元。', 'state': '阶段推进：准入/关键人认可 → 商务谈判，赢单概率提升至75%'},
            {'date': start_date + timedelta(days=73), 'type': '客户活动', 'desc': '价格谈判，客户要求优惠5%，我方同意并承诺提供3年延保服务和试剂优惠套餐。', 'state': '【客户活动】阶段保持：商务谈判'},
            {'date': start_date + timedelta(days=80), 'type': '阶段推进', 'desc': '项目从【商务谈判】推进到【招采/挂网/比选】。医院启动公开招标流程，已提交投标文件。', 'state': '阶段推进：商务谈判 → 招采/挂网/比选，赢单概率提升至80%'},
            {'date': start_date + timedelta(days=81), 'type': '内部工作', 'desc': '准备投标文件，包括技术标书、商务标书、资质证明材料，确保所有文件符合招标要求。', 'state': '【内部工作】阶段保持：招采/挂网/比选'},
            {'date': today - timedelta(days=6), 'type': '客户活动', 'desc': '拜访评审专家，介绍CL-6000i技术优势，重点说明与竞品贝克曼DXi800的差异化功能。', 'state': '【客户活动】阶段保持：招采/挂网/比选'},
            {'date': today - timedelta(days=2), 'type': '客户活动', 'desc': '电话确认开标时间和地点，检验中心主任透露我们的技术评分和商务评分都较高。', 'state': '【客户活动】阶段保持：招采/挂网/比选'},
        ]

        for report_data in reports:
            SalesReport.objects.create(
                project=project,
                salesman=salesman,
                company=company,
                date1=report_data['date'],
                type=report_data['type'],
                desc=report_data['desc'],
                state=report_data['state'],
                next_plan_date=report_data['date'] + timedelta(days=3),
                operator=salesman
            )

        self.stdout.write(f'  [OK] 创建了 {len(reports)} 条日报记录')

    def create_s1_project4_urine_won(self, customer, salesman, company):
        """Salesman 1 - 项目4: 尿液分析仪流水线（已赢单）"""
        self.stdout.write('\n[S1-P4] 创建项目: 尿液分析仪流水线（已赢单）...')

        today = date.today()
        start_date = today - timedelta(days=75)
        win_date = today - timedelta(days=7)

        project = Project.objects.create(
            name='UA-5800尿液分析仪流水线更新项目',
            project_code=f'S1-PRJ{today.strftime("%y%m%d")}004',
            customer=customer,
            company=company,
            salesman=salesman,
            current_stage='收单',
            status='won',
            win_probability=100,
            estimated_amount=Decimal('200000.00'),
            actual_amount=Decimal('185000.00'),
            expected_close_date=win_date,
            actual_close_date=win_date,
            description='检验科尿液组流水线配置更新，老客户复购项目，已成功签约',
            operator=salesman,
            createtime=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        )
        self.stdout.write(f'  [OK] 项目: {project.name} ({project.project_code})')

        # 阶段历史（完整流程到收单）
        stages = [
            {'from': None, 'to': '线索获取', 'date': start_date, 'reason': '老客户刘主任咨询尿液分析仪更新'},
            {'from': '线索获取', 'to': '商机立项', 'date': start_date + timedelta(days=5), 'reason': '确认预算到位，老客户关系良好'},
            {'from': '商机立项', 'to': '方案/报价', 'date': start_date + timedelta(days=15), 'reason': '快速提供流水线配置方案'},
            {'from': '方案/报价', 'to': '商务谈判', 'date': start_date + timedelta(days=35), 'reason': '价格谈判，老客户优惠7.5%'},
            {'from': '商务谈判', 'to': '中标/赢单', 'date': start_date + timedelta(days=55), 'reason': '客户确认采购，签订合同'},
            {'from': '中标/赢单', 'to': '装机/验收', 'date': start_date + timedelta(days=65), 'reason': '设备到货安装，完成培训'},
            {'from': '装机/验收', 'to': '收单', 'date': win_date, 'reason': '项目赢单，成交金额：185000.00元。客户验收合格，款项已到账'},
        ]

        for stage in stages:
            ProjectStageHistory.objects.create(
                project=project,
                from_stage=stage['from'],
                to_stage=stage['to'],
                change_time=timezone.make_aware(timezone.datetime.combine(stage['date'], timezone.datetime.min.time())),
                change_reason=stage['reason'],
                operator=salesman
            )

        # 销售日报
        reports = [
            {'date': start_date, 'type': '客户活动', 'desc': '老客户刘主任电话咨询尿液分析仪流水线配置更新，现有爱威设备已使用6年，希望升级为流水线配置。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=2), 'type': '客户活动', 'desc': '拜访刘主任，了解详细需求：日样本量200+，需要UA+UF流水线配置，预算约20万。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=5), 'type': '阶段推进', 'desc': '项目从【线索获取】推进到【商机立项】。老客户确认预算到位，项目正式立项。', 'state': '阶段推进：线索获取 → 商机立项，赢单概率提升至40%'},
            {'date': start_date + timedelta(days=10), 'type': '客户活动', 'desc': '现场查看安装空间，确认UA-5800流水线配置可以满足需求，刘主任对我们的售后服务很满意。', 'state': '【客户活动】阶段保持：商机立项'},
            {'date': start_date + timedelta(days=15), 'type': '阶段推进', 'desc': '项目从【商机立项】推进到【方案/报价】。快速提供流水线配置技术方案和报价，总价20万元。', 'state': '阶段推进：商机立项 → 方案/报价，赢单概率提升至60%'},
            {'date': start_date + timedelta(days=22), 'type': '客户活动', 'desc': '方案讨论，客户对技术方案满意，但希望价格能有老客户优惠。', 'state': '【客户活动】阶段保持：方案/报价'},
            {'date': start_date + timedelta(days=35), 'type': '阶段推进', 'desc': '项目从【方案/报价】推进到【商务谈判】。老客户优惠7.5%，最终价格18.5万元。', 'state': '阶段推进：方案/报价 → 商务谈判，赢单概率提升至75%'},
            {'date': start_date + timedelta(days=40), 'type': '客户活动', 'desc': '价格谈判，我方同意老客户优惠7.5%，并承诺提供2年延保服务，刘主任非常满意。', 'state': '【客户活动】阶段保持：商务谈判'},
            {'date': start_date + timedelta(days=50), 'type': '内部工作', 'desc': '内部协调，准备合同和发货事宜，确认交货期为10天。', 'state': '【内部工作】阶段保持：商务谈判'},
            {'date': start_date + timedelta(days=55), 'type': '阶段推进', 'desc': '项目从【商务谈判】推进到【中标/赢单】。客户正式签订采购合同，金额18.5万元。', 'state': '阶段推进：商务谈判 → 中标/赢单，赢单概率提升至95%'},
            {'date': start_date + timedelta(days=62), 'type': '客户活动', 'desc': '设备到货，协调安装调试工作，培训检验科操作人员，刘主任对设备性能很满意。', 'state': '【客户活动】阶段保持：中标/赢单'},
            {'date': start_date + timedelta(days=65), 'type': '阶段推进', 'desc': '项目从【中标/赢单】推进到【装机/验收】。设备已送达医院并完成安装调试和人员培训。', 'state': '阶段推进：中标/赢单 → 装机/验收，赢单概率提升至98%'},
            {'date': win_date, 'type': '阶段推进', 'desc': '项目赢单！实际成交金额：185000.00元。客户验收合格，对设备性能和售后服务非常满意，款项已全额到账。老客户关系维护良好。', 'state': '✅ 项目赢单！成交金额：¥185,000.00元'},
        ]

        for report_data in reports:
            SalesReport.objects.create(
                project=project,
                salesman=salesman,
                company=company,
                date1=report_data['date'],
                type=report_data['type'],
                desc=report_data['desc'],
                state=report_data['state'],
                operator=salesman
            )

        self.stdout.write(f'  [OK] 创建了 {len(reports)} 条日报记录')

    def create_s1_project5_blood_lost(self, customer, salesman, company):
        """Salesman 1 - 项目5: 血细胞分析仪更新（已输单）"""
        self.stdout.write('\n[S1-P5] 创建项目: 血细胞分析仪更新（已输单）...')

        today = date.today()
        start_date = today - timedelta(days=65)
        lost_date = today - timedelta(days=10)

        project = Project.objects.create(
            name='BC-6800血细胞分析仪更新项目',
            project_code=f'S1-PRJ{today.strftime("%y%m%d")}005',
            customer=customer,
            company=company,
            salesman=salesman,
            current_stage='测试/验证',
            status='lost',
            win_probability=60,
            estimated_amount=Decimal('350000.00'),
            lost_reason='product_mismatch',
            lost_stage='测试/验证',
            competitor_info='希森美康XN-9000',
            lost_detail='客户在测试验证阶段发现BC-6800的检测速度（100测试/小时）低于希森美康XN-9000（150测试/小时），医院日样本量大，对处理速度要求高，最终选择了竞品。',
            description='检验科血液室设备更新，因产品性能不符输给竞争对手',
            operator=salesman,
            createtime=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        )
        self.stdout.write(f'  [OK] 项目: {project.name} ({project.project_code})')

        # 阶段历史
        stages = [
            {'from': None, 'to': '线索获取', 'date': start_date, 'reason': '检验科血液室主任咨询血细胞分析仪更新'},
            {'from': '线索获取', 'to': '商机立项', 'date': start_date + timedelta(days=8), 'reason': '确认有采购计划和预算'},
            {'from': '商机立项', 'to': '需求调研', 'date': start_date + timedelta(days=18), 'reason': '完成需求沟通，日样本量1000+'},
            {'from': '需求调研', 'to': '方案/报价', 'date': start_date + timedelta(days=30), 'reason': '提交BC-6800技术方案'},
            {'from': '方案/报价', 'to': '测试/验证', 'date': start_date + timedelta(days=45), 'reason': '客户要求现场测试验证设备性能'},
        ]

        for stage in stages:
            ProjectStageHistory.objects.create(
                project=project,
                from_stage=stage['from'],
                to_stage=stage['to'],
                change_time=timezone.make_aware(timezone.datetime.combine(stage['date'], timezone.datetime.min.time())),
                change_reason=stage['reason'],
                operator=salesman
            )

        # 销售日报
        reports = [
            {'date': start_date, 'type': '客户活动', 'desc': '首次拜访检验科张主任，了解血液室现有迈瑞BC-5390设备使用情况，日样本量约1000例，设备处理能力接近极限。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=4), 'type': '客户活动', 'desc': '电话沟通，张主任确认医院计划更新血细胞分析仪，预算约35万，要求了解BC-6800的性能参数。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=8), 'type': '阶段推进', 'desc': '项目从【线索获取】推进到【商机立项】。确认客户有采购计划和预算，项目正式立项。', 'state': '阶段推进：线索获取 → 商机立项，赢单概率提升至20%'},
            {'date': start_date + timedelta(days=12), 'type': '客户活动', 'desc': '二次拜访，详细了解需求，客户要求设备处理速度快、检测参数全面，日样本量1000+。', 'state': '【客户活动】阶段保持：商机立项'},
            {'date': start_date + timedelta(days=18), 'type': '阶段推进', 'desc': '项目从【商机立项】推进到【需求调研】。完成需求调研，客户重点关注检测速度和参数准确性。', 'state': '阶段推进：商机立项 → 需求调研，赢单概率提升至35%'},
            {'date': start_date + timedelta(days=25), 'type': '内部工作', 'desc': '准备BC-6800技术方案，强调26项检测参数+5分类+网织红细胞分析。', 'state': '【内部工作】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=30), 'type': '阶段推进', 'desc': '项目从【需求调研】推进到【方案/报价】。提交BC-6800技术方案和报价，总价35万元。', 'state': '阶段推进：需求调研 → 方案/报价，赢单概率提升至50%'},
            {'date': start_date + timedelta(days=38), 'type': '客户活动', 'desc': '方案讨论，客户对检测参数满意，但提出需要验证检测速度是否能满足日常需求，竞争对手希森美康也在跟进。', 'state': '【客户活动】阶段保持：方案/报价'},
            {'date': start_date + timedelta(days=45), 'type': '阶段推进', 'desc': '项目从【方案/报价】推进到【测试/验证】。客户要求现场测试验证设备性能，特别是处理速度。', 'state': '阶段推进：方案/报价 → 测试/验证，赢单概率提升至60%'},
            {'date': start_date + timedelta(days=48), 'type': '客户活动', 'desc': '现场测试，运行200例样本，BC-6800检测速度约100测试/小时，客户表示希望能更快一些。', 'state': '【客户活动】阶段保持：测试/验证'},
            {'date': start_date + timedelta(days=52), 'type': '客户活动', 'desc': '电话跟进，了解到希森美康XN-9000的测试速度为150测试/小时，客户倾向于选择更快的设备。', 'state': '【客户活动】阶段保持：测试/验证'},
            {'date': lost_date, 'type': '内部工作', 'desc': '项目输单。流失原因：产品性能不符合需求。流失阶段：测试/验证。详细说明：客户在测试阶段发现BC-6800的检测速度（100测试/小时）低于希森美康XN-9000（150测试/小时），医院日样本量大对处理速度要求高，最终选择了竞品。', 'state': '❌ 项目输单 - 流失原因：产品性能不符，流失阶段：测试/验证'},
        ]

        for report_data in reports:
            SalesReport.objects.create(
                project=project,
                salesman=salesman,
                company=company,
                date1=report_data['date'],
                type=report_data['type'],
                desc=report_data['desc'],
                state=report_data['state'],
                operator=salesman
            )

        self.stdout.write(f'  [OK] 创建了 {len(reports)} 条日报记录')

    def create_s1_project6_mass_suspended(self, customer, salesman, company):
        """Salesman 1 - 项目6: 微生物质谱鉴定系统（暂停）"""
        self.stdout.write('\n[S1-P6] 创建项目: 微生物质谱鉴定系统（暂停）...')

        today = date.today()
        start_date = today - timedelta(days=100)
        suspend_date = today - timedelta(days=20)

        project = Project.objects.create(
            name='MALDI-TOF MS微生物质谱鉴定系统采购项目',
            project_code=f'S1-PRJ{today.strftime("%y%m%d")}006',
            customer=customer,
            company=company,
            salesman=salesman,
            current_stage='需求调研',
            status='suspended',
            win_probability=25,
            estimated_amount=Decimal('850000.00'),
            expected_close_date=today + timedelta(days=180),
            suspend_reason='医院信息系统升级中，质谱系统需要与LIS系统对接，需等待信息化改造完成（预计6个月）',
            expected_resume_date=today + timedelta(days=180),
            description='微生物室质谱鉴定系统升级，因信息系统升级暂停跟进',
            operator=salesman,
            createtime=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        )
        self.stdout.write(f'  [OK] 项目: {project.name} ({project.project_code})')

        # 阶段历史
        stages = [
            {'from': None, 'to': '线索获取', 'date': start_date, 'reason': '微生物室主任咨询质谱鉴定系统'},
            {'from': '线索获取', 'to': '线索验证/建档', 'date': start_date + timedelta(days=12), 'reason': '确认有升级需求和预算意向'},
            {'from': '线索验证/建档', 'to': '商机立项', 'date': start_date + timedelta(days=28), 'reason': '项目列入采购计划'},
            {'from': '商机立项', 'to': '需求调研', 'date': start_date + timedelta(days=50), 'reason': '开始详细需求调研'},
        ]

        for stage in stages:
            ProjectStageHistory.objects.create(
                project=project,
                from_stage=stage['from'],
                to_stage=stage['to'],
                change_time=timezone.make_aware(timezone.datetime.combine(stage['date'], timezone.datetime.min.time())),
                change_reason=stage['reason'],
                operator=salesman
            )

        # 销售日报
        reports = [
            {'date': start_date, 'type': '客户活动', 'desc': '首次拜访微生物室赵主任，了解到医院计划引进质谱鉴定系统，现有生化鉴定方法效率低、周期长。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=6), 'type': '客户活动', 'desc': '电话沟通，赵主任确认有明确的采购计划，预算约85万元，时间表为下半年。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=12), 'type': '阶段推进', 'desc': '项目从【线索获取】推进到【线索验证/建档】。确认客户有真实升级需求和预算意向。', 'state': '阶段推进：线索获取 → 线索验证/建档，赢单概率提升至10%'},
            {'date': start_date + timedelta(days=20), 'type': '客户活动', 'desc': '拜访微生物室，了解现有鉴定方法和工作流程，日鉴定样本约30例，周期3-5天。', 'state': '【客户活动】阶段保持：线索验证/建档'},
            {'date': start_date + timedelta(days=28), 'type': '阶段推进', 'desc': '项目从【线索验证/建档】推进到【商机立项】。项目已列入医院年度采购计划。', 'state': '阶段推进：线索验证/建档 → 商机立项，赢单概率提升至20%'},
            {'date': start_date + timedelta(days=38), 'type': '客户活动', 'desc': '需求沟通会，参会人员：微生物室主任、检验科主任、信息科长，讨论质谱系统与LIS对接需求。', 'state': '【客户活动】阶段保持：商机立项'},
            {'date': start_date + timedelta(days=50), 'type': '阶段推进', 'desc': '项目从【商机立项】推进到【需求调研】。开始详细需求调研，客户要求质谱系统能与LIS无缝对接。', 'state': '阶段推进：商机立项 → 需求调研，赢单概率提升至25%'},
            {'date': start_date + timedelta(days=55), 'type': '客户活动', 'desc': '需求调研会，详细讨论鉴定数据库要求、报告格式、LIS对接方案。', 'state': '【客户活动】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=65), 'type': '内部工作', 'desc': '根据需求调研准备技术方案，选定MALDI-TOF MS型号，配置完整数据库。', 'state': '【内部工作】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=75), 'type': '客户活动', 'desc': '电话跟进，信息科告知医院正在进行LIS系统升级，质谱系统对接需要等待信息化改造完成。', 'state': '【客户活动】阶段保持：需求调研'},
            {'date': suspend_date, 'type': '内部工作', 'desc': '项目状态变更为【暂停跟进】。暂停原因：医院信息系统升级中，质谱系统需要与新LIS系统对接，需等待信息化改造完成（预计6个月）。', 'state': '⏸️ 项目暂停跟进 - 等待信息系统升级'},
        ]

        for report_data in reports:
            SalesReport.objects.create(
                project=project,
                salesman=salesman,
                company=company,
                date1=report_data['date'],
                type=report_data['type'],
                desc=report_data['desc'],
                state=report_data['state'],
                operator=salesman
            )

        self.stdout.write(f'  [OK] 创建了 {len(reports)} 条日报记录')

    # ==================== Salesman 48 (浙沪区域) 的项目创建方法 ====================

    def create_salesman48_projects(self, salesman, company):
        """创建 Salesman 48 的浙沪区域项目"""
        # 获取客户
        customers = {}
        customer_names = [
            '杭州市第一人民医院',
            '浙江大学医学院附属第一医院',
            '上海交通大学医学院附属瑞金医院',
            '宁波市第二医院',
            '温州医科大学附属第一医院',
            '浙江省人民医院',
        ]

        for name in customer_names:
            try:
                customers[name] = Customer.objects.get(name=name)
            except Customer.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'错误：找不到客户 {name}'))
                return

        # 项目1：生化分析仪（早期）
        self.create_s48_project1_biochemistry(customers['杭州市第一人民医院'], salesman, company)

        # 项目2：免疫分析系统（中期）
        self.create_s48_project2_immunity(customers['浙江大学医学院附属第一医院'], salesman, company)

        # 项目3：血液分析流水线（后期）
        self.create_s48_project3_pipeline(customers['上海交通大学医学院附属瑞金医院'], salesman, company)

        # 项目4：血凝分析仪批量（已赢单）
        self.create_s48_project4_hemagglutination_won(customers['宁波市第二医院'], salesman, company)

        # 项目5：尿液分析仪（已输单）
        self.create_s48_project5_urine_lost(customers['温州医科大学附属第一医院'], salesman, company)

        # 项目6：微生物培养系统（暂停）
        self.create_s48_project6_microbiology_suspended(customers['浙江省人民医院'], salesman, company)

    def create_s48_project1_biochemistry(self, customer, salesman, company):
        """Salesman 48 - 项目1: 全自动生化分析仪采购（早期阶段）"""
        self.stdout.write('\n[S48-P1] 创建项目: 全自动生化分析仪采购（早期）...')

        today = date.today()
        start_date = today - timedelta(days=18)

        project = Project.objects.create(
            name='BS-400全自动生化分析仪采购项目',
            project_code=f'S48-PRJ{today.strftime("%y%m%d")}001',
            customer=customer,
            company=company,
            salesman=salesman,
            current_stage='线索验证/建档',
            status='active',
            win_probability=15,
            estimated_amount=Decimal('420000.00'),
            expected_close_date=today + timedelta(days=80),
            description='检验科生化室设备老化，需要升级换代，初步接触阶段',
            operator=salesman,
            createtime=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        )
        self.stdout.write(f'  [OK] 项目: {project.name} ({project.project_code})')

        # 阶段历史
        ProjectStageHistory.objects.create(
            project=project,
            from_stage=None,
            to_stage='线索获取',
            change_time=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time())),
            change_reason='检验科陈主任咨询生化分析仪升级方案',
            operator=salesman
        )

        stage_2_date = start_date + timedelta(days=5)
        ProjectStageHistory.objects.create(
            project=project,
            from_stage='线索获取',
            to_stage='线索验证/建档',
            change_time=timezone.make_aware(timezone.datetime.combine(stage_2_date, timezone.datetime.min.time())),
            change_reason='完成初次拜访，确认有真实采购需求，预算约42万',
            operator=salesman
        )

        # 销售日报
        reports = [
            {
                'date': start_date,
                'type': '客户活动',
                'desc': '首次拜访检验科陈主任，了解现有日立7180生化仪使用情况。设备已使用9年，老化严重，维修成本高。',
                'state': '【客户活动】阶段保持：线索获取'
            },
            {
                'date': start_date + timedelta(days=3),
                'type': '客户活动',
                'desc': '电话跟进，陈主任确认医院已批准设备更新预算，要求了解BS-400的技术参数和价格。',
                'state': '【客户活动】阶段保持：线索获取'
            },
            {
                'date': stage_2_date,
                'type': '阶段推进',
                'desc': '项目从【线索获取】推进到【线索验证/建档】。完成初次拜访，确认客户有真实采购需求，预算约42万元。',
                'state': '阶段推进：线索获取 → 线索验证/建档，赢单概率提升至15%'
            },
            {
                'date': today - timedelta(days=8),
                'type': '内部工作',
                'desc': '准备BS-400技术资料和性能对比表，重点突出处理速度（400测试/小时）和试剂开放性。',
                'state': '【内部工作】阶段保持：线索验证/建档'
            },
            {
                'date': today - timedelta(days=4),
                'type': '客户活动',
                'desc': '二次拜访，展示BS-400技术优势，陈主任对设备的自动化程度和质控功能表示认可。',
                'state': '【客户活动】阶段保持：线索验证/建档'
            },
            {
                'date': today - timedelta(days=1),
                'type': '客户活动',
                'desc': '电话沟通，了解到罗氏和贝克曼也在跟进，客户要求下周提供详细方案和报价。',
                'state': '【客户活动】阶段保持：线索验证/建档'
            },
        ]

        for report_data in reports:
            SalesReport.objects.create(
                project=project,
                salesman=salesman,
                company=company,
                date1=report_data['date'],
                type=report_data['type'],
                desc=report_data['desc'],
                state=report_data['state'],
                next_plan_date=report_data['date'] + timedelta(days=3),
                operator=salesman
            )

        self.stdout.write(f'  [OK] 创建了 {len(reports)} 条日报记录')

    def create_s48_project2_immunity(self, customer, salesman, company):
        """Salesman 48 - 项目2: 化学发光免疫分析系统（中期阶段）"""
        self.stdout.write('\n[S48-P2] 创建项目: 化学发光免疫分析系统（中期）...')

        today = date.today()
        start_date = today - timedelta(days=55)

        project = Project.objects.create(
            name='CL-2000i化学发光免疫分析系统采购项目',
            project_code=f'S48-PRJ{today.strftime("%y%m%d")}002',
            customer=customer,
            company=company,
            salesman=salesman,
            current_stage='测试/验证',
            status='active',
            win_probability=60,
            estimated_amount=Decimal('950000.00'),
            expected_close_date=today + timedelta(days=45),
            description='检验中心免疫室设备升级，省级三甲大型项目，正在进行样本测试验证',
            operator=salesman,
            createtime=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        )
        self.stdout.write(f'  [OK] 项目: {project.name} ({project.project_code})')

        # 阶段历史
        stages = [
            {'from': None, 'to': '线索获取', 'date': start_date, 'reason': '检验中心主任咨询免疫分析系统升级'},
            {'from': '线索获取', 'to': '商机立项', 'date': start_date + timedelta(days=6), 'reason': '确认列入年度采购计划'},
            {'from': '商机立项', 'to': '需求调研', 'date': start_date + timedelta(days=18), 'reason': '组织多部门需求调研会'},
            {'from': '需求调研', 'to': '方案/报价', 'date': start_date + timedelta(days=32), 'reason': '提交详细技术方案'},
            {'from': '方案/报价', 'to': '测试/验证', 'date': start_date + timedelta(days=48), 'reason': '客户要求现场测试验证性能'},
        ]

        for stage in stages:
            ProjectStageHistory.objects.create(
                project=project,
                from_stage=stage['from'],
                to_stage=stage['to'],
                change_time=timezone.make_aware(timezone.datetime.combine(stage['date'], timezone.datetime.min.time())),
                change_reason=stage['reason'],
                operator=salesman
            )

        # 销售日报
        reports = [
            {'date': start_date, 'type': '客户活动', 'desc': '首次拜访检验中心徐主任，了解到医院计划升级免疫分析系统，现有罗氏e601设备日样本量400+，需要提升到600+。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=3), 'type': '客户活动', 'desc': '电话跟进，确认项目已在院长办公会通过，预算充足约95万，时间表为Q2完成采购。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=6), 'type': '阶段推进', 'desc': '项目从【线索获取】推进到【商机立项】。医院正式将免疫系统升级列入年度重点采购计划。', 'state': '阶段推进：线索获取 → 商机立项，赢单概率提升至25%'},
            {'date': start_date + timedelta(days=12), 'type': '客户活动', 'desc': '拜访检验中心和免疫室，了解现有设备使用情况和工作流程，日样本量约400例。', 'state': '【客户活动】阶段保持：商机立项'},
            {'date': start_date + timedelta(days=18), 'type': '阶段推进', 'desc': '项目从【商机立项】推进到【需求调研】。组织需求调研会，参会：检验中心主任、免疫室主任、院长。', 'state': '阶段推进：商机立项 → 需求调研，赢单概率提升至35%'},
            {'date': start_date + timedelta(days=20), 'type': '客户活动', 'desc': '需求调研深入讨论，客户要求检测项目120+，通量600测试/小时，配备自动装载系统。', 'state': '【客户活动】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=26), 'type': '内部工作', 'desc': '根据需求调研结果，制定技术方案，选定CL-2000i型号，配置全自动装载系统和试剂冷藏模块。', 'state': '【内部工作】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=32), 'type': '阶段推进', 'desc': '项目从【需求调研】推进到【方案/报价】。正式提交详细技术方案和商务报价，预算95万元。', 'state': '阶段推进：需求调研 → 方案/报价，赢单概率提升至45%'},
            {'date': start_date + timedelta(days=40), 'type': '客户活动', 'desc': '方案讨论会，检验中心对技术方案高度认可，要求进行现场样本测试验证。', 'state': '【客户活动】阶段保持：方案/报价'},
            {'date': start_date + timedelta(days=48), 'type': '阶段推进', 'desc': '项目从【方案/报价】推进到【测试/验证】。客户安排现场测试，验证设备性能指标。', 'state': '阶段推进：方案/报价 → 测试/验证，赢单概率提升至60%'},
            {'date': today - timedelta(days=5), 'type': '客户活动', 'desc': '现场测试第一阶段，运行100例临床样本，结果与参考方法相关性达0.98，客户初步满意。', 'state': '【客户活动】阶段保持：测试/验证'},
            {'date': today - timedelta(days=1), 'type': '客户活动', 'desc': '现场测试第二阶段，继续运行50例特殊样本（溶血、脂血、黄疸），设备表现稳定，徐主任很满意。', 'state': '【客户活动】阶段保持：测试/验证'},
        ]

        for report_data in reports:
            SalesReport.objects.create(
                project=project,
                salesman=salesman,
                company=company,
                date1=report_data['date'],
                type=report_data['type'],
                desc=report_data['desc'],
                state=report_data['state'],
                next_plan_date=report_data['date'] + timedelta(days=4),
                operator=salesman
            )

        self.stdout.write(f'  [OK] 创建了 {len(reports)} 条日报记录')

    def create_s48_project3_pipeline(self, customer, salesman, company):
        """Salesman 48 - 项目3: 全自动血液细胞分析流水线（后期阶段）"""
        self.stdout.write('\n[S48-P3] 创建项目: 全自动血液细胞分析流水线（后期）...')

        today = date.today()
        start_date = today - timedelta(days=95)

        project = Project.objects.create(
            name='BC-6800+SA-1000血液分析流水线项目',
            project_code=f'S48-PRJ{today.strftime("%y%m%d")}003',
            customer=customer,
            company=company,
            salesman=salesman,
            current_stage='商务谈判',
            status='active',
            win_probability=75,
            estimated_amount=Decimal('1600000.00'),
            expected_close_date=today + timedelta(days=25),
            description='中心实验室血液室流水线配置，高端配置，日样本量1200+，进入最后谈判阶段',
            operator=salesman,
            createtime=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        )
        self.stdout.write(f'  [OK] 项目: {project.name} ({project.project_code})')

        # 阶段历史（完整的7个阶段）
        stages = [
            {'from': None, 'to': '线索获取', 'date': start_date, 'reason': '中心实验室主任咨询血液分析流水线方案'},
            {'from': '线索获取', 'to': '商机立项', 'date': start_date + timedelta(days=10), 'reason': '列入实验室升级改造计划'},
            {'from': '商机立项', 'to': '需求调研', 'date': start_date + timedelta(days=25), 'reason': '组织流水线需求论证会'},
            {'from': '需求调研', 'to': '方案/报价', 'date': start_date + timedelta(days=45), 'reason': '提交流水线配置方案'},
            {'from': '方案/报价', 'to': '测试/验证', 'date': start_date + timedelta(days=62), 'reason': '客户要求流水线现场演示'},
            {'from': '测试/验证', 'to': '准入/关键人认可', 'date': start_date + timedelta(days=75), 'reason': '实验室主任和院长认可方案'},
            {'from': '准入/关键人认可', 'to': '商务谈判', 'date': start_date + timedelta(days=85), 'reason': '进入价格谈判，讨论配置优化'},
        ]

        for stage in stages:
            ProjectStageHistory.objects.create(
                project=project,
                from_stage=stage['from'],
                to_stage=stage['to'],
                change_time=timezone.make_aware(timezone.datetime.combine(stage['date'], timezone.datetime.min.time())),
                change_reason=stage['reason'],
                operator=salesman
            )

        # 销售日报
        reports = [
            {'date': start_date, 'type': '客户活动', 'desc': '首次拜访中心实验室林主任，了解到医院计划引进血液分析流水线，现有手工操作效率低，日样本量1200+。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=5), 'type': '客户活动', 'desc': '电话跟进，确认项目已在医院战略发展会议通过，预算充足约160万，时间表为Q1完成招标。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=10), 'type': '阶段推进', 'desc': '项目从【线索获取】推进到【商机立项】。医院正式将流水线项目列入实验室升级改造计划。', 'state': '阶段推进：线索获取 → 商机立项，赢单概率提升至25%'},
            {'date': start_date + timedelta(days=18), 'type': '客户活动', 'desc': '拜访实验室，现场查看空间布局和工作流程，确认BC-6800+SA-1000流水线配置可行。', 'state': '【客户活动】阶段保持：商机立项'},
            {'date': start_date + timedelta(days=25), 'type': '阶段推进', 'desc': '项目从【商机立项】推进到【需求调研】。组织流水线需求论证会，参会：实验室主任、血液室主任、设备处、财务处。', 'state': '阶段推进：商机立项 → 需求调研，赢单概率提升至35%'},
            {'date': start_date + timedelta(days=28), 'type': '客户活动', 'desc': '需求论证会深入讨论，客户要求流水线处理能力150样本/小时，自动进样+自动涂片+自动染色。', 'state': '【客户活动】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=38), 'type': '内部工作', 'desc': '根据需求调研，制定流水线配置方案：BC-6800×2台+SA-1000×1台+自动进样系统+LIS对接。', 'state': '【内部工作】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=45), 'type': '阶段推进', 'desc': '项目从【需求调研】推进到【方案/报价】。正式提交流水线配置方案和报价，预算160万元。', 'state': '阶段推进：需求调研 → 方案/报价，赢单概率提升至45%'},
            {'date': start_date + timedelta(days=55), 'type': '客户活动', 'desc': '方案讨论会，实验室主任对流水线配置高度认可，要求安排现场演示和参观案例医院。', 'state': '【客户活动】阶段保持：方案/报价'},
            {'date': start_date + timedelta(days=62), 'type': '阶段推进', 'desc': '项目从【方案/报价】推进到【测试/验证】。安排客户到上海某三甲医院参观流水线运行情况。', 'state': '阶段推进：方案/报价 → 测试/验证，赢单概率提升至60%'},
            {'date': start_date + timedelta(days=65), 'type': '客户活动', 'desc': '客户参观案例医院，现场观看流水线运行，日处理1500+样本，自动化程度高，林主任非常满意。', 'state': '【客户活动】阶段保持：测试/验证'},
            {'date': start_date + timedelta(days=75), 'type': '阶段推进', 'desc': '项目从【测试/验证】推进到【准入/关键人认可】。实验室主任和分管副院长正式认可流水线方案。', 'state': '阶段推进：测试/验证 → 准入/关键人认可，赢单概率提升至70%'},
            {'date': start_date + timedelta(days=85), 'type': '阶段推进', 'desc': '项目从【准入/关键人认可】推进到【商务谈判】。进入价格谈判阶段，讨论配置优化和价格调整。', 'state': '阶段推进：准入/关键人认可 → 商务谈判，赢单概率提升至75%'},
            {'date': start_date + timedelta(days=88), 'type': '客户活动', 'desc': '价格谈判第一轮，客户要求优惠8%，我方表示需要内部申请，可以考虑优惠6%+试剂支持。', 'state': '【客户活动】阶段保持：商务谈判'},
            {'date': today - timedelta(days=4), 'type': '内部工作', 'desc': '内部协调商务部门和市场部，获批优惠6.5%+首年试剂优惠10%+3年延保的方案。', 'state': '【内部工作】阶段保持：商务谈判'},
            {'date': today - timedelta(days=1), 'type': '客户活动', 'desc': '价格谈判第二轮，告知客户最终方案，林主任表示基本接受，需要向院领导汇报后确定，预计本周给答复。', 'state': '【客户活动】阶段保持：商务谈判'},
        ]

        for report_data in reports:
            SalesReport.objects.create(
                project=project,
                salesman=salesman,
                company=company,
                date1=report_data['date'],
                type=report_data['type'],
                desc=report_data['desc'],
                state=report_data['state'],
                next_plan_date=report_data['date'] + timedelta(days=3),
                operator=salesman
            )

        self.stdout.write(f'  [OK] 创建了 {len(reports)} 条日报记录')

    def create_s48_project4_hemagglutination_won(self, customer, salesman, company):
        """Salesman 48 - 项目4: 血凝分析仪批量采购（已赢单）"""
        self.stdout.write('\n[S48-P4] 创建项目: 血凝分析仪批量采购（已赢单）...')

        today = date.today()
        start_date = today - timedelta(days=70)
        win_date = today - timedelta(days=5)

        project = Project.objects.create(
            name='CA-7000血凝分析仪批量采购项目（3台）',
            project_code=f'S48-PRJ{today.strftime("%y%m%d")}004',
            customer=customer,
            company=company,
            salesman=salesman,
            current_stage='收单',
            status='won',
            win_probability=100,
            estimated_amount=Decimal('680000.00'),
            actual_amount=Decimal('620000.00'),
            expected_close_date=win_date,
            actual_close_date=win_date,
            description='检验科凝血组批量采购3台血凝仪，老客户项目，已成功签约',
            operator=salesman,
            createtime=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        )
        self.stdout.write(f'  [OK] 项目: {project.name} ({project.project_code})')

        # 阶段历史
        stages = [
            {'from': None, 'to': '线索获取', 'date': start_date, 'reason': '老客户张主任咨询血凝仪批量采购'},
            {'from': '线索获取', 'to': '商机立项', 'date': start_date + timedelta(days=6), 'reason': '确认批量采购预算到位'},
            {'from': '商机立项', 'to': '方案/报价', 'date': start_date + timedelta(days=18), 'reason': '提供批量采购方案'},
            {'from': '方案/报价', 'to': '商务谈判', 'date': start_date + timedelta(days=38), 'reason': '批量优惠价格谈判'},
            {'from': '商务谈判', 'to': '中标/赢单', 'date': start_date + timedelta(days=55), 'reason': '客户确认采购，签订合同'},
            {'from': '中标/赢单', 'to': '装机/验收', 'date': start_date + timedelta(days=62), 'reason': '3台设备全部安装完成'},
            {'from': '装机/验收', 'to': '收单', 'date': win_date, 'reason': '项目赢单，成交金额：620000.00元。客户验收合格，款项已到账'},
        ]

        for stage in stages:
            ProjectStageHistory.objects.create(
                project=project,
                from_stage=stage['from'],
                to_stage=stage['to'],
                change_time=timezone.make_aware(timezone.datetime.combine(stage['date'], timezone.datetime.min.time())),
                change_reason=stage['reason'],
                operator=salesman
            )

        # 销售日报
        reports = [
            {'date': start_date, 'type': '客户活动', 'desc': '老客户张主任电话咨询血凝分析仪批量采购，医院新增2个检测点，需要3台CA-7000。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=3), 'type': '客户活动', 'desc': '拜访张主任，了解批量需求：3台CA-7000用于3个不同检测点，要求配置一致，预算约68万。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=6), 'type': '阶段推进', 'desc': '项目从【线索获取】推进到【商机立项】。老客户确认批量采购预算到位，项目正式立项。', 'state': '阶段推进：线索获取 → 商机立项，赢单概率提升至40%'},
            {'date': start_date + timedelta(days=12), 'type': '客户活动', 'desc': '现场查看3个检测点的安装空间，确认CA-7000配置可以满足需求，张主任希望获得批量优惠。', 'state': '【客户活动】阶段保持：商机立项'},
            {'date': start_date + timedelta(days=18), 'type': '阶段推进', 'desc': '项目从【商机立项】推进到【方案/报价】。提供批量采购方案和报价，3台总价68万元。', 'state': '阶段推进：商机立项 → 方案/报价，赢单概率提升至60%'},
            {'date': start_date + timedelta(days=25), 'type': '客户活动', 'desc': '方案讨论，客户对技术方案满意，要求批量优惠幅度能达到10%。', 'state': '【客户活动】阶段保持：方案/报价'},
            {'date': start_date + timedelta(days=38), 'type': '阶段推进', 'desc': '项目从【方案/报价】推进到【商务谈判】。批量采购优惠9%，最终价格62万元（3台）。', 'state': '阶段推进：方案/报价 → 商务谈判，赢单概率提升至75%'},
            {'date': start_date + timedelta(days=42), 'type': '客户活动', 'desc': '价格谈判，我方同意批量优惠9%+统一售后服务+试剂优惠，张主任非常满意。', 'state': '【客户活动】阶段保持：商务谈判'},
            {'date': start_date + timedelta(days=50), 'type': '内部工作', 'desc': '内部协调，准备批量采购合同和发货计划，确认3台设备同时交货。', 'state': '【内部工作】阶段保持：商务谈判'},
            {'date': start_date + timedelta(days=55), 'type': '阶段推进', 'desc': '项目从【商务谈判】推进到【中标/赢单】。客户正式签订批量采购合同，金额62万元。', 'state': '阶段推进：商务谈判 → 中标/赢单，赢单概率提升至95%'},
            {'date': start_date + timedelta(days=60), 'type': '客户活动', 'desc': '3台设备到货，协调安装调试工作，分别在3个检测点安装，培训各点操作人员。', 'state': '【客户活动】阶段保持：中标/赢单'},
            {'date': start_date + timedelta(days=62), 'type': '阶段推进', 'desc': '项目从【中标/赢单】推进到【装机/验收】。3台设备全部安装完成并通过验收。', 'state': '阶段推进：中标/赢单 → 装机/验收，赢单概率提升至98%'},
            {'date': win_date, 'type': '阶段推进', 'desc': '项目赢单！实际成交金额：620000.00元（3台）。客户对批量采购优惠和售后服务非常满意，款项已全额到账。老客户关系进一步巩固。', 'state': '✅ 项目赢单！成交金额：¥620,000.00元'},
        ]

        for report_data in reports:
            SalesReport.objects.create(
                project=project,
                salesman=salesman,
                company=company,
                date1=report_data['date'],
                type=report_data['type'],
                desc=report_data['desc'],
                state=report_data['state'],
                operator=salesman
            )

        self.stdout.write(f'  [OK] 创建了 {len(reports)} 条日报记录')

    def create_s48_project5_urine_lost(self, customer, salesman, company):
        """Salesman 48 - 项目5: 尿液分析仪更新（已输单）"""
        self.stdout.write('\n[S48-P5] 创建项目: 尿液分析仪更新（已输单）...')

        today = date.today()
        start_date = today - timedelta(days=45)
        lost_date = today - timedelta(days=15)

        project = Project.objects.create(
            name='UA-6800尿液分析仪更新项目',
            project_code=f'S48-PRJ{today.strftime("%y%m%d")}005',
            customer=customer,
            company=company,
            salesman=salesman,
            current_stage='方案/报价',
            status='lost',
            win_probability=50,
            estimated_amount=Decimal('280000.00'),
            lost_reason='price',
            lost_stage='方案/报价',
            competitor_info='爱威AVE-776',
            lost_detail='客户在方案比较阶段，因预算限制选择了爱威的低价方案（22万 vs 我方28万），虽然我方性能略优但客户更看重价格因素。',
            description='检验科尿液室设备更新，因价格因素输给低价竞争对手',
            operator=salesman,
            createtime=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        )
        self.stdout.write(f'  [OK] 项目: {project.name} ({project.project_code})')

        # 阶段历史
        stages = [
            {'from': None, 'to': '线索获取', 'date': start_date, 'reason': '检验科尿液室主任咨询设备更新'},
            {'from': '线索获取', 'to': '商机立项', 'date': start_date + timedelta(days=7), 'reason': '确认有采购计划'},
            {'from': '商机立项', 'to': '需求调研', 'date': start_date + timedelta(days=15), 'reason': '完成需求沟通'},
            {'from': '需求调研', 'to': '方案/报价', 'date': start_date + timedelta(days=25), 'reason': '提交方案和报价'},
        ]

        for stage in stages:
            ProjectStageHistory.objects.create(
                project=project,
                from_stage=stage['from'],
                to_stage=stage['to'],
                change_time=timezone.make_aware(timezone.datetime.combine(stage['date'], timezone.datetime.min.time())),
                change_reason=stage['reason'],
                operator=salesman
            )

        # 销售日报
        reports = [
            {'date': start_date, 'type': '客户活动', 'desc': '首次拜访检验科周主任，了解尿液室现有桂林优利特设备使用情况，日样本量约180例，设备已使用7年需要更换。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=4), 'type': '客户活动', 'desc': '电话沟通，周主任确认医院已批准设备更新预算，但预算有限约25-28万，要求了解UA-6800的价格。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=7), 'type': '阶段推进', 'desc': '项目从【线索获取】推进到【商机立项】。确认客户有采购计划，但预算有限。', 'state': '阶段推进：线索获取 → 商机立项，赢单概率提升至20%'},
            {'date': start_date + timedelta(days=10), 'type': '客户活动', 'desc': '二次拜访，详细了解需求，客户要求设备操作简单、维护成本低，强调预算限制。', 'state': '【客户活动】阶段保持：商机立项'},
            {'date': start_date + timedelta(days=15), 'type': '阶段推进', 'desc': '项目从【商机立项】推进到【需求调研】。完成需求沟通，客户重点关注价格和试剂成本。', 'state': '阶段推进：商机立项 → 需求调研，赢单概率提升至35%'},
            {'date': start_date + timedelta(days=20), 'type': '内部工作', 'desc': '准备UA-6800技术方案，强调性能优势和性价比，申请价格优惠。', 'state': '【内部工作】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=25), 'type': '阶段推进', 'desc': '项目从【需求调研】推进到【方案/报价】。提交方案和报价，总价28万元。', 'state': '阶段推进：需求调研 → 方案/报价，赢单概率提升至50%'},
            {'date': start_date + timedelta(days=28), 'type': '客户活动', 'desc': '方案讨论，客户对技术方案认可，但表示价格超出预算，希望能降到25万以内。', 'state': '【客户活动】阶段保持：方案/报价'},
            {'date': start_date + timedelta(days=30), 'type': '内部工作', 'desc': '内部协调申请价格优惠，但因成本限制只能降到27万，无法达到客户要求的25万。', 'state': '【内部工作】阶段保持：方案/报价'},
            {'date': lost_date, 'type': '内部工作', 'desc': '项目输单。流失原因：价格因素。流失阶段：方案/报价。详细说明：客户因预算限制选择了爱威的低价方案（22万 vs 我方最低27万），虽然我方性能略优（检测速度更快、参数更多）但客户更看重价格，最终选择了竞品。', 'state': '❌ 项目输单 - 流失原因：价格因素，流失阶段：方案/报价'},
        ]

        for report_data in reports:
            SalesReport.objects.create(
                project=project,
                salesman=salesman,
                company=company,
                date1=report_data['date'],
                type=report_data['type'],
                desc=report_data['desc'],
                state=report_data['state'],
                operator=salesman
            )

        self.stdout.write(f'  [OK] 创建了 {len(reports)} 条日报记录')

    def create_s48_project6_microbiology_suspended(self, customer, salesman, company):
        """Salesman 48 - 项目6: 微生物培养鉴定系统（暂停）"""
        self.stdout.write('\n[S48-P6] 创建项目: 微生物培养鉴定系统（暂停）...')

        today = date.today()
        start_date = today - timedelta(days=85)
        suspend_date = today - timedelta(days=12)

        project = Project.objects.create(
            name='BACT/ALERT 3D微生物培养系统采购项目',
            project_code=f'S48-PRJ{today.strftime("%y%m%d")}006',
            customer=customer,
            company=company,
            salesman=salesman,
            current_stage='需求调研',
            status='suspended',
            win_probability=25,
            estimated_amount=Decimal('750000.00'),
            expected_close_date=today + timedelta(days=150),
            suspend_reason='微生物室正在进行P2实验室升级改造，工程延期2-3个月，设备采购需等改造完成',
            expected_resume_date=today + timedelta(days=90),
            description='微生物室培养鉴定系统升级，因实验室改造延期暂停跟进',
            operator=salesman,
            createtime=timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
        )
        self.stdout.write(f'  [OK] 项目: {project.name} ({project.project_code})')

        # 阶段历史
        stages = [
            {'from': None, 'to': '线索获取', 'date': start_date, 'reason': '微生物室主任咨询培养鉴定系统'},
            {'from': '线索获取', 'to': '线索验证/建档', 'date': start_date + timedelta(days=10), 'reason': '确认有升级需求和预算'},
            {'from': '线索验证/建档', 'to': '商机立项', 'date': start_date + timedelta(days=25), 'reason': '项目列入采购计划'},
            {'from': '商机立项', 'to': '需求调研', 'date': start_date + timedelta(days=45), 'reason': '开始详细需求调研'},
        ]

        for stage in stages:
            ProjectStageHistory.objects.create(
                project=project,
                from_stage=stage['from'],
                to_stage=stage['to'],
                change_time=timezone.make_aware(timezone.datetime.combine(stage['date'], timezone.datetime.min.time())),
                change_reason=stage['reason'],
                operator=salesman
            )

        # 销售日报
        reports = [
            {'date': start_date, 'type': '客户活动', 'desc': '首次拜访微生物室钱主任，了解到医院计划升级微生物培养鉴定系统，现有手工培养效率低、周期长。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=5), 'type': '客户活动', 'desc': '电话沟通，钱主任确认有明确的采购计划，预算约75万元，同时提到实验室正在规划P2改造。', 'state': '【客户活动】阶段保持：线索获取'},
            {'date': start_date + timedelta(days=10), 'type': '阶段推进', 'desc': '项目从【线索获取】推进到【线索验证/建档】。确认客户有真实升级需求和预算。', 'state': '阶段推进：线索获取 → 线索验证/建档，赢单概率提升至10%'},
            {'date': start_date + timedelta(days=18), 'type': '客户活动', 'desc': '拜访微生物室，了解现有培养方法和工作流程，日培养样本约40例，周期需要48-72小时。', 'state': '【客户活动】阶段保持：线索验证/建档'},
            {'date': start_date + timedelta(days=25), 'type': '阶段推进', 'desc': '项目从【线索验证/建档】推进到【商机立项】。项目已列入医院年度采购计划。', 'state': '阶段推进：线索验证/建档 → 商机立项，赢单概率提升至20%'},
            {'date': start_date + timedelta(days=35), 'type': '客户活动', 'desc': '需求沟通会，参会：微生物室主任、检验中心主任、基建科长，讨论P2实验室改造和设备采购的协调。', 'state': '【客户活动】阶段保持：商机立项'},
            {'date': start_date + timedelta(days=45), 'type': '阶段推进', 'desc': '项目从【商机立项】推进到【需求调研】。开始详细需求调研，但客户提醒设备采购需等P2改造完成。', 'state': '阶段推进：商机立项 → 需求调研，赢单概率提升至25%'},
            {'date': start_date + timedelta(days=50), 'type': '客户活动', 'desc': '需求调研会，讨论培养系统容量、阳性时间、数据管理等需求，客户要求配置120瓶位系统。', 'state': '【客户活动】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=60), 'type': '内部工作', 'desc': '根据需求调研准备技术方案，选定BACT/ALERT 3D型号，配置120瓶位+全自动装卸载。', 'state': '【内部工作】阶段保持：需求调研'},
            {'date': start_date + timedelta(days=70), 'type': '客户活动', 'desc': '电话跟进，基建科告知P2实验室改造工程因设计变更延期，预计延期2-3个月。', 'state': '【客户活动】阶段保持：需求调研'},
            {'date': suspend_date, 'type': '内部工作', 'desc': '项目状态变更为【暂停跟进】。暂停原因：微生物室正在进行P2实验室升级改造，工程延期2-3个月，设备采购需等改造完成后重新启动。', 'state': '⏸️ 项目暂停跟进 - 等待实验室改造完成'},
        ]

        for report_data in reports:
            SalesReport.objects.create(
                project=project,
                salesman=salesman,
                company=company,
                date1=report_data['date'],
                type=report_data['type'],
                desc=report_data['desc'],
                state=report_data['state'],
                operator=salesman
            )

        self.stdout.write(f'  [OK] 创建了 {len(reports)} 条日报记录')
