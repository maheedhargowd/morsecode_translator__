import os
import sys

# Activate the virtual environment (this line should be commented out locally if not needed)
activate_this = '/home/maheedhargowd/.virtualenvs/myenv/bin/activate_this.py'
if os.path.exists(activate_this):
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

path = '/home/maheedhargowd/morsecode_translator__'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'morse_code_translator.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
