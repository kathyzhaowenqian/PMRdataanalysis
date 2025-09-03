from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from .models import InstrumentModel, Brand
import logging

logger = logging.getLogger(__name__)

@staff_member_required
@require_http_methods(["GET"])
def get_models_by_brand(request):
    logger.info("get_models_by_brand view called")
    
    brand_id = request.GET.get('brand_id')
    logger.info(f"Brand ID: {brand_id}")
    
    if brand_id:
        try:
            brand_id = int(brand_id)
            
            # 检查是否有这个品牌
            if not Brand.objects.filter(id=brand_id, is_active=True).exists():
                logger.warning(f"Brand {brand_id} not found or inactive")
                return JsonResponse([], safe=False)
            
            # 获取型号列表
            models = InstrumentModel.objects.filter(
                brand_id=brand_id, 
                is_active=True
            ).values('id', 'model_name').order_by('model_name')
            
            result = [
                {'id': model['id'], 'name': model['model_name']} 
                for model in models
            ]
            
            logger.info(f"Returning {len(result)} models")
            return JsonResponse(result, safe=False)
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error processing brand_id {brand_id}: {e}")
            return JsonResponse([], safe=False)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse([], safe=False)
    
    return JsonResponse([], safe=False)

 