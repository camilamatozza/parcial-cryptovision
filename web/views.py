from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Consulta, UsuarioPermitido
from .utils import clasificar_categoria
from .forms import ConsultaForm, RegistroForm, ValidacionCuentaForm


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ConsultaSerializer
from django.contrib.auth import logout
from django.shortcuts import redirect, render


import requests


def index(request):
    return render(request, "index.html")


def services(request):
    return render(request, "services.html")


def contacto(request):
    if request.method == "POST":
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)

            
            texto = f"{consulta.asunto} {consulta.mensaje}"
            consulta.categoria = clasificar_categoria(texto)

            consulta.save()

            
            asunto_mail = f"[{consulta.categoria}] Nueva consulta desde CryptoVision"
            cuerpo_mail = f"""
Se recibió una nueva consulta desde la web.

Nombre: {consulta.nombre}
Email: {consulta.email}
Asunto: {consulta.asunto}
Mensaje:
{consulta.mensaje}

Categoría asignada: {consulta.categoria}
"""

            try:
                send_mail(
                    subject=asunto_mail,
                    message=cuerpo_mail,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[consulta.email],  
                    fail_silently=False,
                )
            except Exception:
                
                messages.warning(
                    request,
                    "Tu consulta se guardó correctamente, pero hubo un problema enviando el correo de confirmación.",
                )

            return redirect("contacto_ok")
    else:
        form = ConsultaForm()

    return render(request, "contacto.html", {"form": form})


def contacto_ok(request):
    return render(request, "contacto_ok.html")


@login_required
def panel_consultas(request):
    total = Consulta.objects.count()

    por_categoria = (
        Consulta.objects
        .values("categoria")
        .annotate(cantidad=Count("id"))
        .order_by("categoria")
    )

    consultas = Consulta.objects.order_by("-fecha")

    contexto = {
        "total": total,
        "por_categoria": por_categoria,
        "consultas": consultas,
    }
    return render(request, "panel_consultas.html", contexto)


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()  
            email = user.email

            
            permitido = UsuarioPermitido.objects.get(email=email)

            
            url_validar = request.build_absolute_uri(
                reverse("validar_cuenta")
            ) + f"?email={email}"

            cuerpo = f"""
Hola {user.first_name},

Tu registro en CryptoVision fue recibido.

Para validar tu cuenta usá este código: {permitido.codigo_validacion}

Ingresá a este enlace y completá el código:
{url_validar}

Si vos no iniciaste este registro, podés ignorar este mensaje.
"""

            try:
                send_mail(
                    subject="Validación de cuenta - CryptoVision",
                    message=cuerpo,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception:
                messages.warning(
                    request,
                    "Se creó el usuario, pero hubo un problema enviando el correo de validación.",
                )

            return render(request, "registro_ok.html", {"email": email})
    else:
        form = RegistroForm()

    return render(request, "registro.html", {"form": form})


def validar_cuenta(request):
    
    email_inicial = request.GET.get("email", "")

    if request.method == "POST":
        form = ValidacionCuentaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            codigo = form.cleaned_data["codigo"]

            try:
                permitido = UsuarioPermitido.objects.get(email=email)
            except UsuarioPermitido.DoesNotExist:
                form.add_error(None, "Este email no está autorizado.")
            else:
                if permitido.codigo_validacion != codigo:
                    form.add_error("codigo", "El código de validación no es correcto.")
                else:
                    try:
                        user = User.objects.get(email=email)
                    except User.DoesNotExist:
                        form.add_error(None, "No existe un usuario para este email.")
                    else:
                        user.is_active = True
                        user.save()
                        messages.success(
                            request,
                            "Cuenta validada correctamente. Ya podés iniciar sesión."
                        )
                        return redirect("login")
    else:
        form = ValidacionCuentaForm(initial={"email": email_inicial})

    return render(request, "validar_cuenta.html", {"form": form})

@api_view(["GET"])
def api_consultas(request):
    """
    Devuelve todas las consultas en JSON.
    URL: /api/consultas/
    """
    consultas = Consulta.objects.order_by("-fecha")
    serializer = ConsultaSerializer(consultas, many=True)
    return Response(serializer.data)


def mercado(request):
    """
    Consume una API externa de criptomonedas y muestra
    un pequeño tablero de precios.
    """
    monedas = []
    error = None

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,cardano,solana",
    }

    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        monedas = resp.json()
    except Exception:
        error = "No se pudo cargar la información del mercado en este momento."

    contexto = {
        "monedas": monedas,
        "error": error,
    }
    return render(request, "mercado.html", contexto)


def salir(request):
  
    logout(request)
    return redirect("index")
