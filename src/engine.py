import pandas as pd
import datetime
import math
import sys
import os
from src.parser import parse_all_stores
from src.config import TIENDAS_ROTATIVAS_210, HORARIOS_ESPECIALES, CURRENT_YEAR, HORAS_ESTANDAR_CONTRATO, FESTIVOS_2026
from src.workers import VIGILANTES_FIJOS, get_full_staff
from src.exporter import export_to_excel
from src.formatter import generate_visual_report
from src.store_formatter import generate_store_report # Nueva importación

# ... (Clase SchedulingEngine se mantiene igual que antes) ...

class SchedulingEngine:
    def __init__(self, requirements_df, month):
        self.df = requirements_df.copy()
        self.month = month
        self.year = CURRENT_YEAR
        self.staff = []
        self.hours_tracker = {}

    def apply_business_rules(self):
        tienda_activa = TIENDAS_ROTATIVAS_210.get(self.month)
        tiendas_rotativas = set(TIENDAS_ROTATIVAS_210.values())
        tiendas_rotativas.add("210")
        self.df = self.df[~((self.df['tienda'].isin(tiendas_rotativas)) & (self.df['tienda'] != tienda_activa))]
        for tienda, info in HORARIOS_ESPECIALES.items():
            if self.month in info['meses']:
                mask = self.df['tienda'] == tienda
                self.df.loc[mask, 'entrada'] = float(info['horario'][0])
                self.df.loc[mask, 'salida'] = float(info['horario'][1])
                self.df.loc[mask, 'horas'] = float(info['horario'][1] - info['horario'][0])
        mask_274 = self.df['tienda'] == "274"
        for idx, row in self.df[mask_274].iterrows():
            try:
                if datetime.date(self.year, self.month, int(row['dia'])).weekday() in [4, 5]:
                    self.df.loc[idx, ['entrada', 'salida', 'horas']] = [16.0, 22.0, 6.0]
            except: continue
        def es_festivo(row):
            return FESTIVOS_2026.get((self.month, int(row['dia'])), "")
        self.df['Festivo'] = self.df.apply(es_festivo, axis=1)
        self.df = self.df.sort_values(by=['dia', 'entrada']).reset_index(drop=True)
        return self.df

    def analyze_and_setup_staff(self):
        total_hours_needed = self.df['horas'].sum()
        current_capacity = sum(w['max_horas'] for w in VIGILANTES_FIJOS)
        deficit = total_hours_needed - current_capacity
        extra_needed = math.ceil(deficit / HORAS_ESTANDAR_CONTRATO) if deficit > 0 else 0
        self.staff = get_full_staff(extra_needed)
        self.hours_tracker = {w['nombre']: 0.0 for w in self.staff}
        return extra_needed

    def is_worker_available(self, worker_name, day, start_h, end_h):
        assigned = self.df[self.df['vigilante_asignado'] == worker_name]
        for _, shift in assigned.iterrows():
            if shift['dia'] == day:
                if not (end_h <= shift['entrada'] or start_h >= shift['salida']): return False
            if shift['dia'] == day - 1:
                if (start_h + 24) - shift['salida'] < 12: return False
            if shift['dia'] == day + 1:
                if (shift['entrada'] + 24) - end_h < 12: return False
        return True

    def assign_workers(self):
        self.df['vigilante_asignado'] = "SIN_ASIGNAR"
        worker_idx = 0
        for idx, row in self.df.iterrows():
            asignado = False
            for _ in range(len(self.staff)):
                worker = self.staff[worker_idx % len(self.staff)]
                worker_idx += 1
                if (self.hours_tracker[worker['nombre']] + row['horas'] <= worker['max_horas'] and 
                    self.is_worker_available(worker['nombre'], row['dia'], row['entrada'], row['salida'])):
                    self.df.at[idx, 'vigilante_asignado'] = worker['nombre']
                    self.hours_tracker[worker['nombre']] += row['horas']
                    asignado = True
                    break
            if not asignado:
                for worker in self.staff:
                    if self.is_worker_available(worker['nombre'], row['dia'], row['entrada'], row['salida']):
                        self.df.at[idx, 'vigilante_asignado'] = worker['nombre']
                        self.hours_tracker[worker['nombre']] += row['horas']
                        asignado = True
                        break
        return self.df

def get_month_name(month_num):
    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", 
             "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    return meses[month_num - 1]

if __name__ == "__main__":
    input_file = "data/03_CONSUMSEGURIDAD.xlsm"
    output_dir = "outputs"
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    print("--- GENERADOR DE CUADRANTES AUTOMÁTICO ---")
    try:
        selected_month = int(input("Introduce el número del mes (1-12): "))
    except: sys.exit(1)

    nombre_mes = get_month_name(selected_month)
    
    # Rutas de archivos
    tecnico_file = os.path.join(output_dir, f"CUADRANTE_TECNICO_{nombre_mes}.xlsx")
    visual_file = os.path.join(output_dir, f"REPORTE_VIGILANTES_{nombre_mes}.xlsx")
    tiendas_file = os.path.join(output_dir, f"REPORTE_TIENDAS_{nombre_mes}.xlsx")
    
    engine = SchedulingEngine(parse_all_stores(input_file), month=selected_month)
    engine.apply_business_rules()
    engine.analyze_and_setup_staff()
    
    print(f"Asignando personal para {nombre_mes}...")
    final_df = engine.assign_workers()
    
    # Los 3 archivos
    export_to_excel(final_df, engine.hours_tracker, tecnico_file)
    generate_visual_report(final_df, nombre_mes, CURRENT_YEAR, visual_file)
    generate_store_report(final_df, nombre_mes, CURRENT_YEAR, tiendas_file)
    
    print(f"\n✅ Proceso completado. Revisa la carpeta '{output_dir}'.")