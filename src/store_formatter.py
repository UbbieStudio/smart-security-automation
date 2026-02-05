import pandas as pd
import xlsxwriter
import datetime

def generate_store_report(df, month_name, year, output_path):
    print(f"Generando reporte por tiendas con días de la semana en: {output_path}...")
    
    def format_cell(row):
        return f"{row['vigilante_asignado']}\n({int(row['entrada'])}:00-{int(row['salida'])}:00)"

    df_display = df.copy()
    df_display['info_celda'] = df_display.apply(format_cell, axis=1)
    month_num = {m: i+1 for i, m in enumerate(["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"])}[month_name]

    workbook = xlsxwriter.Workbook(output_path)
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#C0504D', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
    cell_fmt = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 9, 'text_wrap': True})
    store_fmt = workbook.add_format({'bold': True, 'bg_color': '#F2DCDB', 'border': 1, 'valign': 'vcenter'})

    def create_store_grid(data_subset, sheet_name, title_label):
        pivot = data_subset.pivot_table(index='tienda', columns='dia', values='info_celda', aggfunc=lambda x: "\n---\n".join(x)).fillna("")
        for day in range(1, 32):
            if day not in pivot.columns: pivot[day] = ""
        pivot = pivot.reindex(columns=range(1, 32))

        worksheet = workbook.add_worksheet(sheet_name)
        worksheet.write(0, 0, title_label, header_fmt)
        worksheet.set_column(0, 0, 15)
        
        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

        for day in range(1, 32):
            try:
                fecha = datetime.date(year, month_num, day)
                nombre_dia = dias_semana[fecha.weekday()]
                cabecera = f"{day}\n{nombre_dia}"
            except ValueError:
                cabecera = f"{day}"
            worksheet.write(0, day, cabecera, header_fmt)
            worksheet.set_column(day, day, 15)

        for row_num, (store_id, row_values) in enumerate(pivot.iterrows()):
            worksheet.set_row(row_num + 1, 45)
            worksheet.write(row_num + 1, 0, f"Tienda {store_id}", store_fmt)
            for col_num, day in enumerate(range(1, 32)):
                worksheet.write(row_num + 1, col_num + 1, row_values[day], cell_fmt)

    create_store_grid(df_display, "RESUMEN TODAS TIENDAS", "TIENDA / DÍA")
    stores = sorted(df_display['tienda'].unique(), key=lambda x: int(x) if str(x).isdigit() else x)
    for store in stores:
        create_store_grid(df_display[df_display['tienda'] == store], f"Tienda {store}"[:31], "DÍA / PERSONAL")

    workbook.close()
    print(f"✅ Reporte de tiendas finalizado.")