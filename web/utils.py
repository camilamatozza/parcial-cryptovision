def clasificar_categoria(texto: str) -> str:
    """
    Clasifica el texto de la consulta en una categoría:
    COMERCIAL, TECNICA, RRHH o GENERAL.
    """
    t = texto.lower()

    palabras_comercial = [
        "precio", "costo", "tarifa", "compra",
        "cotización", "cotizacion", "presupuesto", "pago"
    ]
    palabras_tecnica = [
        "soporte", "error", "problema", "ayuda",
        "fallo", "no funciona"
    ]
    palabras_rrhh = [
        "trabajo", "cv", "currículum", "curriculum",
        "empleo", "linkedin", "búsqueda laboral", "busqueda laboral"
    ]

    if any(p in t for p in palabras_comercial):
        return "COMERCIAL"
    if any(p in t for p in palabras_tecnica):
        return "TECNICA"
    if any(p in t for p in palabras_rrhh):
        return "RRHH"

    return "GENERAL"
