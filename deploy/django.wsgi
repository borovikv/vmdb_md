# -*- coding: utf-8 -*-
import os, sys

# В python path добавляется директория проекта
dn = os.path.dirname
PROJECT_ROOT = os.path.abspath( dn(dn(__file__)) + '/src' ) 
if PROJECT_ROOT not in sys.path:
	sys.path.append( PROJECT_ROOT )

# Установка файла настроек
project_name = 'varodb'
os.environ["DJANGO_SETTINGS_MODULE"] = project_name + ".settings"

#f = open('/home/drifter/development/testfile', 'w+')
#f.write('------------------')
#for p in sys.path:
#	f.writelines(p)
#	f.write("\n")
# Запуск wsgi-обработчика
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
