# from django.shortcuts import render

# # Create your views here.
# from django.http import JsonResponse
# from django.contrib.admin.views.decorators import staff_member_required
# from .models import *
# @staff_member_required
# def get_blood_instruments(request):
    # hospital_survey_id = request.GET.get('hospital_survey_id')
    # if hospital_survey_id:
    #     instruments = MindrayInstrumentSurvey.objects.filter(
    #         hospital_survey_id=hospital_survey_id,
    #         category__name='血球',
    #         is_active=True
    #     ).values('id', 'model', 'brand__brand')
        
    #     data = []
    #     for inst in instruments:
    #         text = f"{inst['brand__brand'] or '未知品牌'} {inst['model'] or '未知型号'}"
    #         data.append({
    #             'id': inst['id'],
    #             'text': text
    #         })
        
    #     return JsonResponse(data, safe=False)
    
    # return JsonResponse([], safe=False)