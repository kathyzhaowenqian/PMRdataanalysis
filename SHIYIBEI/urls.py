from django.urls import path
from SHIYIBEI.views import *

urlpatterns = [
    # path('uploads', Upload.as_view()),
    # path('downloads', Download.as_view()),
    path('uploads2', Upload2.as_view()),
    path('downloads2', Download2.as_view()),

]

