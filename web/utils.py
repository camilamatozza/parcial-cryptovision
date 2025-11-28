def clasificar_categoria(texto: str) -> str:
    t = texto.lower()

    palabras_comercial = ["precio", "costo", "cotización", "presupuesto", "compra", "pago"]
    palabras_tecnica = ["error", "fallo", "soporte", "técnico", "tecnico", "no funciona", "problema"]
    palabras_rrhh = ["cv", "currículum", "curriculum", "trabajo", "postulación", "búsqueda laboral"]

    if any(p in t for p in palabras_comercial):
        return "COMERCIAL"
    if any(p in t for p in palabras_tecnica):
        return "TECNICA"
    if any(p in t for p in palabras_rrhh):
        return "RRHH"
    return "GENERAL"
