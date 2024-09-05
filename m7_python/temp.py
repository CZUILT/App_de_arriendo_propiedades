import os
import django
from dotenv import load_dotenv
load_dotenv()

import sys
# # Asegúrate de que el directorio del proyecto esté en el PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# -> .../OneDrive/Escritorio/DJANGO-PY 2024/MODULOS/MODULO-7/HITO2 
import mysite1

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite1.settings")
django.setup()

from m7_python.models import Inmueble, Region, Comuna
from django.contrib.auth.models import User

#ToDo: Ejemplo simple
def get_list_inmuebles_sql():
    pass