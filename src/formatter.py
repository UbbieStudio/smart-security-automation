import pandas as pd
import xlsxwriter
import datetime

def generate_visual_report(df, month_name, year, output_path):
    print(f"Generando reporte visual con días de la semana en: {output_path}...")
    
    # 1. Preparación de datos
    def format_cell(row):
        return f"T-{row['tienda']}\n({int(row['entrada'])}:00-{int(row['salida'])}:00)"

    df_display = df.copy()
    df_display['info_celda'] = df_display.apply(format_cell, axis=1)

    # Obtener el número de mes para datetime
    month_num = {m: i+1 for i, m in enumerate(["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"])}[month_name]

    workbook = xlsxwriter.Workbook(output_path)
    
    # FORMATOS
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#4F81BD', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
    cell_fmt = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 9, 'text_wrap': True})
    name_fmt = workbook.add_format({'bold': True, 'bg_color': '#DCE6F1', 'border': 1, 'valign': 'vcenter'})

    def create_grid_sheet(data_subset, sheet_name, title_row):
        pivot = data_subset.pivot_table(index='vigilante_asignado', columns='dia', values='info_celda', aggfunc=lambda x: "\n---\n".join(x)).fillna("")

        for day in range(1, 32):
            if day not in pivot.columns: pivot[day] = ""
        pivot = pivot.reindex(columns=range(1, 32))

        worksheet = workbook.add_worksheet(sheet_name)
        worksheet.write(0, 0, title_row, header_fmt)
        worksheet.set_column(0, 0, 25)
        
        # Diccionario de días
        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

        # Cabecera con Día + Nombre
        for day in range(1, 32):
            try:
                fecha = datetime.date(year, month_num, day)
                nombre_dia = dias_semana[fecha.weekday()]
                cabecera = f"{day}\n{nombre_dia}"
            except ValueError: # Para meses de menos de 31 días
                cabecera = f"{day}"
            
            worksheet.write(0, day, cabecera, header_fmt)
            worksheet.set_column(day, day, 12)

        for row_num, (name, row_values) in enumerate(pivot.iterrows()):
            worksheet.set_row(row_num + 1, 40)
            worksheet.write(row_num + 1, 0, name, name_fmt)
            for col_num, day in enumerate(range(1, 32)):
                worksheet.write(row_num + 1, col_num + 1, row_values[day], cell_fmt)

    create_grid_sheet(df_display, "RESUMEN GENERAL", "VIGILANTE / DÍA")
    workers = sorted([w for w in df_display['vigilante_asignado'].unique() if w != "SIN_ASIGNAR"])
    for worker in workers:
        safe_name = str(worker)[:31].replace(':', '').replace('/', '')
        create_grid_sheet(df_display[df_display['vigilante_asignado'] == worker], safe_name, "DÍA / TURNO")

    workbook.close()
    print(f"✅ Reporte visual finalizado.")