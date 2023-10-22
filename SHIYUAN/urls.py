from django.urls import path
from SHIYUAN.views import *

urlpatterns = [
    path('uploads', Upload.as_view()),
    path('downloads', Download.as_view()),
]

