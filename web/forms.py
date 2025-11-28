from django import forms
from django.contrib.auth.models import User         
from .models import Consulta, UsuarioPermitido      


MOTIVOS = [
    ("asesoramiento", "Asesoramiento"),
    ("compra-venta", "Compra / Venta"),
    ("billeteras", "Billeteras digitales"),
    ("otros", "Otros"),
]

class ContactFormV1(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Tu nombre"})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "tunombre@mail.com"})
    )
    motivo = forms.ChoiceField(
        label="Motivo",
        choices=MOTIVOS
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Contanos qué necesitás"})
    )
    acepta = forms.BooleanField(
        label="Acepto la política de privacidad"
    )


class ConsultaForm(forms.ModelForm):
    
    acepta = forms.BooleanField(
        label="Acepto la política de privacidad",
        required=True
    )

    class Meta:
        model = Consulta
        fields = ["nombre", "email", "asunto", "mensaje"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "asunto": forms.TextInput(attrs={"class": "form-control"}),
            "mensaje": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }  
class RegistroForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Tu nombre completo"})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "tunombre@mail.com"})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput
    )
    codigo = forms.CharField(
        label="Código de validación",
        max_length=10,
        widget=forms.TextInput(attrs={"placeholder": "Código que te dio la empresa"})
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Ya existe un usuario registrado con este email."
            )
        
      
        if not UsuarioPermitido.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este sitio es de acceso restringido. Consultá con el administrador."
            )
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        email = cleaned.get("email")
        codigo = cleaned.get("codigo")

       
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")

       
        if email and codigo:
            try:
                permitido = UsuarioPermitido.objects.get(email=email)
            except UsuarioPermitido.DoesNotExist:
                return cleaned

            if permitido.codigo_validacion != codigo:
                self.add_error("codigo", "El código de validación no es correcto.")

        return cleaned

    def save(self):
        
        nombre = self.cleaned_data["nombre"]
        email = self.cleaned_data["email"].lower()
        password = self.cleaned_data["password1"]

        user = User.objects.create_user(
            username=email,   
            email=email,
            password=password,
        )
        user.first_name = nombre
        user.is_active = False   
        user.save()
        return user


class ValidacionCuentaForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput)
    codigo = forms.CharField(
        label="Código de validación",
        max_length=10,
        widget=forms.TextInput(attrs={"placeholder": "Código que recibiste por mail"})
    )

