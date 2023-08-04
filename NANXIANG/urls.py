from django.urls import path
from NANXIANG.views import *

urlpatterns = [
    path('gantt',NXgantt.as_view()),
]


