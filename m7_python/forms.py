# aquí van nuestros Formularios
from django.contrib.auth.forms import UserCreationForm
from django import forms
from.models import UserProfile, ContactForm, Inmueble, Solicitud
from django.contrib.auth.models import User

#ToDo: REGISTER - FORM

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Ingrese una dirección de correo electrónico válida.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email

#ToDo: REGISTER_ROL - FORM  +  Etapa de Edit PROFILE
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['rut', 'direccion', 'telefono', 'rol']


# Formulario para editar perfil
#* -> UserProfileForm - este form nos va a servir además para cuando vayamos a editar el perfil
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['rut', 'direccion', 'telefono']

# Formulario de Contacto 
class ContactModelForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['customer_email', 'customer_name', 'message']

# Formulario para crear inmueble(s)
class InmuebleForm(forms.ModelForm):
    class Meta: 
        model = Inmueble
        fields = [
            'nombre', 'descripcion', 'm2_construidos', 'm2_totales',
            'num_estacionamientos', 'num_habitaciones', 'num_baños',
            'direccion', 'tipo_inmueble', 'precio', 'disponible',
            'comuna'
        ]

# Formulario para crear solicitudes
class UpdateSolicitudEstadoForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['estado']
        widgets = {
            'estado': forms.Select(choices=Solicitud.ESTADOS)  # ChoiseField basado en el modelo
        } 

# Formulario de disponibilidad de Inmuebles
class EditDisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['disponible']  # Solo permitimos modificar la disponibilidad
        widgets = {
            'disponible': forms.CheckboxInput(),  # (disponible o no - checkbox)
        }

# Formulario ejemplo
class EjemploInmuebleForm(forms.ModelForm):
    class Meta: 
        model = Inmueble
        fields = [
            'nombre', 'descripcion'
        ]









