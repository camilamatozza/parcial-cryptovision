from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   
    path("", views.index, name="index"),
    path("servicios/", views.services, name="services"),
    path("contacto/", views.contacto, name="contacto"),
    path("contact/", views.contacto, name="contact"),
    path("contacto/ok/", views.contacto_ok, name="contacto_ok"),
    path("mercado/", views.mercado, name="mercado"),

    
    path("panel/consultas/", views.panel_consultas, name="panel_consultas"),

   
    path("registro/", views.registro, name="registro"),
    path("validar-cuenta/", views.validar_cuenta, name="validar_cuenta"),

   
    path("api/consultas/", views.api_consultas, name="api_consultas"),

    
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
  path("salir/", views.salir, name="salir"),

]
