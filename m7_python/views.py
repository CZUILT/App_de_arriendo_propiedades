from django.shortcuts import render, redirect
from .services import get_all_inmuebles, get_or_create_user_profile, get_inmuebles_for_arrendador
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileForm, ContactModelForm, UserForm, UserEditProfileForm
from .models import UserProfile, ContactForm
from django.contrib.auth import login
from django.contrib import messages

# Vistas o logicas URLs
@login_required # decorador: es una función que recibe otra función como parámetro, le añade cosas y retorna una función diferente
def indexView(request):
    if request.user.is_authenticated:
        profile = get_or_create_user_profile(request.user)
        if profile.rol == 'arrendador':
            messages.success(request, 'Yahoo')
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


# STEP -> CREAR el FORM de Registro
#TODO__ REGISTER and REGISTER_ROL (tipo de usuario) - FORMS
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


#* VER PERFIL 
@login_required
def profile_view(request):
    user = request.user
    user_profile = get_or_create_user_profile(user)  # Llama al servicio para obtener o crear el perfil

    if not user_profile:
        # En caso de que ocurra un error al obtener o crear el perfil
        return render(request, 'error.html', {'message': 'No se pudo obtener el perfil del usuario.'})

    return render(request, 'profile_detail.html', {
        'user': user,
        'profile': user_profile,
    })

#* EDITAR PERFIL -> Usa UserProfile, ContactForm (http://127.0.0.1:8000/profile/edit/)
@login_required
def edit_profile_view(request):
    user = request.user 
    user_profile = get_or_create_user_profile(user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserEditProfileForm(request.POST, instance=user_profile) 
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else: # GET
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