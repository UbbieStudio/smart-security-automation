import pandas as pd
import xlsxwriter

def export_to_excel(df, hours_summary, output_path):
    print(f"Generando archivo Excel en: {output_path}...")
    
    # 1. Crear el Workbook
    workbook = xlsxwriter.Workbook(output_path)
    
    # 2. Formatos
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
    festivo_fmt = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'}) 

    # 3. Datos de Resumen
    summary_data = [{"Vigilante": n, "Horas": round(h, 2)} for n, h in hours_summary.items() if h > 0]
    df_summary = pd.DataFrame(summary_data).sort_values(by="Horas", ascending=False)
    
    # Función interna corregida (add_worksheet)
    def write_df(df_to_write, sheet_name):
        # EL MÉTODO CORRECTO ES add_worksheet
        worksheet = workbook.add_worksheet(sheet_name)
        
        # Escribir cabeceras
        for col_num, value in enumerate(df_to_write.columns.values):
            worksheet.write(0, col_num, str(value), header_fmt)
            # Ajuste de ancho
            max_len = max(df_to_write[value].astype(str).map(len).max(), len(str(value))) + 2
            worksheet.set_column(col_num, col_num, max_len)
            
        # Escribir datos
        cols_list = list(df_to_write.columns)
        for row_num, row_data in enumerate(df_to_write.values):
            current_row_fmt = None
            if 'Festivo' in cols_list:
                fest_val = row_data[cols_list.index('Festivo')]
                if fest_val and str(fest_val).strip() != "":
                    current_row_fmt = festivo_fmt
            
            for col_num, cell_value in enumerate(row_data):
                # Escribir la celda
                worksheet.write(row_num + 1, col_num, cell_value, current_row_fmt)

    # Ejecutar escritura
    write_df(df_summary, 'Resumen Personal')
    write_df(df, 'Cuadrante Maestro')
    
    workers = sorted([w for w in df['vigilante_asignado'].unique() if w != "SIN_ASIGNAR"])
    for worker in workers:
        worker_df = df[df['vigilante_asignado'] == worker].sort_values(by=['dia', 'entrada'])
        # Limpieza de nombre de pestaña
        safe_name = str(worker)[:31].replace(':', '').replace('/', '').replace('\\', '').replace('[', '').replace(']', '')
        write_df(worker_df, safe_name)

    # 4. Cerrar
    workbook.close()
    print(f"✅ Proceso finalizado con éxito.")