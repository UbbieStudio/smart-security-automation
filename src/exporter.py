import pandas as pd

def export_to_excel(df, hours_summary, output_path):
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        pd.DataFrame(list(hours_summary.items()), columns=['Vigilante', 'Horas']).to_excel(writer, sheet_name='Resumen', index=False)
        df.to_excel(writer, sheet_name='Maestro', index=False)
        
        for worker in df['vigilante_asignado'].unique():
            if worker != "SIN_ASIGNAR":
                df[df['vigilante_asignado'] == worker].to_excel(writer, sheet_name=str(worker)[:31], index=False)