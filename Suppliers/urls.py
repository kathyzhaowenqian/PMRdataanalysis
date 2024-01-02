from django.urls import path
from Suppliers.views import *

urlpatterns = [
    path('uploads_xey_23', Uploads_XEY_23.as_view()),
    path('uploads_xey_24', Uploads_XEY_24.as_view()),
    path('downloads_xey', Downloads_XEY.as_view()),
]