from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("servicios/", views.services, name="services"),

   
    path("contact/", views.contacto, name="contact"),       
    path("contacto/", views.contacto, name="contacto"),     

    path("contacto/ok/", views.contacto_ok, name="contacto_ok"),

    
    path("panel/consultas/", views.panel_consultas, name="panel_consultas"),

    
    path("registro/", views.registro, name="registro"),
    path("validar-cuenta/", views.validar_cuenta, name="validar_cuenta"),

   
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="index"),
        name="logout",
    ),
]

