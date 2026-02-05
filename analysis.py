import pandas as pd

file_path = "data/03_CONSUMSEGURIDAD.xlsm"
tienda_test = '31' # La de las Fallas

# Leemos la pestaña 31 saltándonos las primeras filas vacías
df = pd.read_excel(file_path, sheet_name=tienda_test, skiprows=5)

print(f"--- Datos de la Tienda {tienda_test} ---")
print(df.dropna(how='all', axis=0).head(10)) # Quitamos filas totalmente vacías