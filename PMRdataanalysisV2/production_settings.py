"""
Django settings for PMRdataanalysisV2 project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'Marketing_Research',
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'Marketing_Research_WD',
    'Marketing_Research_QT',
    'Marketing_Research_JC',
    'Marketing_Research_ZS',
    'PMR_U8_001',
    'PMR_U8_009',
    'PMR_U8_010',
    'PMR_U8_011',
    'PMR_U8_012',
    'import_export',
    'Marketing_Research_Community',
    'PUZHONGXIN',
    'SIWUWU',
    'ANTING',
    'NANXIANG',
    'nested_admin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PMRdataanalysisV2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PMRdataanalysisV2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {

    #'default':{},
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRESQL_INTERNAL_DBNAME'),
        'USER': os.environ.get('POSTGRESQL_INTERNAL_USERNAME'),
        'PASSWORD': os.environ.get('POSTGRESQL_INTERNAL_PASSWORD'),
        'HOST': os.environ.get('POSTGRESQL_INTERNAL_HOST'), 
        'PORT': os.environ.get('POSTGRESQL_INTERNAL_PORT'),
        'OPTIONS': {
            'options': '-c search_path="django_admin_v2","marketing_research_v2","PMR_U8_001","PMR_U8_009","PMR_U8_010","PMR_U8_011","PMR_U8_012"'
        }
    },
}

CACHES = {
		"default": {
 					"BACKEND": "django_redis.cache.RedisCache",
 					"LOCATION": "redis://{}:{}/2".format(os.environ.get('REDIS_INTERNAL_HOST'),os.environ.get('REDIS_INTERNAL_PORT')),		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!数字代表使用redis哪个数据库
 								"OPTIONS": 
            				  {
								 "CLIENT_CLASS": "django_redis.client.DefaultClient",
 								  "PASSWORD": os.environ.get('REDIS_PASSWORD'),
                                }
					}
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = ['Marketing_Research/static/','PUZHONGXIN/static/']




# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




AUTH_USER_MODEL = 'Marketing_Research.UserInfo'


SIMPLEUI_ANALYSIS = False

SIMPLEUI_HOME_PAGE ='https://data.bio-merry.com:8087/login/'
SIMPLEUI_HOME_TITLE = 'Superset BI 数据看板'
SIMPLEUI_HOME_ICON = 'fa-sharp fa-solid fa-chart-simple'

SIMPLEUI_CONFIG = {
    'system_keep': True,
     # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
    'menu_display': ['普美瑞直销调研表','其田直销调研表','卫顿直销调研表','国赛美瑞调研表','百来社区医院调研表','集成调研表','集成战略地图/作战计划','用友-U8-同步','认证授权'],  
    'dynamic': True,    # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    'menus': [

        #一级菜单：普美瑞直销调研表
        {
            'name': '普美瑞直销调研表',
            'icon': 'fa-solid fa-star',
            'models': [
                {
                # 第二级菜单                
                'name': '调研表列表(在此填报)',
                'url': '/admin/Marketing_Research/pmrresearchlist/',
                'icon': 'fa-solid fa-pen'
                }, 
                {
                'name': '调研表仪器详情表',
                'icon': 'fa-solid fa-list',
                'url': '/admin/Marketing_Research/pmrresearchdetail/'
                },
                {
                'name': '普美瑞调研数据分析',
                'icon': 'fa-solid fa-list',
                'url': '/Marketing_Research/pmranalysis'
                },
                {
                'name': '普美瑞已删除的数据',
                'icon': 'fa-solid fa-list',
                'url': '/admin/Marketing_Research/pmrresearchlistdelete/'
                },

            ] 
        },

        #一级菜单：其田直销调研表
        {
            'name': '其田直销调研表',
            'icon': 'fa-solid fa-star',
            'models': [
                {
                # 第二级菜单                
                'name': '调研表列表(在此填报)',
                'url': '/admin/Marketing_Research_QT/pmrresearchlist3/',
                'icon': 'fa-solid fa-pen'
                }, 
                {
                'name': '调研表仪器详情表',
                'icon': 'fa-solid fa-list',
                'url': '/admin/Marketing_Research_QT/pmrresearchdetail3/'
                },
                {
                'name': '其田调研数据分析',
                'icon': 'fa-solid fa-list',
                'url': '/Marketing_Research_QT/qtanalysis'
                },
                {
                'name': '其田已删除的数据',
                'icon': 'fa-solid fa-list',
                'url': '/admin/Marketing_Research_QT/pmrresearchlist3delete/'
                },                        
            ]        
        },

        #一级菜单：卫顿直销调研表
        {
            'name': '卫顿直销调研表',
            'icon': 'fa-solid fa-star',
            'models': [
                {
                # 第二级菜单                
                'name': '调研表列表(在此填报)',
                'url': '/admin/Marketing_Research_WD/pmrresearchlist2/',
                'icon': 'fa-solid fa-pen'
                }, 
                {
                'name': '调研表仪器详情表',
                'icon': 'fa-solid fa-list',
                'url': '/admin/Marketing_Research_WD/pmrresearchdetail2/'
                } ,
                {
                'name': '卫顿调研数据分析',
                'icon': 'fa-solid fa-list',
                'url': '/Marketing_Research_WD/wdanalysis'
                },
                {
                'name': '卫顿已删除的数据',
                'icon': 'fa-solid fa-list',
                'url': '/admin/Marketing_Research_WD/pmrresearchlist2delete/'
                },                       
            ]        
        },
        
        #一级菜单：国赛美瑞直销调研表
        {
            'name': '国赛美瑞调研表',
            'icon': 'fa-solid fa-star',
            'models': [
                {
                # 第二级菜单                
                'name': '调研表列表(在此填报)',
                'url': '/admin/Marketing_Research_ZS/gsmrresearchlist/',
                'icon': 'fa-solid fa-pen'
                }, 
                {
                'name': '调研表仪器详情表',
                'icon': 'fa-solid fa-list',
                'url': '/admin/Marketing_Research_ZS/gsmrresearchdetail/'
                },
                {
                'name': '国赛美瑞已删除的数据',
                'icon': 'fa-solid fa-list',
                'url': '/admin/Marketing_Research_ZS/gsmrresearchlistdelete/'
                },                        
             ]        
        },

        #一级菜单：百来调研表
        {
            'name': '百来社区医院调研表',
            'icon': 'fa-solid fa-star',
            'models': [
                {
                # 第二级菜单                
                'name': '调研表列表(在此填报)',
                'url': '/admin/Marketing_Research_Community/communityresearchlist/',
                'icon': 'fa-solid fa-pen'
                }, 
                {
                'name': '调研表仪器详情表',
                'icon': 'fa-solid fa-list',
                'url': '/admin/Marketing_Research_Community/communityresearchdetail/'
                },
                {
                'name': '已删除的数据',
                'icon': 'fa-solid fa-list',
                'url': '/admin/Marketing_Research_Community/communityresearchlistdelete/'
                },                        
             ]        
        },


        #一级菜单：集成调研表
        {
            'name': '集成调研表',
            'icon': 'fa-solid fa-star',
            'models': [
                {
                # 第二级菜单                
                'name': '调研表列表(在此填报)',
                'url': '/admin/Marketing_Research_JC/jcresearchlist/',
                'icon': 'fa-solid fa-pen'
                }, 
                                 
            ]        
        },
        
        #一级菜单：集成战略地图/作战计划
        {
            'name': '集成战略地图/作战计划',
            'icon': 'fa-solid fa-star',
            'models': [
                #二级菜单：普中心
                {
                    'name': '普中心',
                    'icon': 'fab fa-github',
                    'models': [
                        #三级菜单：普中心战略地图                      
                            {
                            'name': '普中心战略地图(销售的excel)',
                            'url': '/admin/PUZHONGXIN/pzxspdlist/'
                            },      
                        #三级菜单：普中心作战计划                      
                            {
                            'name': '普中心作战计划(在此填报)',
                            'url': '/admin/PUZHONGXIN/pzxoverall/'
                            },           
                        #三级菜单：普中心甘特图                     
                            {
                            'name': '普中心进度甘特图',
                            'url': '/PUZHONGXIN/gantt'
                            },  
                        #三级菜单：普中心新开项目明细                     
                            {
                            'name': '普中心新开项目明细',
                            'url': '/admin/PUZHONGXIN/pzxnewprojectdetail/'
                            },         
                            #三级菜单：普中心供应商重新谈判明细                     
                            {
                            'name': '普中心供应商重新谈判明细',
                            'url': '/admin/PUZHONGXIN/pzxnegotiationdetail/'
                            },        
                            #三级菜单：普中心渠道变更明细                     
                            {
                            'name': '普中心渠道变更明细',
                            'url': '/admin/PUZHONGXIN/pzxchangechanneldetail/'
                            },    
                            #三级菜单：普中心品牌替换后明细                     
                            {
                            'name': '普中心品牌替换后明细',
                            'url': '/admin/PUZHONGXIN/pzxafterchangebranddetail/'
                            },   
                            #三级菜单：普中心套餐绑定明细                     
                            {
                            'name': '普中心套餐绑定明细',
                            'url': '/admin/PUZHONGXIN/pzxsetdetail/'
                            },   
                            #三级菜单：普中心作战计划已删除的数据  
                            {
                            'name': '普中心作战计划已删除的数据',
                            'icon': 'fa-solid fa-list',
                            'url': '/admin/PUZHONGXIN/pzxoveralldelete/'
                            },
                    ]                
                } ,
                
                #二级菜单：四五五
                {
                    'name': '四五五',
                    'icon': 'fab fa-github',
                    'models': [

                        #三级菜单：四五五战略地图                      
                            {
                            'name': '四五五战略地图',
                            'url': '/admin/SIWUWU/swwspdlist/'
                            },                        
                    ]                
                } ,

                #二级菜单：安亭
                {
                    'name': '安亭',
                    'icon': 'fab fa-github',
                    'models': [

                        #三级菜单：安亭战略地图                      
                            {
                            'name': '安亭战略地图',
                            'url': '/admin/ANTING/atspdlist/'
                            },                        
                    ]                
                } ,


                #二级菜单：南翔
                {
                    'name': '南翔',
                    'icon': 'fab fa-github',
                    'models': [

                        #三级菜单：南翔战略地图                      
                            {
                            'name': '南翔战略地图',
                            'url': '/admin/NANXIANG/nxspdlist/'
                            },                        
                    ]                
                } ,                                 
            ]        
        },

        #一级菜单：用友-U8-同步
        {
            'name': '用友-U8-同步',
            'icon': 'fab fa-github',
            'models': [

                #二级菜单：PMR_U8_001
                {
                    'name': '用友-普美瑞-U8-001',
                    'icon': 'fab fa-github',
                    'models': [
                        {
                        'name': '发货单',
                        'url': '/admin/PMR_U8_001/consignments/'
                        }, 
                    ]                
                } ,

                #二级菜单：PMR_U8_009
                {
                    'name': '用友-盈帅-U8-009',
                    'icon': 'fab fa-github',
                    'models': [
                        {
                        'name': '发货单',
                        'url': '/admin/PMR_U8_009/consignments/'
                        }, 
                    ]                
                } ,

                #二级菜单：PMR_U8_010
                {
                    'name': '用友-国赛美瑞-U8-010',
                    'icon': 'fab fa-github',
                    'models': [
                        {
                        'name': '发货单',
                        'url': '/admin/PMR_U8_010/consignments/'
                        },          
                    ]        
                },  
                #二级菜单：PMR_U8_011
                {
                    'name': '用友-其田-U8-011',
                    'icon': 'fab fa-github',
                    'models': [
                        {
                        'name': '发货单',
                        'url': '/admin/PMR_U8_011/consignments/'
                        },          
                    ]        
                },  
                #二级菜单：PMR_U8_012
                {
                    'name': '用友-卫顿-U8-012',
                    'icon': 'fab fa-github',
                    'models': [
                        {
                        'name': '发货单',
                        'url': '/admin/PMR_U8_012/consignments/'
                        },          
                    ]        
                },  

            ]        
        },
            
        #一级菜单：人员
        {
            'name': '认证授权',
            'icon': 'fab fa-github',
            'models': [
                {
                # 第二级菜单                
                'name': '用户',
                'url': '/admin/Marketing_Research/userinfo/',
                'icon': 'far fa-surprise'
                }, 
                {
                'name': '组',
                'icon': 'far fa-surprise',
                'url': '/admin/auth/group/'
                }                        
            ]        
        },

        ]
    }



STATIC_ROOT = '/djangostatic'

#可以展示的时间 。 
MARKETING_RESEARCH_TARGET_AUTO_ADVANCED_DAYS = 30
MARKETING_RESEARCH_TARGET_AUTO_DELAYED_DAYS = 30


SIMPLEUI_LOGO = '/static/pmr/images/logo.png'

SESSION_COOKIE_AGE = 21600 