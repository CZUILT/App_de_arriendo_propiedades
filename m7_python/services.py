from.models import Inmueble, Comuna, User, Region, UserProfile


def get_or_create_user_profile(user):
    try:
        # Intenta obtener el perfil del usuario o crearlo si no existe
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            print("Se ha creado un nuevo perfil para el usuario.")
        else:
            print("El perfil ya existía.")
        return user_profile
    except Exception as e:
        print(f'Error al obtener o crear el perfil del usuario. {e}')
        return None


def create_user(new_user):
    user = User.objects.create_user(
        username = new_user['username'],
        email = new_user['email'],
        first_name = new_user['first_name'],
        last_name = new_user['last_name'],
        password = new_user['password']
    )
    return user

def create_user_by_params(username,email,first_name,last_name,password):
    user = User.objects.create_user(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password
    )
    return user

def create_region(cod, nombre):
   region = Region.objects.create(
       cod = cod,
       nombre = nombre
   )

def create_comuna(cod, nombre, region_cod):
    region = Region.objects.get(cod = region_cod)
    comuna = Comuna.objects.create(
        cod = cod,
        nombre = nombre,
        region = region
    )

def insertar_inmueble(data):
    # Obtiene el usuario (arrendador) por ID
    arrendador = User.objects.get(id=data['id_user'])
    # Obtiene la comuna por código (cod)
    comuna = Comuna.objects.get(cod=data['comuna_cod'])
    # Crear un nuevo Inmueble usando los datos proporcionados
    inmueble = Inmueble(
        arrendador = arrendador,
        tipo_inmueble = data['tipo_inmueble'],
        comuna = comuna,
        nombre = data['nombre'],
        descripcion = data['descripcion'],
        m2_construidos = data['m2_construidos'],
        m2_totales = data['m2_totales'],
        num_baños = data['num_baños'],
        num_habitaciones = data['num_habitaciones'],
        num_estacionamientos = data.get('num_estacionamientos', 0),
        direccion = data['direccion'],
        precio = data.get('precio', None),
        precio_ufs = data.get('precio_ufs', None)
    )
    inmueble.save()
    return inmueble

def get_all_inmuebles():
    inmuebles = Inmueble.objects.all()
    return inmuebles


def actualizar_disponibilidad_inmueble(id_inmueble, disponible):
    """
    Actualiza la disponibilidad de un inmueble existente.
    Parámetros:
        id_inmueble (int): ID del inmueble a actualizar.
        disponible (bool): Nueva disponibilidad para el inmueble.
    Retorna:
        dict: Resultado de la operación con un mensaje de éxito o error.
    """
    try:
        inmueble = Inmueble.objects.get(pk=id_inmueble)  # Buscar el inmueble por ID
        # Actualizar la disponibilidad
        inmueble.disponible = disponible
        # inmueble.direccion = direccion
        # inmueble.descripcion = descripcion
        
        inmueble.save()  # Guardar los cambios
        return {
            "success": True,
            "message": "Disponibilidad actualizada con éxito"
        }
    except Inmueble.DoesNotExist:
        return {
            "success": False,
            "message": "Inmueble no encontrado"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error al actualizar la disponibilidad del inmueble: {str(e)}"
        }

def eliminar_inmueble(id_inmueble):
    try:
        inmueble = Inmueble.objects.get(pk=id_inmueble)  # Buscar el inmueble por ID
        inmueble.delete()
        return {
            "success": True,
            "message": "El inmueble ha sido eliminado con éxito"
        }
    except Inmueble.DoesNotExist:
        return {
            "success": False,
            "message": "El inmueble no ha sido encontrado"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error al eliminar el inmueble: {str(e)}"
        }


def get_inmuebles_for_arrendador(user):
    rol = user.user_profile.rol
    if rol != 'arrendador':
        print(f'Usuario no es arrendador')
        return []
    inmuebles = Inmueble.objects.filter(arrendador = user)
    if not inmuebles.exists():
        print(f'No hay inmuebles disponibles')
        return []
    return inmuebles


















# van nuestros servicios SERVICES


"""
a. Crear un objeto con el modelo.
b. Enlistar desde el modelo de datos.
c. Actualizar un registro en el modelo de datos.
d. Borrar un registro del modelo de datos utilizando un modelo Django.
"""
