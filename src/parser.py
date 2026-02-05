import pandas as pd

def parse_all_stores(file_path):
    print(f"Leyendo archivo: {file_path}...")
    xl = pd.ExcelFile(file_path)
    all_requirements = []

    for sheet in xl.sheet_names:
        # Simple read. If the first row is empty, Pandas handles it or we find it in the next step.
        df = pd.read_excel(xl, sheet_name=sheet)
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # If 'dia' isn't in the first row, it's likely in the second.
        if 'dia' not in df.columns:
            df = pd.read_excel(xl, sheet_name=sheet, header=1)
            df.columns = [str(c).strip().lower() for c in df.columns]

        if 'dia' in df.columns and 'entrada' in df.columns:
            df = df.dropna(subset=['dia', 'entrada'])
            df['tienda'] = str(sheet)
            
            if 'salida' in df.columns:
                df['horas'] = df['salida'] - df['entrada']
                # Correct midnight shifts
                df.loc[df['horas'] < 0, 'horas'] += 24
                all_requirements.append(df)
                print(f"✅ Tienda detectada: {sheet}")

    return pd.concat(all_requirements, ignore_index=True) if all_requirements else pd.DataFrame()