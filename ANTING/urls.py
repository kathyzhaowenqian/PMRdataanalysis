from django.urls import path
from ANTING.views import *

urlpatterns = [
    path('gantt',ATgantt.as_view()),
]


