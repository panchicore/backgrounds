import os, sys
from os.path import abspath, dirname, join

import site
site.addsitedir('/home/<user>/.venvs/<backgrounds>/lib/python2.6/site-packages')


sys.path.insert(0, abspath(join(dirname(__file__), "..", "..")))
sys.path.insert(0, abspath(join(dirname(__file__), "..")))


os.environ['DJANGO_SETTINGS_MODULE'] = 'backgrounds.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
