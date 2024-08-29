from django.urls import path
from SALESREPORT.views import *

urlpatterns = [
 
    path('reportsubmit', Submit.as_view()),
 
]