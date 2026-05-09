import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plugin_accessibility.settings')

application = get_wsgi_application()
