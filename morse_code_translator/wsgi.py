import os
import sys

# Add your project directory to the sys.path
project_home = '/home/maheedhargowd/morsecode_translator__'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set the DJANGO_SETTINGS_MODULE environment variable to point to your settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'morse_code_translator.settings'

# Import Django's get_wsgi_application and set the application variable
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
