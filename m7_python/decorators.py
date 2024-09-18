from functools import wraps
from django.shortcuts import redirect
from .models import UserProfile

def rol_requerido(requested_rol: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                try:
                    user_profile = request.user.user_profile  # Accede al perfil del usuario
                    if user_profile.rol == requested_rol:
                        return view_func(request, *args, **kwargs)
                    else:
                        # return redirect('profile')  # Cambiar a tu vista a Pefil o a ruta de 'no autorizado'
                        return redirect('not_authorized')
                except UserProfile.DoesNotExist:
                    return redirect('login')  # Si el perfil no existe, también redirige
            else:
                return redirect('login')  # Redirige al login si no está autentitificado
        return _wrapped_view
    return decorator