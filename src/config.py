# src/config.py

CURRENT_YEAR = 2026
HORAS_ESTANDAR_CONTRATO = 160.0

# Calendario de Festivos Valencia/C.Valenciana 2026
FESTIVOS_2026 = {
    (1, 1): "Año Nuevo",
    (1, 6): "Reyes Magos",
    (1, 22): "San Vicente Mártir",
    (3, 19): "San José",
    (4, 3): "Viernes Santo",
    (4, 6): "Lunes de Pascua",
    (4, 13): "San Vicente Ferrer",
    (5, 1): "Día del Trabajo",
    (6, 24): "San Juan",
    (8, 15): "Asunción de la Virgen",
    (10, 9): "Día Comunitat Valenciana",
    (10, 12): "Fiesta Nacional España",
    (11, 2): "Traslado Todos los Santos",
    (12, 7): "Traslado Día Constitución",
    (12, 8): "Inmaculada Concepción",
    (12, 25): "Navidad"
}

# Tiendas rotativas vinculadas a la 210
TIENDAS_ROTATIVAS_210 = {
    1: "567", 2: "1057", 3: "534", 4: "286", 
    5: "567", 6: "286", 7: "534", 8: "1057", 
    9: "567", 10: "286", 11: "534", 12: "1057"
}

# Tiendas con horarios especiales (Festivales Julio/Agosto)
HORARIOS_ESPECIALES = {
    "111": {"meses": [7, 8], "horario": (9, 22)},
    "151": {"meses": [7, 8], "horario": (9, 22)},
    "1060": {"meses": [7, 8], "horario": (9, 22)},
}