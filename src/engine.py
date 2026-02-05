import pandas as pd
from src.parser import parse_all_stores
from src.exporter import export_to_excel
from src.config import WORKERS, tiendas_rotativas, tienda_activa

class QuadrantEngine:
    def __init__(self, file_path, month):
        self.df = parse_all_stores(file_path)
        self.workers = WORKERS

    def run(self, output_path):
        if self.df.empty:
            print("ERROR: No se han podido cargar datos.")
            return

        # Simple filtering
        self.df = self.df[~((self.df['tienda'].isin(tiendas_rotativas)) & (self.df['tienda'] != tienda_activa))]
        self.df = self.df.sort_values(by=['dia', 'entrada'])
        
        # Assignment Logic
        stats = {w['name']: 0.0 for w in self.workers}
        limits = {w['name']: float(w['max_hours']) for w in self.workers}
        
        # We create the list of names first
        assigned_names = []
        for row in self.df.itertuples():
            h = float(row.horas)
            target = "SIN_ASIGNAR"
            for name in stats:
                if stats[name] + h <= limits[name]:
                    target = name
                    stats[name] += h
                    break
            assigned_names.append(target)
        
        # Add the column all at once - NO .loc error possible here
        self.df['vigilante_asignado'] = assigned_names

        summary = {k: v for k, v in stats.items() if v > 0}
        export_to_excel(self.df, summary, output_path)
        print("--- PROCESO COMPLETADO ---")

if __name__ == "__main__":
    m = input("Mes (1-12): ")
    engine = QuadrantEngine("data/03_CONSUMSEGURIDAD.xlsm", m)
    engine.run("data/CUADRANTE_FINAL.xlsx")