from django.urls import path
from Marketing_Research_QT.views import *

urlpatterns = [
    path('qtanalysis',QTANALYSIS.as_view()),
    path('qtanalysisdetail',QTANALYSISDETAIL.as_view()),
]
