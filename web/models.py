from django.db import models
from django.utils import timezone


class Consulta(models.Model):
    TIPO_CHOICES = [
        ("COMERCIAL", "Comercial"),
        ("TECNICA", "Técnica"),
        ("RRHH", "RRHH"),
        ("GENERAL", "General"),
    ]

    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=150)
    mensaje = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    categoria = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default="GENERAL",
    )

    def __str__(self):
        return f"{self.asunto} - {self.email}"


class UsuarioPermitido(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    codigo_validacion = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} ({self.email})"
