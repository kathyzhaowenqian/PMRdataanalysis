from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import RedirectView
favicon_view = RedirectView.as_view(url='/static/pmr/images/favicon.ico',permanent=True)
mainsite_view=RedirectView.as_view(url='admin/',permanent=True)
 
from Mindray_Research.views import get_models_by_brand  

urlpatterns = [
    path('admin/get_models_by_brand/', get_models_by_brand, name='get_models_by_brand'),

    path('_nested_admin/', include('nested_admin.urls')),
    path('admin/', admin.site.urls),


    # path('chaining/', include('smart_selects.urls')),


    path('', mainsite_view),
    path('Marketing_Research/',include('Marketing_Research.urls')),
    path('Marketing_Research_QT/',include('Marketing_Research_QT.urls')),
    path('Marketing_Research_WD/',include('Marketing_Research_WD.urls')),
    path('PUZHONGXIN/',include('PUZHONGXIN.urls')),
    path('Marketing_Research_ZS/',include('Marketing_Research_ZS.urls')),
    path('ANTING/',include('ANTING.urls')),
    path('NANXIANG/',include('NANXIANG.urls')),
    path('XINYI/',include('XINYI.urls')),
    path('XUERYUAN/',include('XUERYUAN.urls')),
    # path('PIZHOU/',include('PIZHOU.urls')),
    path('SHIYUAN/',include('SHIYUAN.urls')),
    path('GONGWEI/',include('GONGWEI.urls')),

    path('SHIYIBEI/',include('SHIYIBEI.urls')),
    path('SHIYINAN/',include('SHIYINAN.urls')),
    path('Suppliers/',include('Suppliers.urls')),
    path('SALESREPORT/',include('SALESREPORT.urls')),

    path('favicon.ico', favicon_view)
]


 