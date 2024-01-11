from django.urls import path
from Suppliers.views import *

urlpatterns = [
    path('uploads_xey_23', Uploads_XEY_23.as_view()),
    path('uploads_xey_24', Uploads_XEY_24.as_view()),
    path('downloads_xey', Downloads_XEY.as_view()),
    
    path('uploads_nq_23', Uploads_NQ_23.as_view()),
    path('uploads_nq_24', Uploads_NQ_24.as_view()),
    path('downloads_nq', Downloads_NQ.as_view()),

    path('uploads_pzx_23', Uploads_PZX_23.as_view()),
    path('uploads_pzx_24', Uploads_PZX_24.as_view()),
    path('downloads_pzx', Downloads_PZX.as_view()),
    #新沂
    path('uploads_xinyi_23', Uploads_XINYI_23.as_view()),
    path('uploads_xinyi_24', Uploads_XINYI_24.as_view()),
    path('downloads_xinyi', Downloads_XINYI.as_view()),
    #邳州
    path('uploads_pizhou_23', Uploads_PIZHOU_23.as_view()),
    path('uploads_pizhou_24', Uploads_PIZHOU_24.as_view()),
    path('downloads_pizhou', Downloads_PIZHOU.as_view()),
    #安亭
    path('uploads_anting_23', Uploads_ANTING_23.as_view()),
    path('uploads_anting_24', Uploads_ANTING_24.as_view()),
    path('downloads_anting', Downloads_ANTING.as_view()),
    #南翔
    path('uploads_nanxiang_23', Uploads_NANXIANG_23.as_view()),
    path('uploads_nanxiang_24', Uploads_NANXIANG_24.as_view()),
    path('downloads_nanxiang', Downloads_NANXIANG.as_view()),

    #齐贤
    path('uploads_qixian_23', Uploads_QIXIAN_23.as_view()),
    path('uploads_qixian_24', Uploads_QIXIAN_24.as_view()),
    path('downloads_qixian', Downloads_QIXIAN.as_view()),
    #申养
    path('uploads_shenyang_23', Uploads_SHENYANG_23.as_view()),
    path('uploads_shenyang_24', Uploads_SHENYANG_24.as_view()),
    path('downloads_shenyang', Downloads_SHENYANG.as_view()),
    #四团
    path('uploads_situan_23', Uploads_SITUAN_23.as_view()),
    path('uploads_situan_24', Uploads_SITUAN_24.as_view()),
    path('downloads_situan', Downloads_SITUAN.as_view()),
    #四五五
    path('uploads_siwuwu_23', Uploads_SIWUWU_23.as_view()),
    path('uploads_siwuwu_24', Uploads_SIWUWU_24.as_view()),
    path('downloads_siwuwu', Downloads_SIWUWU.as_view()),
    #亭林
    path('uploads_tinglin_23', Uploads_TINGLIN_23.as_view()),
    path('uploads_tinglin_24', Uploads_TINGLIN_24.as_view()),
    path('downloads_tinglin', Downloads_TINGLIN.as_view()),
    #西渡
    path('uploads_xidu_23', Uploads_XIDU_23.as_view()),
    path('uploads_xidu_24', Uploads_XIDU_24.as_view()),
    path('downloads_xidu', Downloads_XIDU.as_view()),
    #直销
    path('uploads_zhixiao_23', Uploads_ZHIXIAO_23.as_view()),
    path('uploads_zhixiao_24', Uploads_ZHIXIAO_24.as_view()),
    path('downloads_zhixiao', Downloads_ZHIXIAO.as_view()),
]