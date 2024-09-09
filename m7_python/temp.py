
#! -> se ejecuta con --> python m7_python/temp.py <-- corre con
import os
import django
from dotenv import load_dotenv
load_dotenv()

import sys
# # Asegúrate de que el directorio del proyecto esté en el PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Me entrega el path del project -> ... ~/OneDrive/Escritorio/Curso practico/MODULO 7/DIA_7/mysite1

import mysite1

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite1.settings")
django.setup()

from m7_python.models import Inmueble, Region, Comuna
from django.contrib.auth.models import User

#TODO_ Ejemplos SIMPLES:
def get_list_inmuebles_sql():
    select = """
        SELECT * FROM m7_python_inmueble
        """
    inmuebles = Inmueble.objects.raw(select)
    # inmuebles = Inmueble.objects.all()     <- ORM
    index=1
    print("LISTA INMUEBLES")
    for l in inmuebles:
        print(f"{index}__ {l.nombre}, {l.descripcion}")
        index += 1
    with open("m7_python/outputs/datos.txt", "a") as file:
        for l in inmuebles:
            # print(f" {l.nombre}, {l.descripcion}")
            file.write(f" {l.nombre}, {l.descripcion}\n")
                
    return

"""
Consultar listado de inmuebles para arriendo separado por comunas, solo usando los 
campos "nombre" y "descripción" en un script python que se conecta a la DB usando 
DJango y SQL guardando los resultados en un archivo de texto.
"""
def listado_inmuebles_comuna_orm(comuna, descr=None):
    # inmuebles = Inmueble.objects.all()
    # comuna__nombre__icontains
    # Guardar la data en nuestro .txt con nuestro OPEN de python
    
    # inmuebles = Inmueble.objects.filter(comuna__nombre__icontains=comuna)
    # print(f'--> {inmuebles}')
    
    filtros = {
            'comuna__nombre__icontains': comuna
    }
    if descr:
        filtros['descripcion__icontains'] = descr
        
    inmuebles = Inmueble.objects.filter(**filtros)
       
    with open("m7_python/outputs/datos.txt", "a") as file:
        file.write(f'__ listado_inmuebles_comuna_orm __\n')
        for l in inmuebles:
            file.write(f"{l.nombre}, {l.descripcion} - comuna: {l.comuna.nombre}\n")
    return

def listado_inmuebles_comuna_sql(comuna):
    select = """
    SELECT A.id, A.nombre AS nombre_inmueble, A.descripcion
    FROM m7_python_inmueble A
    INNER JOIN m7_python_comuna C ON A.comuna_id = C.cod
    WHERE C.nombre ILIKE %s
    """
    inmuebles = Inmueble.objects.raw(select, [f"%{comuna}%"])
    # Guardar la data en nuestro .txt con nuestro OPEN de python
    with open("m7_python/outputs/datos.txt", "a") as file:
        file.write(f'\n __ listado_inmuebles_comuna_sql __\n')
        for l in inmuebles:
            file.write(f"{l.nombre}, {l.descripcion} - comuna: {l.comuna.nombre}\n")
    return

"""
Consultar listado de inmuebles para arriendo separado por regiones en un script python 
que se conecta a la DB usando DJango y SQL guardando los resultados en un archivo de texto
"""

def listado_inmuebles_region_orm(region):
    inmuebles = Inmueble.objects.filter(comuna__region__nombre__icontains=region)
    with open("m7_python/outputs/datos.txt", "a") as file:
        file.write(f'\n__ listado_inmuebles_region_orm __\n')
        for l in inmuebles:
            file.write(f"{l.nombre}, {l.descripcion} - region: {l.comuna.region.nombre}\n")
    return


def listado_inmuebles_region_sql(region):
    select = """
    SELECT A.id, A.nombre AS nombre_inmueble, A.descripcion
    FROM m7_python_inmueble A
    INNER JOIN m7_python_comuna C ON A.comuna_id = C.cod
    INNER JOIN m7_python_region B ON C.region_id = B.cod
    WHERE B.nombre ILIKE %s
    """
    inmuebles = Inmueble.objects.raw(select, [f"%{region}%"])
    with open("m7_python/outputs/datos.txt", "a") as file:
        file.write(f'\n __ listado_inmuebles_region_sql __\n')
        for l in inmuebles:
            file.write(f"{l.nombre}, {l.descripcion} - region: {l.comuna.region.nombre}\n")
    return


# Ejecución de funciones de ejemplo
if __name__ == "__main__":
    #TODO_ Ejemplos SIMPLES:
    # get_list_inmuebles_sql()
    listado_inmuebles_comuna_orm("Santiago")
    listado_inmuebles_comuna_sql("Providencia")
    listado_inmuebles_region_orm("De Valparaíso")
    listado_inmuebles_region_sql("De Los Rios")