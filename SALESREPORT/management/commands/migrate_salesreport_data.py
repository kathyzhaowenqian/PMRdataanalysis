"""
数据迁移脚本：将旧的SalesReport数据迁移到新的Project架构

使用方法：
python manage.py migrate_salesreport_data [--dry-run]

参数：
--dry-run: 模拟运行，不实际写入数据库
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from collections import defaultdict
import hashlib
from datetime import datetime

from SALESREPORT.models_new import (
    Customer, Project, ProjectStageHistory, SalesReport, SalesReportOld,
    SALES_STAGE_CHOICES
)


class Command(BaseCommand):
    help = '将旧的销售日报数据迁移到新的Project架构'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='模拟运行，不实际写入数据库',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('=== 模拟运行模式 ==='))
        else:
            self.stdout.write(self.style.WARNING('=== 正式迁移模式 ==='))

        # 统计信息
        stats = {
            'customers': 0,
            'projects': 0,
            'stage_histories': 0,
            'sales_reports': 0,
        }

        try:
            with transaction.atomic():
                # Step 1: 获取所有旧数据
                old_reports = SalesReportOld.objects.filter(is_active=True).order_by('project', 'date1')
                total_records = old_reports.count()
                self.stdout.write(f'\n找到 {total_records} 条旧日报记录\n')

                if total_records == 0:
                    self.stdout.write(self.style.WARNING('没有需要迁移的数据'))
                    return

                # Step 2: 按项目名称+负责人分组
                project_groups = defaultdict(list)
                for report in old_reports:
                    # 使用 项目名+负责人+公司 作为唯一标识
                    key = (report.project.strip(), report.salesman_id, report.company_id)
                    project_groups[key].append(report)

                self.stdout.write(f'识别出 {len(project_groups)} 个独立项目\n')

                # Step 3: 处理每个项目
                for (project_name, salesman_id, company_id), reports in project_groups.items():
                    # 按日期排序
                    reports.sort(key=lambda x: x.date1)

                    # 创建或获取客户
                    customer = self._get_or_create_customer(project_name, stats, dry_run)

                    # 创建项目
                    project = self._create_project(
                        project_name, salesman_id, company_id,
                        customer, reports, stats, dry_run
                    )

                    if not dry_run:
                        # 创建阶段历史
                        self._create_stage_histories(project, reports, stats)

                        # 创建新的销售日报记录
                        self._create_sales_reports(project, reports, stats)

                # 输出统计
                self.stdout.write('\n' + '=' * 50)
                self.stdout.write(self.style.SUCCESS('迁移统计：'))
                self.stdout.write(f'  - 创建客户数：{stats["customers"]}')
                self.stdout.write(f'  - 创建项目数：{stats["projects"]}')
                self.stdout.write(f'  - 阶段变更记录：{stats["stage_histories"]}')
                self.stdout.write(f'  - 销售日报记录：{stats["sales_reports"]}')
                self.stdout.write('=' * 50 + '\n')

                if dry_run:
                    self.stdout.write(self.style.WARNING('模拟运行完成，未实际写入数据'))
                    raise Exception("Dry run - rolling back")  # 回滚事务
                else:
                    self.stdout.write(self.style.SUCCESS('数据迁移成功完成！'))

        except Exception as e:
            if str(e) == "Dry run - rolling back":
                self.stdout.write(self.style.SUCCESS('模拟运行完成'))
            else:
                self.stdout.write(self.style.ERROR(f'迁移失败：{str(e)}'))
                raise

    def _get_or_create_customer(self, project_name, stats, dry_run):
        """创建或获取客户记录"""
        # 简单策略：从项目名称中提取客户名称
        # 如果项目名称包含常见分隔符，取第一部分作为客户名
        customer_name = project_name.split('-')[0].split('_')[0].strip()

        if dry_run:
            # 模拟运行，返回虚拟customer
            class DummyCustomer:
                id = 1
                name = customer_name
            stats['customers'] += 1
            return DummyCustomer()

        customer, created = Customer.objects.get_or_create(
            name=customer_name,
            defaults={
                'customer_type': 'hospital',
                'level': 'C',
            }
        )

        if created:
            stats['customers'] += 1
            self.stdout.write(f'  创建客户: {customer_name}')

        return customer

    def _generate_project_code(self, project_name, salesman_id, company_id):
        """生成项目编号"""
        # 使用时间戳 + 哈希确保唯一性
        timestamp = datetime.now().strftime('%Y%m%d')
        hash_str = hashlib.md5(
            f"{project_name}{salesman_id}{company_id}".encode()
        ).hexdigest()[:6]
        return f"PRJ{timestamp}{hash_str.upper()}"

    def _create_project(self, project_name, salesman_id, company_id,
                       customer, reports, stats, dry_run):
        """创建项目记录"""
        # 获取最新的stage作为当前阶段
        latest_stage = reports[-1].stage
        first_report = reports[0]

        # 计算赢单概率（基于阶段）
        stage_probability_map = {
            '线索获取': 10,
            '线索验证/建档': 15,
            '商机立项': 20,
            '需求调研': 30,
            '方案/报价': 40,
            '测试/验证': 50,
            '准入/关键人认可': 60,
            '商务谈判': 70,
            '招采/挂网/比选': 80,
            '中标/赢单': 95,
            '装机/验收': 98,
            '收单': 100,
        }
        win_probability = stage_probability_map.get(latest_stage, 0)

        # 判断项目状态
        if latest_stage in ['中标/赢单', '装机/验收', '收单']:
            status = 'won'
        else:
            status = 'active'

        project_code = self._generate_project_code(project_name, salesman_id, company_id)

        if dry_run:
            # 模拟运行
            class DummyProject:
                id = stats['projects'] + 1
                name = project_name
                project_code = project_code
                current_stage = latest_stage

            stats['projects'] += 1
            self.stdout.write(f'  [模拟] 项目: {project_name} ({project_code})')
            return DummyProject()

        project = Project.objects.create(
            name=project_name,
            project_code=project_code,
            customer=customer,
            company_id=company_id,
            salesman_id=salesman_id,
            current_stage=latest_stage,
            status=status,
            win_probability=win_probability,
            description=first_report.desc,
            operator_id=salesman_id,
        )

        stats['projects'] += 1
        self.stdout.write(f'  创建项目: {project_name} ({project_code})')

        return project

    def _create_stage_histories(self, project, reports, stats):
        """创建阶段变更历史"""
        stage_changes = []
        previous_stage = None

        for report in reports:
            current_stage = report.stage

            # 如果阶段发生变化，记录
            if current_stage != previous_stage:
                stage_changes.append({
                    'from_stage': previous_stage,
                    'to_stage': current_stage,
                    'change_time': timezone.make_aware(
                        datetime.combine(report.date1, datetime.min.time())
                    ),
                    'operator_id': report.salesman_id,
                })
                previous_stage = current_stage

        # 批量创建阶段历史
        for i, change in enumerate(stage_changes):
            # 计算停留天数
            if i > 0:
                prev_change_time = stage_changes[i - 1]['change_time']
                days_diff = (change['change_time'].date() - prev_change_time.date()).days
            else:
                days_diff = 0

            ProjectStageHistory.objects.create(
                project=project,
                from_stage=change['from_stage'],
                to_stage=change['to_stage'],
                change_time=change['change_time'],
                days_in_previous_stage=days_diff,
                operator_id=change['operator_id'],
            )
            stats['stage_histories'] += 1

        if stage_changes:
            self.stdout.write(f'    └─ 创建 {len(stage_changes)} 条阶段变更记录')

    def _create_sales_reports(self, project, reports, stats):
        """创建新的销售日报记录"""
        for report in reports:
            SalesReport.objects.create(
                project=project,
                salesman_id=report.salesman_id,
                company_id=report.company_id,
                date1=report.date1,
                desc=report.desc,
                type=report.type,
                state=report.state,
                last_feedback_date=report.date2,
                next_plan_date=report.date3,
                operator_id=report.operator_id,
                createtime=report.createtime,
                updatetime=report.updatetime,
            )
            stats['sales_reports'] += 1

        self.stdout.write(f'    └─ 创建 {len(reports)} 条日报记录')
