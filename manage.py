#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys




def main():
    """Run administrative tasks."""
    # 开发环境启动的settings
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PMRdataanalysisV2.local_settings')
    # 生成境启动的settings 
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PMRdataanalysisV2.production_settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


#333333

if __name__ == '__main__':
    main()
