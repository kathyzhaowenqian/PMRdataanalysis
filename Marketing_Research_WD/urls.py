from django.urls import path
from Marketing_Research_WD.views import *

urlpatterns = [
    path('wdanalysis',WDANALYSIS.as_view()),
    path('wdanalysisdetail',WDANALYSISDETAIL.as_view()),
]
