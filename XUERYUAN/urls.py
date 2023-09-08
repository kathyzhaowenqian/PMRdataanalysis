from django.urls import path
from XUERYUAN.views import *

urlpatterns = [
    path('gantt',XEYgantt.as_view()),
]


