FIXED_WORKERS = [
    {"name": "Vigilante Fijo 01", "type": "fijo", "max_hours": 162},
    {"name": "Vigilante Fijo 02", "type": "fijo", "max_hours": 162},
]

def get_workers(num_refuerzos=15):
    workers = FIXED_WORKERS.copy()
    for i in range(1, num_refuerzos + 1):
        workers.append({
            "name": f"Refuerzo {i:02d}",
            "type": "refuerzo",
            "max_hours": 120
        })
    return workers

WORKERS = get_workers(15)

tiendas_rotativas = ["5", "10", "15"]
tienda_activa = "5"