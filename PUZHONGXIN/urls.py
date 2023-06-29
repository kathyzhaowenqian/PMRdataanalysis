from django.urls import path
from PUZHONGXIN.views import *

urlpatterns = [
    path('gantt',PZXgantt.as_view()),
]


