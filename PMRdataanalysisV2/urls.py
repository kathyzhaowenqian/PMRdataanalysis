"""PMRdataanalysisV2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import RedirectView
favicon_view = RedirectView.as_view(url='/static/pmr/images/favicon.ico',permanent=True)
mainsite_view=RedirectView.as_view(url='admin/',permanent=True)
 

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('_nested_admin/', include('nested_admin.urls')),
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


 