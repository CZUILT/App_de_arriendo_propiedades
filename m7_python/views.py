from django.shortcuts import render, redirect, get_object_or_404
from.services import (get_all_inmuebles, get_or_create_user_profile, get_inmuebles_for_arrendador, 
                       create_inmueble_for_arrendador, actualizar_disponibilidad_inmueble)
from django.contrib.auth.decorators import login_required
from.forms import (CustomUserCreationForm, UserProfileForm, ContactModelForm, UserForm, 
                   UserEditProfileForm, InmuebleForm, EditDisponibilidadForm, EjemploInmuebleForm,
                   UpdateSolicitudEstadoForm)
from.models import UserProfile, ContactForm, Inmueble, Solicitud, User
from django.contrib.auth import login
from django.contrib import messages
from.decorators import rol_requerido

#* Route para manejo de error para ingresos indevidos NOT_AUTH
def not_authorized_view(request):
    return render(request, "not_authorized.html", {})

# Vistas o logicas URLs
@login_required # decorador: es una función que recibe otra función como parámetro, le añade cosas y retorna una función diferente
def indexView(request):
    if request.user.is_authenticated:
        profile = get_or_create_user_profile(request.user)
        if profile.rol == 'arrendador':
            messages.success(request, 'Lista de inmuebles disponibles')
            return redirect ('dashboard_arrendador') 
        elif profile.rol == 'arrendatario':
            return redirect('index_arrendatario')
        else:
            return redirect('login')
        # inmuebles = get_all_inmuebles()
        # return render(request,'index.html',{'inmuebles':inmuebles} )
    else:
        return redirect('login')

@login_required   
def index_arrendatario(request):
    inmuebles = get_all_inmuebles()
    return render(request,'arrendatario/index_arrendatario.html', {'inmuebles': inmuebles})

@login_required 
def dashboard_arrendador(request):
    inmuebles = get_inmuebles_for_arrendador(request.user)
    return render(request, 'arrendador/dashboard_arrendador.html', {'inmuebles': inmuebles})



#ToDo: REGISTER and REGISTER_ROL (tipo de usuario) - FORMS
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('register_rol')
    else:
        form = CustomUserCreationForm()
    return render(request,'registration/register.html',{'form':form} )

@login_required
def register_rol(request):
    user_profile = get_or_create_user_profile(request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige a la página de inicio o cualquier otra página
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'registration/register_rol.html', {'form': form})


#* VISUALIZAR PERFIL 
@login_required
def profile_view(request):
    user = request.user
    user_profile = get_or_create_user_profile(user)  # Llama al servicio para obtener o crear el perfil

    if not user_profile:
        # En caso de que ocurra un error al obtener o crear el perfil
        return render(request, 'error.html', {'message': 'No se pudo encontrar el perfil del usuario ingresado.'})

    return render(request, 'profile_detail.html', {
        'user': user,
        'profile': user_profile,
    })

#* EDITAR PERFIL -> Usa UserProfile, ContactForm (http://127.0.0.1:8000/profile/edit/)
@login_required
def edit_profile_view(request):
    user = request.user 
    user_profile = get_or_create_user_profile(user)
    if request.method == 'POST': # Corresponde a un POST
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserEditProfileForm(request.POST, instance=user_profile) 
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else: # Corresponde a un GET
        user_form = UserForm(instance=user) 
        profile_form = UserEditProfileForm(instance=user_profile)
    return render(request, 'profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

    # return render(request, 'profile_edit.html', {})
"""
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['rut', 'direccion', 'telefono']
"""

# def todas_las_vistas_tienen_el_request(request):
#     request.user 
#     request.user.first_name
#     request.user.last_name 
#     request.user.user_profile.rol
#     pass


def about(request):
    return render(request, 'about.html', {})


@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactModelForm(request.POST) # <- {"customer_email": "kiki@gamial.com", "customer_name": "Kiki", "message": "Hola soy Kiki"}
        print(f'errors -> {form.errors}')
        if form.is_valid():
            #* MODEL - Guardamos la data en nuestra DB en la TABLA CONACTFORM
            ContactForm.objects.create(**form.cleaned_data) # pasamos la data del diccionario .cleaned_data a argumentos
            # messages.success(request, f'Gracias por contactarse con nosotros, en breve le responderemos.')
            return redirect('home')
    else: 
        form = ContactModelForm()   
    return render(request, 'contact.html', {'form':form})

####################################
#######! VISTAS ARRENDADOR #########
####################################
@login_required
@rol_requerido('arrendador')
def create_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = create_inmueble_for_arrendador(request.user, form.cleaned_data)
            return redirect('dashboard_arrendador')
    else: 
        form = InmuebleForm()
    return render(request, 'arrendador/create_inmueble.html', {'form': form})

@login_required
def edit_inmueble(request, inmueble_id):
    inmueble_edit =  get_object_or_404(Inmueble, id=inmueble_id)
    # inmueble_edit =  Inmueble.objects.get(pk=inmueble_id)
    if request.method == 'POST':
        form = InmuebleForm(request.POST, instance=inmueble_edit)
        if form.is_valid():
            #* Crear service para update Inmueble y validar
            form.save()
            return redirect('dashboard_arrendador')
    else: 
        form = InmuebleForm(instance=inmueble_edit)
    return render(request, 'arrendador/edit_inmueble.html', {'form': form})

@login_required
def delete_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    if request.method == 'POST':
        inmueble.delete()
        return redirect('dashboard_arrendador')

    return render(request, 'arrendador/delete_inmueble.html', {'inmueble': inmueble})


@login_required
def detail_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    # inmueble =  Inmueble.objects.get(id=inmueble_id)
    return render(request, 'detail_inmueble.html', {'inmueble': inmueble})

@login_required
def edit_disponibilidad_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    if request.method == 'POST':
        form = EditDisponibilidadForm(request.POST, instance=inmueble) 
        if form.is_valid():
            disponible = form.cleaned_data['disponible']
            result = actualizar_disponibilidad_inmueble(inmueble_id, disponible)
            if result["success"]:
                messages.success(request, result["message"])
            else: 
                messages.error(request, result["message"])
            return redirect('dashboard_arrendador')
             
    else: 
        form = EditDisponibilidadForm(instance=inmueble)
    return render(request, 'arrendador/edit_disponibilidad.html', {'form': form, 'inmueble': inmueble})

@login_required
def view_list_solicitudes(request, inmueble_id):
    pass

@login_required
def edit_status_solicitud(request, inmueble_id):
    pass

####################################
#######! VISTAS ARRENDATARIO #######
####################################

@login_required
@rol_requerido('arrendatario')
def send_solicitud(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    if request.method == 'POST':
        solicitud = Solicitud(arrendatario= request.user, inmueble= inmueble, estado= 'pendiente')
        solicitud.save()
        messages.success(request, f'Solicitud inmueble {inmueble.nombre} realizada con éxito!!!')
        return redirect('index_arrendatario')
    return render(request, 'arrendatario/send_solicitud.html', {'inmueble': inmueble})


def view_list_user_solicitudes(request):
    arrendatario =  get_object_or_404(User, id=request.user.id)
    solicitudes = Solicitud.objects.filter(arrendatario=arrendatario)
    return render(request, 'arrendatario/list_user_solicitudes.html', {
        'solicitudes': solicitudes,
        'arrendatario': arrendatario
    })

@login_required
def view_list_solicitudes(request, inmueble_id):
    # Obtenemos inmueble que validaremos previamente
    inmueble = get_object_or_404(Inmueble, id=inmueble_id) 
    solicitudes = Solicitud.objects.filter(inmueble_id=inmueble_id)
    return render(request, 'arrendador/list_solicitudes.html', {'inmueble':inmueble, 'solicitudes': solicitudes})

@login_required
def edit_status_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id) 
    if request.method == 'POST':
        form = UpdateSolicitudEstadoForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            print(f'--> {form.cleaned_data['estado']}')
            return redirect('view_list_solicitudes', inmueble_id=solicitud.inmueble.id)
    else:
        form = UpdateSolicitudEstadoForm(instance=solicitud)
    return render(request, 'arrendador/edit_status_solicitud.html', {'form': form, 'solicitud': solicitud})
    

def cancelar_solicitud(request, solicitud_id):
    pass

def detail_inmueble_user(request, inmueble_id):
    pass

#! estas serán funciones (services)
# Filtro por comuna y por región
def filtros(request):
    pass

def buscar_por_nombre(request):
    pass

###########################
def view_ejemplo_form(request, data_id):
    print(f'id por params --> {data_id}')
    inmu = Inmueble.objects.get(id=data_id)
    print(f'inmu encontrado --> {inmu}')
    
    context = {
        
    }
    return render(request, 'ejemplo.html', context)