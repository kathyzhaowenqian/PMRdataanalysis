from django.urls import path
from Marketing_Research.views import *

urlpatterns = [
    path('pmranalysis',PMRANALYSIS.as_view()),
    path('pmranalysisdetail',PMRANALYSISDETAIL.as_view()),
]


