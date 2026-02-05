# src/workers.py
from src.config import HORAS_ESTANDAR_CONTRATO

# Plantilla de personal fija
VIGILANTES_FIJOS = [
    {"id": 1, "nombre": "Juan Pérez", "max_horas": 160},
    {"id": 2, "nombre": "María García", "max_horas": 160},
    {"id": 3, "nombre": "Carlos López", "max_horas": 160},
    {"id": 4, "nombre": "Ana Belén", "max_horas": 120},
    {"id": 5, "nombre": "David Ruiz", "max_horas": 160},
    {"id": 6, "nombre": "Elena Sanz", "max_horas": 160},
]

def get_full_staff(needed_extra_workers=0):
    """Retorna la plantilla fija más los refuerzos necesarios."""
    staff = VIGILANTES_FIJOS.copy()
    for i in range(1, needed_extra_workers + 1):
        staff.append({
            "id": 100 + i,
            "nombre": f"Refuerzo {i:02d}",
            "max_horas": HORAS_ESTANDAR_CONTRATO
        })
    return staff