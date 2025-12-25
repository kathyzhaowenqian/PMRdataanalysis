"""
重构后的销售日报视图
支持项目管理、阶段自动跟踪、API接口
"""

from typing import Any
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.utils import timezone
from datetime import date, datetime
import json
import pytz
import hashlib

from .models import (
    Customer, Project, ProjectStageHistory, SalesReport,
    Company, ReportUserInfo, SALES_STAGE_CHOICES
)


china_tz = pytz.timezone('Asia/Shanghai')

# 用户-公司映射
user_company_dict = {
    1: 1,
 
}


def transfer_date(frontend_date):
    """转换前端日期为中国时区时间"""
    date_obj = datetime.strptime(frontend_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    date_obj = date_obj.replace(tzinfo=pytz.UTC)
    date_obj = date_obj.astimezone(china_tz)
    return date_obj


class Submit(View):
    """销售日报提交视图"""

    def get(self, request):
        """显示日报提交表单"""
        # 权限检查
        JcReport_view_group_list = ['JCReport']
        user_in_group_list = request.user.groups.values('name')

        has_permission = False
        for user_in_group_dict in user_in_group_list:
            if user_in_group_dict['name'] in JcReport_view_group_list:
                has_permission = True
                break

        if request.user.username in ['admin', 'zwq8zhj']:
            has_permission = True

        if not has_permission:
            return HttpResponse('您好，目前您暂无权限访问')

        today = date.today()
        context = {'today': today}
        return render(request, 'report/report_new.html', context=context)

    def post(self, request):
        """处理日报提交 - 支持三种操作类型"""
        login_user = request.user.id

        if not login_user:
            return JsonResponse({'status': 'error', 'message': '用户未登录'}, status=401)

        try:
            data = json.loads(request.body)
            companyid = user_company_dict.get(login_user)

            if not companyid:
                return JsonResponse({'status': 'error', 'message': '用户未配置公司'}, status=400)

            # 获取操作类型
            operation_type = data.get('operationType')

            # 判断是新建项目还是选择现有项目
            if data.get('projectMode') == 'new':
                # 创建新项目（逻辑保持不变）
                project = self._create_new_project(data, login_user, companyid)
                # 新建项目默认作为活动记录
                result = self._record_activity(project, data, login_user, companyid)
            else:
                # 使用现有项目
                project_id = data.get('selectedProject')
                if not project_id:
                    return JsonResponse({'status': 'error', 'message': '请选择项目'}, status=400)

                project = Project.objects.get(id=project_id)

                # 根据操作类型处理
                if operation_type == 'activity':
                    # 记录跟进活动（阶段不变）
                    result = self._record_activity(project, data, login_user, companyid)

                elif operation_type == 'advance':
                    # 推进项目阶段
                    result = self._advance_stage(project, data, login_user, companyid)

                elif operation_type == 'conclude':
                    # 标记项目结果
                    result = self._conclude_project(project, data, login_user, companyid)

                else:
                    return JsonResponse({'status': 'error', 'message': '无效的操作类型'}, status=400)

            return JsonResponse(result, status=201)

        except Project.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '项目不存在'}, status=404)
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'提交失败：{str(e)}'
            }, status=500)

    def _record_activity(self, project, data, user_id, company_id):
        """记录跟进活动（不改变项目阶段）"""

        # 将前端的活动类型映射到数据库的简化中文类型
        activity_type_map = {
            # 新版简化类型（前端当前使用）
            'customer': '客户活动',
            'internal': '内部工作',
            'stage_advance': '阶段推进',
            # 旧版详细类型（兼容性保留）
            'customer_visit': '客户活动',
            'phone_call': '客户活动',
            'tech_demo': '客户活动',
            'negotiation': '客户活动',
            'proposal_prep': '内部工作',
            'internal_coord': '内部工作',
            'bid_prep': '内部工作',
            'other': '内部工作',
        }
        # 获取数据库活动类型（中文简化值）
        db_activity_type = activity_type_map.get(data.get('activityType', ''), '内部工作')
        state_text = f"【{db_activity_type}】阶段保持：{project.current_stage}"

        # 创建销售日报记录
        report = SalesReport.objects.create(
            project=project,
            salesman_id=user_id,
            company_id=company_id,
            date1=transfer_date(data['date1']),
            type=db_activity_type,
            desc=data.get('activityContent', ''),
            state=state_text,
            next_plan_date=transfer_date(data['nextPlanDate']) if data.get('nextPlanDate') else None,
            operator_id=user_id
        )

        # 更新项目的最后更新时间
        if data.get('nextPlanDate'):
            project.updatetime = timezone.now()
            project.save(update_fields=['updatetime'])

        return {
            'status': 'success',
            'message': '活动记录成功',
            'operation': 'activity',
            'project_id': project.id,
            'project_code': project.project_code,
            'report_id': report.id
        }

    def _advance_stage(self, project, data, user_id, company_id):
        """推进项目阶段"""

        new_stage = data.get('newStage')
        stage_reason = data.get('stageAdvanceReason', '')

        if not new_stage:
            raise ValueError('未指定新阶段')

        if project.current_stage == new_stage:
            raise ValueError('新阶段与当前阶段相同，无需更新')

        old_stage = project.current_stage

        # 1. 创建阶段变更历史
        stage_history = ProjectStageHistory.objects.create(
            project=project,
            from_stage=old_stage,
            to_stage=new_stage,
            change_reason=stage_reason,
            operator_id=user_id
            # days_in_previous_stage 会在save()中自动计算
        )

        # 2. 更新项目
        project.current_stage = new_stage
        project.win_probability = self._calculate_win_probability(new_stage)

        # 如果推进到成交阶段，自动标记为won
        if new_stage in ['中标/赢单', '装机/验收', '收单']:
            project.status = 'won'
            if not project.actual_close_date:
                project.actual_close_date = date.today()

        # 更新预计成交时间（如提供）
        if data.get('expectedCloseDate'):
            project.expected_close_date = transfer_date(data['expectedCloseDate']).date()

        project.save()

        # 3. 创建销售日报记录（type='阶段推进'）
        state_text = f"阶段推进：{old_stage} → {new_stage}，赢单概率提升至{project.win_probability}%"

        report = SalesReport.objects.create(
            project=project,
            salesman_id=user_id,
            company_id=company_id,
            date1=transfer_date(data['date1']),
            type='阶段推进',  # 阶段推进类型
            desc=f'项目从【{old_stage}】推进到【{new_stage}】。{stage_reason}',
            state=state_text,
            operator_id=user_id
        )

        return {
            'status': 'success',
            'message': f'项目阶段已从【{old_stage}】推进到【{new_stage}】',
            'operation': 'advance',
            'project_id': project.id,
            'project_code': project.project_code,
            'old_stage': old_stage,
            'new_stage': new_stage,
            'days_in_stage': stage_history.days_in_previous_stage,
            'new_probability': project.win_probability
        }

    def _conclude_project(self, project, data, user_id, company_id):
        """标记项目结果（赢单/输单/暂停）"""

        conclusion_type = data.get('conclusionType')

        if not conclusion_type:
            raise ValueError('未指定结果类型')

        if conclusion_type == 'won':
            # 赢单处理
            actual_amount = data.get('actualAmount')
            if not actual_amount:
                raise ValueError('请填写实际成交金额')

            project.status = 'won'
            project.actual_amount = actual_amount
            project.actual_close_date = transfer_date(data['actualCloseDate']).date() if data.get('actualCloseDate') else date.today()

            # 如果未到最后阶段，自动推进到"收单"
            if project.current_stage != '收单':
                old_stage = project.current_stage
                project.current_stage = '收单'
                project.win_probability = 100

                # 创建阶段历史
                ProjectStageHistory.objects.create(
                    project=project,
                    from_stage=old_stage,
                    to_stage='收单',
                    change_reason=f'项目赢单，成交金额：{actual_amount}元。{data.get("winRemark", "")}',
                    operator_id=user_id
                )

            project.save()

            # 创建日报记录
            state_text = f"✅ 项目赢单！成交金额：¥{actual_amount:,.2f}元"

            SalesReport.objects.create(
                project=project,
                salesman_id=user_id,
                company_id=company_id,
                date1=transfer_date(data['date1']),
                type='阶段推进',
                desc=f'项目赢单！实际成交金额：{actual_amount}元。{data.get("winRemark", "")}',
                state=state_text,
                operator_id=user_id
            )

            message = f'恭喜！项目赢单，成交金额：{actual_amount}元'

        elif conclusion_type == 'lost':
            # 输单处理
            lost_reason = data.get('lostReason')
            lost_detail = data.get('lostDetail')

            if not lost_reason or not lost_detail:
                raise ValueError('请填写流失原因和详细说明')

            project.status = 'lost'
            project.lost_reason = lost_reason
            project.lost_stage = project.current_stage  # 记录流失时的阶段
            project.lost_detail = lost_detail
            project.competitor_info = data.get('competitorInfo', '')
            project.save()

            # 创建日报记录
            reason_text = dict([
                ('price', '价格因素'),
                ('competitor', '竞争对手中标'),
                ('budget_cancel', '客户预算取消'),
                ('product_mismatch', '产品不符合需求'),
                ('timing', '时机不合适'),
                ('other', '其他'),
            ]).get(lost_reason, lost_reason)

            state_text = f"❌ 项目输单 - 流失原因：{reason_text}，流失阶段：{project.lost_stage}"

            SalesReport.objects.create(
                project=project,
                salesman_id=user_id,
                company_id=company_id,
                date1=transfer_date(data['date1']),
                type='内部工作',
                desc=f'项目输单。流失原因：{reason_text}。流失阶段：{project.lost_stage}。详细说明：{lost_detail}',
                state=state_text,
                operator_id=user_id
            )

            message = f'项目已标记为输单，流失原因：{reason_text}'

        elif conclusion_type == 'suspended':
            # 暂停处理
            suspend_reason = data.get('suspendReason')

            if not suspend_reason:
                raise ValueError('请填写暂停原因')

            project.status = 'suspended'
            project.suspend_reason = suspend_reason
            project.expected_resume_date = transfer_date(data['expectedResumeDate']).date() if data.get('expectedResumeDate') else None
            project.save()

            # 创建日报记录
            state_text = f"⏸️ 项目暂停跟进 - {suspend_reason[:30]}..."

            SalesReport.objects.create(
                project=project,
                salesman_id=user_id,
                company_id=company_id,
                date1=transfer_date(data['date1']),
                type='内部工作',
                desc=f'项目暂停跟进。暂停原因：{suspend_reason}',
                state=state_text,
                operator_id=user_id
            )

            message = f'项目已暂停跟进'

        else:
            raise ValueError('无效的结果类型')

        return {
            'status': 'success',
            'message': message,
            'operation': 'conclude',
            'conclusion_type': conclusion_type,
            'project_id': project.id,
            'project_code': project.project_code,
            'project_status': project.status
        }

    def _create_new_project(self, data, salesman_id, company_id):
        """创建新项目"""
        # 获取或创建客户
        customer_name = data.get('customerName', '').strip()
        customer, _ = Customer.objects.get_or_create(
            name=customer_name,
            defaults={
                'customer_type': 'hospital',
                'level': 'C',
            }
        )

        # 生成项目编号
        project_code = self._generate_project_code(
            data.get('projectName', ''),
            salesman_id,
            company_id
        )

        # 计算赢单概率
        current_stage = data.get('currentStage', '线索获取')
        win_probability = self._calculate_win_probability(current_stage)

        # 创建项目
        project = Project.objects.create(
            name=data.get('projectName', ''),
            project_code=project_code,
            customer=customer,
            company_id=company_id,
            salesman_id=salesman_id,
            current_stage=current_stage,
            status='active',
            win_probability=win_probability,
            estimated_amount=data.get('estimatedAmount'),
            expected_close_date=transfer_date(data['expectedCloseDate']).date() if data.get('expectedCloseDate') else None,
            description=data.get('projectDesc', ''),
            operator_id=salesman_id,
        )

        # 创建初始阶段历史
        ProjectStageHistory.objects.create(
            project=project,
            from_stage=None,  # 初始阶段
            to_stage=current_stage,
            change_time=timezone.now(),
            days_in_previous_stage=0,
            change_reason='项目创建',
            operator_id=salesman_id,
        )

        return project

    def _update_project_stage(self, project, new_stage, reason, operator_id):
        """更新项目阶段"""
        if project.current_stage == new_stage:
            return  # 阶段未变化，无需更新

        old_stage = project.current_stage

        # 创建阶段变更历史
        ProjectStageHistory.objects.create(
            project=project,
            from_stage=old_stage,
            to_stage=new_stage,
            change_time=timezone.now(),
            change_reason=reason,
            operator_id=operator_id,
        )

        # 更新项目当前阶段和赢单概率
        project.current_stage = new_stage
        project.win_probability = self._calculate_win_probability(new_stage)

        # 如果进入赢单阶段，更新状态
        if new_stage in ['中标/赢单', '装机/验收', '收单']:
            project.status = 'won'
            if not project.actual_close_date:
                project.actual_close_date = date.today()

        project.operator_id = operator_id
        project.save()

    def _generate_project_code(self, project_name, salesman_id, company_id):
        """生成项目编号"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        hash_str = hashlib.md5(
            f"{project_name}{salesman_id}{company_id}{timestamp}".encode()
        ).hexdigest()[:6]
        return f"PRJ{timestamp[2:]}{hash_str.upper()}"

    def _calculate_win_probability(self, stage):
        """根据阶段计算赢单概率"""
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
        return stage_probability_map.get(stage, 0)


class ProjectAPI(View):
    """项目API接口"""

    def get(self, request, project_id=None):
        """
        获取项目列表或详情
        GET /SALESREPORT/api/projects/ - 搜索项目列表
        GET /SALESREPORT/api/projects/{id}/ - 获取项目详情
        """
        if not request.user.is_authenticated:
            return JsonResponse({'error': '未登录'}, status=401)

        if project_id:
            # 获取项目详情
            try:
                project = Project.objects.select_related('customer', 'company', 'salesman').get(
                    id=project_id,
                    is_active=True
                )

                # 权限检查：只能查看自己负责的项目或有特殊权限
                if not self._can_view_project(request.user, project):
                    return JsonResponse({'error': '无权限'}, status=403)

                data = {
                    'id': project.id,
                    'name': project.name,
                    'project_code': project.project_code,
                    'customer_name': project.customer.name,
                    'current_stage': project.current_stage,
                    'status': project.status,
                    'win_probability': project.win_probability,
                    'estimated_amount': str(project.estimated_amount) if project.estimated_amount else None,
                    'expected_close_date': project.expected_close_date.isoformat() if project.expected_close_date else None,
                    'description': project.description,
                }
                return JsonResponse(data)

            except Project.DoesNotExist:
                return JsonResponse({'error': '项目不存在'}, status=404)
        else:
            # 搜索项目列表
            search = request.GET.get('search', '').strip()
            # 允许选择所有未流失的项目（active、won、suspended），排除lost
            queryset = Project.objects.filter(is_active=True).exclude(status='lost')

            # 权限过滤
            if not request.user.is_superuser and request.user.username not in ['zwq8zhj']:
                queryset = queryset.filter(salesman=request.user)

            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(project_code__icontains=search) |
                    Q(customer__name__icontains=search)
                )

            queryset = queryset.select_related('customer').order_by('-updatetime')[:20]

            data = [{
                'id': p.id,
                'name': p.name,
                'project_code': p.project_code,
                'current_stage': p.current_stage,
                'customer_name': p.customer.name,
            } for p in queryset]

            return JsonResponse(data, safe=False)

    def _can_view_project(self, user, project):
        """检查用户是否有权查看项目"""
        if user.is_superuser or user.username in ['zwq8zhj']:
            return True
        return project.salesman == user


class CustomerAPI(View):
    """客户API接口"""

    def get(self, request):
        """
        搜索客户列表
        GET /SALESREPORT/api/customers/?search=xxx
        """
        if not request.user.is_authenticated:
            return JsonResponse({'error': '未登录'}, status=401)

        search = request.GET.get('search', '').strip()
        queryset = Customer.objects.filter(is_active=True)

        if search:
            queryset = queryset.filter(name__icontains=search)

        queryset = queryset.order_by('-updatetime')[:10]

        data = [{
            'id': c.id,
            'name': c.name,
            'customer_type': c.customer_type,
            'level': c.level,
        } for c in queryset]

        return JsonResponse(data, safe=False)
