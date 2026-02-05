import pandas as pd
import re

def parse_store_requirements(file_path, sheet_name):
    """
    Analiza una pestaña individual de tienda y extrae los turnos (Entrada/Salida).
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=5)
    df = df.dropna(how='all', axis=1)
    
    rows_e = df[df.iloc[:, 1] == 'E']
    services = []
    
    for idx, row_e in rows_e.iterrows():
        try:
            row_s = df.loc[idx + 1]
        except KeyError:
            continue

        # Ya no necesitamos extraer el vigilante_nombre de la columna 0
        
        for day in range(1, 32):
            col_name = f'Unnamed: {day + 1}'
            
            if col_name in df.columns:
                h_e = row_e[col_name]
                h_s = row_s[col_name]
                
                if pd.notna(h_e) and pd.notna(h_s):
                    try:
                        val_e = float(h_e)
                        val_s = float(h_s)
                        
                        horas_total = val_s - val_e if val_s > val_e else (24 - val_e) + val_s
                        
                        services.append({
                            'tienda': str(sheet_name),
                            'dia': day,
                            'entrada': val_e,
                            'salida': val_s,
                            'horas': horas_total
                            # Columna 'vigilante_actual' ELIMINADA
                        })
                    except (ValueError, TypeError):
                        continue
                        
    return pd.DataFrame(services)

def parse_all_stores(file_path):
    xl = pd.ExcelFile(file_path)
    store_sheets = [s for s in xl.sheet_names if re.match(r'^\d+$', str(s))]
    
    print(f"Detectadas {len(store_sheets)} tiendas para procesar...")
    all_requirements = []
    
    for store_id in store_sheets:
        try:
            df_store = parse_store_requirements(file_path, store_id)
            if not df_store.empty:
                all_requirements.append(df_store)
        except Exception as e:
            print(f"Error procesando tienda {store_id}: {e}")
            
    if not all_requirements:
        return pd.DataFrame()
        
    return pd.concat(all_requirements, ignore_index=True)