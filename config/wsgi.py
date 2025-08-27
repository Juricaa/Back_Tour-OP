"""
WSGI config for bzkRestApisMySQL project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application


# Chemin vers votre virtualenv
VIRTUALENV_PATH = 'C:/xampp/htdocs/TourOp/backend/venv'

# Chemin vers votre projet Django
PROJECT_PATH = 'C:/xampp/htdocs/TourOp/backend'

# Ajout du virtualenv au path Python
activate_this = os.path.join(VIRTUALENV_PATH, 'Scripts', 'activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Ajout du projet au path Python
sys.path.append(PROJECT_PATH)






os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()