from django.urls import path
from Marketing_Research_ZS.views import *

urlpatterns = [
    path('gantt',ZSgantt.as_view()),
]
