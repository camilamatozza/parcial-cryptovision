# CryptoVision – Recuperatorio Examen Parcial · Programación Web II · UCES
  
El sitio representa la plataforma ficticia **CryptoVision**, un servicio de asesoramiento y gestión de criptomonedas.

---

##  Deploy del proyecto
 **Sitio en Render:** https://parcial-cryptovision.onrender.com/

 **API interna (DRF):** https://parcial-cryptovision.onrender.com/api/consultas/

---

##  Tecnologías utilizadas

- Python 3.x  
- Django  
- Django REST Framework  
- PostgreSQL (base de datos en Render)  
- HTML · CSS · JavaScript  
- WhiteNoise  
- Render 

---

##  Estructura del sitio

El sitio cuenta con:

- Página de inicio  
- Página de servicios  
- Mercado cripto (con API externa)  
- Formulario de contacto (Django Forms + JS)  
- Registro, validación de cuenta y login  
- Panel de administración para el cliente  

Todas las secciones utilizan **templates** que extienden de `base.html`.

---

##  Formularios + Base de Datos

El formulario de contacto:

- Usa **Django Forms**  
- Tiene validaciones con **JavaScript**  
- Guarda los datos en la base de datos PostgreSQL  
- Asigna una **categoría automática** según palabras clave:
  - Comercial → “precio”, “tarifa”, “costo”, “compra”
  - Técnica → “soporte”, “error”, “problema”, “ayuda”
  - RRHH → “trabajo”, “CV”, “empleo”, “linkedin”
  - General → si no contiene ninguna de las anteriores

---

##  Panel del Cliente y Resumen Estadístico

En `/panel_consultas/` el cliente puede:

- Ver todas las solicitudes  
- Editarlas o eliminarlas  
- Ver un **resumen estadístico**:
  - Total de solicitudes  
  - Cantidad por categoría  

---

## Autenticación y validación de cuenta

Incluye:

- Registro con nombre, apellido, email y contraseña  
- Verificación de que el email esté en la tabla **UsuariosPermitidos**  
- Envío de un correo con **código de validación**  
- Activación de cuenta  
- Login con email y contraseña  
- Acceso restringido al panel de consultas

Usuario autorizado obligatorio según consigna:
`annavillegas@live.com.ar`

---

##  Servidor de correo configurado (según consigna)

- SMTP: `c2280296.ferozo.com`  
- Puerto: 465  
- SSL: True  
- TLS: False  

El usuario recibe un correo tanto para validar su cuenta como para confirmar la recepción del formulario de contacto.

---

##  API externa utilizada

Se consume una API relacionada al mercado cripto:

 **URL de la API utilizada:**  
https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd

La información obtenida se muestra en la sección **Mercado**.


