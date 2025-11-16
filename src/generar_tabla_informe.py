import json
import os
import pandas as pd

def generar_tabla_markdown():
    """
    Recopila las métricas de los diferentes escenarios y genera una tabla
    comparativa en formato Markdown.
    """
    ruta_output = os.path.join("data", "output")
    
    # Nombres de los escenarios que quieres incluir en la tabla
    # Asegúrate de que estos nombres coincidan con los nombres de las carpetas
    nombres_escenarios = [
        "base",
        "10_cabinas",
        "95_asistencia",
        "horario_extendido",
        "12_semanas",
        "acelerado"
        # Agrega aquí otros escenarios que hayas corrido
    ]
    
    datos_tabla = []

    for nombre in nombres_escenarios:
        ruta_metricas = os.path.join(ruta_output, nombre, "metricas.json")
        
        if not os.path.exists(ruta_metricas):
            print(f"Advertencia: No se encontró el archivo de métricas para el escenario '{nombre}'. Saltando.")
            continue
            
        with open(ruta_metricas, 'r') as f:
            metricas = json.load(f)
        
        # --- Extracción de datos con manejo de valores faltantes ---
        num_cabinas = metricas.get("parametros_escenario", {}).get("num_cabinas", "N/A")
        
        tiempo_espera = metricas.get("tiempos_espera_minutos", {}).get("promedio", 0)
        
        tasa_abandono = metricas.get("generales", {}).get("tasa_abandono_porcentual", 0)
        
        dias_100 = metricas.get("hitos_vacunacion", {}).get("100_porciento", {}).get("dias", "No alcanzado")
        
        costo_total = metricas.get("costos", {}).get("costo_total_campana", 0)
        
        costo_por_vacunado = metricas.get("costos", {}).get("costo_por_paciente_vacunado", 0)

        datos_tabla.append({
            "Escenario": nombre.replace("_", " ").title(),
            "N.º de Cabinas": num_cabinas,
            "Tiempo Espera Prom. (min)": f"{tiempo_espera:.2f}",
            "Tasa de Abandono (%)": f"{tasa_abandono:.2f}",
            "Días para Vacunar al 100%": f"{dias_100:.2f}" if isinstance(dias_100, (int, float)) else dias_100,
            "Costo Total ($)": f"{costo_total:,.0f}",
            "Costo por Vacunado ($)": f"{costo_por_vacunado:,.0f}"
        })

    if not datos_tabla:
        print("No se pudieron recopilar datos para ningún escenario.")
        return

    # --- Creación de la tabla Markdown ---
    df = pd.DataFrame(datos_tabla)
    markdown_table = df.to_markdown(index=False)
    
    print("\n--- Copia y pega esta tabla en tu archivo informe.md ---\n")
    print(markdown_table)


if __name__ == '__main__':
    generar_tabla_markdown()
