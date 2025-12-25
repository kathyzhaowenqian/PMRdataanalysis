"""
销售漏斗分析视图
提供多维度的销售数据分析
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg, Sum, Q, F
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from collections import defaultdict

from .models import (
    Project, ProjectStageHistory, SalesReport,
    SALES_STAGE_CHOICES
)


@login_required
def funnel_analysis_view(request):
    """漏斗分析主页面"""
    # 权限检查
    if not (request.user.is_superuser or
            request.user.username == 'zwq8zhj' or
            request.user.groups.filter(name__in=['boss', 'JCboss']).exists()):
        return render(request, 'report/no_permission.html')

    return render(request, 'report/funnel_analysis.html')


@login_required
def funnel_data_api(request):
    """漏斗数据API"""
    # 获取时间范围参数
    days = int(request.GET.get('days', 90))  # 默认最近90天
    salesman_id = request.GET.get('salesman')  # 可选：特定销售
    company_id = request.GET.get('company')  # 可选：特定公司

    # 计算时间范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # 构建查询（添加时间筛选）
    queryset = Project.objects.filter(
        is_active=True,
        createtime__gte=start_date  # 只统计时间范围内创建的项目
    )

    if salesman_id:
        queryset = queryset.filter(salesman_id=salesman_id)
    if company_id:
        queryset = queryset.filter(company_id=company_id)

    # 获取符合筛选条件的项目ID列表（用于后续所有 ProjectStageHistory 查询）
    allowed_project_ids = list(queryset.values_list('id', flat=True))

    # 1. 各阶段项目数量统计（漏斗统计：递减的漏斗效果）
    stage_stats = {}
    stage_stats_filled = []  # 重命名：补齐漏斗（到达后续阶段算完成前面阶段）
    total_projects = queryset.count()  # 总项目数（用于 summary）
    stages_list = list(SALES_STAGE_CHOICES)  # 转换为列表以便索引

    for i, (stage_value, stage_label) in enumerate(stages_list):
        # 该阶段及以后的所有阶段（确保漏斗递减）
        current_and_subsequent_stages = [s[0] for s in stages_list[i:]]

        # 统计进入过该阶段或之后阶段的项目数（保证递减）
        count = ProjectStageHistory.objects.filter(
            to_stage__in=current_and_subsequent_stages,
            project__id__in=allowed_project_ids
        ).order_by().values('project').distinct().count()  # 清除默认排序以确保 distinct 正确工作

        stage_stats[stage_label] = {
            'count': count,
            'percentage': 0  # 百分比由 ECharts 自动计算
        }

        # 保持销售流程顺序
        stage_stats_filled.append({
            'name': stage_label,
            'value': count
        })

    # 1.5. 严格漏斗统计（只统计实际填过该阶段的项目）
    stage_stats_strict = []
    for stage_value, stage_label in SALES_STAGE_CHOICES:
        # 统计实际进入过该阶段的项目数（不补齐）
        count = ProjectStageHistory.objects.filter(
            to_stage=stage_value,
            project__id__in=allowed_project_ids
        ).order_by().values('project').distinct().count()  # 清除默认排序以确保 distinct 正确工作

        stage_stats_strict.append({
            'name': stage_label,
            'value': count
        })

    # 2. 阶段转化率分析（双重统计：标准转化率 + 跳阶段分析）
    conversion_rates = []
    stages = [s[0] for s in SALES_STAGE_CHOICES]  # 使用阶段值（不是标签）
    stage_labels = [s[1] for s in SALES_STAGE_CHOICES]  # 阶段标签用于显示

    for i in range(len(stages) - 1):
        current_stage = stages[i]
        current_label = stage_labels[i]
        next_stage = stages[i + 1]
        next_label = stage_labels[i + 1]

        # 后续所有阶段（用于跳阶段统计）
        subsequent_stages = stages[i + 1:]
        skip_stages = stages[i + 2:] if i < len(stages) - 2 else []  # 跳过至少一个阶段

        # 1. 进入过该阶段的项目总数（方案B的分母）
        entered_current = ProjectStageHistory.objects.filter(
            to_stage=current_stage,
            project__id__in=allowed_project_ids
        ).order_by().values('project').distinct().count()  # 清除默认排序

        # 2. 已离开该阶段的项目总数（方案A的分母）
        left_current = ProjectStageHistory.objects.filter(
            from_stage=current_stage,
            project__id__in=allowed_project_ids
        ).order_by().values('project').distinct().count()  # 清除默认排序

        # 3. 标准转化：直接进入下一阶段的项目数
        direct_to_next = ProjectStageHistory.objects.filter(
            from_stage=current_stage,
            to_stage=next_stage,  # 只统计直接进入下一阶段
            project__id__in=allowed_project_ids
        ).order_by().values('project').distinct().count()  # 清除默认排序

        # 4. 跳阶段：跳过至少一个阶段直接到更后面的项目数
        skip_count = ProjectStageHistory.objects.filter(
            from_stage=current_stage,
            to_stage__in=skip_stages,  # 跳过至少一个阶段
            project__id__in=allowed_project_ids
        ).order_by().values('project').distinct().count() if skip_stages else 0  # 清除默认排序

        # 5. 总推进数（直接 + 跳阶段）
        total_progressed = direct_to_next + skip_count

        # 6. 计算双重转化率指标
        # 方案A：流程转化率（已离开该阶段的项目中，成功推进的比例）
        process_conversion_rate = round(
            total_progressed / left_current * 100, 1
        ) if left_current > 0 else 0

        # 方案B：整体推进率（所有进入该阶段的项目中，已推进的比例）
        overall_progression_rate = round(
            total_progressed / entered_current * 100, 1
        ) if entered_current > 0 else 0

        # 标准转化率（只算直接推进，不含跳阶段）
        standard_conversion_rate = round(
            direct_to_next / left_current * 100, 1
        ) if left_current > 0 else 0

        # 计算还在该阶段的项目数
        in_progress_count = entered_current - left_current

        # 计算跳填率（避免重复查询，整合到转化率计算中）
        subsequent_stages_for_skip = stages[i + 1:]
        if subsequent_stages_for_skip:
            # 到达后续阶段的所有项目
            reached_subsequent = ProjectStageHistory.objects.filter(
                to_stage__in=subsequent_stages_for_skip,
                project__id__in=allowed_project_ids
            ).order_by().values_list('project', flat=True).distinct()  # 清除默认排序

            reached_subsequent_set = set(reached_subsequent)

            # 实际填过当前阶段的项目
            filled_current_set = set(
                ProjectStageHistory.objects.filter(
                    to_stage=current_stage,
                    project__id__in=allowed_project_ids
                ).order_by().values_list('project', flat=True).distinct()  # 清除默认排序
            )

            # 跳过未填的项目数
            never_filled_count = len(reached_subsequent_set - filled_current_set)

            # 计算跳填率
            skip_fill_rate = round(
                never_filled_count / len(reached_subsequent_set) * 100, 1
            ) if reached_subsequent_set else 0
        else:
            never_filled_count = 0
            skip_fill_rate = 0

        conversion_rates.append({
            'from_stage': current_label,
            'to_stage': next_label,

            # 基础数据
            'entered_count': entered_current,  # 进入过该阶段的总数
            'left_count': left_current,  # 已离开该阶段的总数
            'in_progress_count': in_progress_count,  # 还在该阶段的项目数

            # 推进数据
            'direct_count': direct_to_next,  # 直接推进到下一阶段
            'skip_count': skip_count,  # 跳阶段推进
            'total_progressed': total_progressed,  # 总推进数

            # 双重转化率指标
            'process_conversion_rate': process_conversion_rate,  # 方案A：流程转化率（已完成项目的转化率）
            'overall_progression_rate': overall_progression_rate,  # 方案B：整体推进率（包括在途项目）
            'standard_conversion_rate': standard_conversion_rate,  # 标准转化率（只算直接推进）

            # 新增：跳填率数据（用于漏斗图标注）
            'skip_fill_rate': skip_fill_rate,  # 跳填率
            'never_filled_count': never_filled_count,  # 未填数量（用于tooltip）

            # 兼容旧字段（前端可能还在使用）
            'progressed_count': total_progressed,
            'conversion_rate': process_conversion_rate,  # 默认使用方案A
        })

    # 3. 各阶段平均停留时间（天数）- 改进版（包含中位数和样本量）
    stage_duration = {}
    stage_duration_analysis = []

    for i, (stage_value, stage_label) in enumerate(SALES_STAGE_CHOICES):
        # 查询所有从该阶段离开的记录的停留天数
        stage_records = ProjectStageHistory.objects.filter(
            from_stage=stage_value,
            project__id__in=allowed_project_ids
        ).values_list('days_in_previous_stage', flat=True)

        stage_records_list = list(stage_records)

        if stage_records_list:
            # 计算平均值和中位数
            import statistics
            avg_days = round(sum(stage_records_list) / len(stage_records_list), 1)
            median_days = round(statistics.median(stage_records_list), 1)
            sample_size = len(stage_records_list)

            # 从转化率数据中获取跳过率
            skip_rate = 0
            if i < len(conversion_rates):
                skip_rate = conversion_rates[i].get('skip_fill_rate', 0)
        else:
            avg_days = 0
            median_days = 0
            sample_size = 0
            skip_rate = 0

        # 保留旧格式（兼容性）
        stage_duration[stage_label] = avg_days

        # 新格式（增强数据）
        stage_duration_analysis.append({
            'stage': stage_label,
            'avg_days': avg_days,          # 平均值
            'median_days': median_days,    # 中位数（更准确，不受极端值影响）
            'sample_size': sample_size,    # 样本量（多少个项目实际经历了该阶段）
            'skip_rate': skip_rate,        # 跳过率（从转化率分析中获取）
        })

    # 3.5. 阶段跳填分析（新增）
    skip_fill_stats = []
    stages = [s[0] for s in SALES_STAGE_CHOICES]
    stage_labels = [s[1] for s in SALES_STAGE_CHOICES]

    for i in range(len(stages)):
        current_stage = stages[i]
        current_label = stage_labels[i]

        # 后续所有阶段
        subsequent_stages = stages[i + 1:]

        if not subsequent_stages:
            continue  # 最后一个阶段没有后续，跳过

        # 1. 到过后续阶段的项目（到达过N及以后）
        projects_reached_subsequent = list(
            ProjectStageHistory.objects.filter(
                to_stage__in=subsequent_stages,
                project__id__in=allowed_project_ids
            ).order_by().values_list('project', flat=True).distinct()  # 清除默认排序以确保 distinct 正确工作
        )

        reached_subsequent_count = len(projects_reached_subsequent)

        if reached_subsequent_count == 0:
            continue  # 没有项目到达后续阶段，跳过

        # 2. 到达过当前阶段的项目
        projects_reached_current = set(
            ProjectStageHistory.objects.filter(
                to_stage=current_stage,
                project__id__in=allowed_project_ids
            ).order_by().values_list('project', flat=True).distinct()  # 清除默认排序以确保 distinct 正确工作
        )

        # 3. 从未填过当前阶段，但到达了后续阶段的项目（跳填）
        never_filled_current = set(projects_reached_subsequent) - projects_reached_current
        never_filled_count = len(never_filled_current)

        # 4. 计算跳填比例
        skip_rate = round(never_filled_count / reached_subsequent_count * 100, 1)

        skip_fill_stats.append({
            'stage': current_label,
            'reached_subsequent_count': reached_subsequent_count,  # 到达后续阶段的项目数
            'never_filled_count': never_filled_count,  # 从未填过该阶段的项目数
            'filled_count': reached_subsequent_count - never_filled_count,  # 填过该阶段的项目数
            'skip_rate': skip_rate,  # 跳填比例
        })

    # 4. 项目状态分布
    status_distribution = queryset.values('status').annotate(
        count=Count('id')
    )
    status_stats = {item['status']: item['count'] for item in status_distribution}

    # 5. 月度新增项目趋势
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    monthly_new_projects = Project.objects.filter(
        createtime__gte=start_date,
        is_active=True
    ).annotate(
        month=TruncMonth('createtime')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    monthly_trend = [
        {
            'month': item['month'].strftime('%Y-%m'),
            'count': item['count']
        }
        for item in monthly_new_projects
    ]

    # 6. 赢单统计
    won_projects = queryset.filter(status='won')
    total_won_amount = won_projects.aggregate(
        total=Sum('actual_amount')  # 修复：使用实际成交金额而非预计金额
    )['total'] or 0

    return JsonResponse({
        # 新增字段
        'stage_stats_strict': stage_stats_strict,  # 严格漏斗统计（只统计实际填过的）
        'stage_stats_filled': stage_stats_filled,  # 补齐漏斗统计（到达后续算完成）

        # 保留兼容字段
        'stage_stats': stage_stats,  # 保留旧格式（兼容性）
        'stage_stats_ordered': stage_stats_filled,  # 保留旧字段名，映射到新字段

        # 现有字段（已增强，添加了跳填率）
        'conversion_rates': conversion_rates,  # 已添加 skip_fill_rate 和 never_filled_count
        'stage_duration': stage_duration,  # 保留旧格式（兼容性）
        'stage_duration_analysis': stage_duration_analysis,  # 新增：包含中位数、样本量、跳过率
        'skip_fill_stats': skip_fill_stats,  # 独立跳填分析
        'status_stats': status_stats,
        'monthly_trend': monthly_trend,
        'summary': {
            'total_projects': total_projects,
            'active_projects': queryset.filter(status='active').count(),
            'won_projects': won_projects.count(),
            'won_rate': round(won_projects.count() / total_projects * 100, 1) if total_projects > 0 else 0,
            'total_won_amount': float(total_won_amount),
        }
    })


@login_required
def salesman_performance_api(request):
    """销售人员业绩分析API（支持时间范围筛选）"""
    from .models import ReportUserInfo

    # 获取时间范围参数（与漏斗分析保持一致）
    days = int(request.GET.get('days', 90))
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # 获取所有销售人员（有项目的销售人员）
    salesmans = ReportUserInfo.objects.filter(
        Q(username__in=['jy', 'fzj', 'wh', 'zjm', 'gjb', 'gsj']) |
        Q(is_superuser=True)
    )

    performance_data = []

    for salesman in salesmans:
        # 时间范围内创建的项目
        projects = Project.objects.filter(
            salesman=salesman,
            is_active=True,
            createtime__gte=start_date
        )

        if projects.count() == 0:
            continue  # 跳过没有项目的销售人员

        won_projects = projects.filter(status='won')
        lost_projects = projects.filter(status='lost')
        active_projects = projects.filter(status='active')

        # 使用实际成交金额（actual_amount）而非预估金额
        total_won_amount = won_projects.aggregate(
            total=Sum('actual_amount')
        )['total'] or 0

        # 预估在途金额（活跃项目的预估金额）
        estimated_pipeline_amount = active_projects.aggregate(
            total=Sum('estimated_amount')
        )['total'] or 0

        performance_data.append({
            'salesman_id': salesman.id,
            'salesman_name': salesman.chinesename or salesman.username,
            'total_projects': projects.count(),
            'active_projects': active_projects.count(),
            'won_projects': won_projects.count(),
            'lost_projects': lost_projects.count(),
            'won_rate': round(
                won_projects.count() / projects.count() * 100, 1
            ) if projects.count() > 0 else 0,
            'total_won_amount': float(total_won_amount),
            'estimated_pipeline_amount': float(estimated_pipeline_amount),
            'avg_won_amount': float(total_won_amount / won_projects.count()) if won_projects.count() > 0 else 0,
        })

    # 按赢单金额排序
    performance_data.sort(key=lambda x: x['total_won_amount'], reverse=True)

    return JsonResponse({
        'performance_data': performance_data,
        'time_range': {
            'days': days,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
        }
    })
