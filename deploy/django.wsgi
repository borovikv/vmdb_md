# -*- coding: utf-8 -*-
import os, sys

# В python path добавляется директория проекта
dn = os.path.dirname
PROJECT_ROOT = os.path.abspath( dn(dn(__file__)) ) 

if PROJECT_ROOT not in sys.path:
	sys.path.append( PROJECT_ROOT )

# Установка файла настроек
project_name = 'vmdb_md'
os.environ["DJANGO_SETTINGS_MODULE"] = project_name + ".settings"

# Запуск wsgi-обработчика
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
