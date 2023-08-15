from django.urls import path
from XINYI.views import *

urlpatterns = [
    path('gantt',XYgantt.as_view()),
]


