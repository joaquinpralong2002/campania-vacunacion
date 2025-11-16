# src/generar_comparativas.py

import os
import json
import pandas as pd
from src.visualization import plot_comparacion_escenarios
from src.config import ConfiguracionSimulacion

def generar_tabla_consolidada(metricas_por_escenario: dict, ruta_salida: str):
    """
    Genera una única tabla consolidada en formato CSV con parámetros y métricas clave de todos los escenarios.
    """
    print("\n--- Generando tabla consolidada de escenarios ---")
    
    datos_tabla = []
    for nombre, metricas in metricas_por_escenario.items():
        try:
            # Obtener parámetros de entrada desde el módulo de configuración
            config_escenario = ConfiguracionSimulacion.obtener_configuracion_escenario(nombre)
        except ValueError:
            print(f"Advertencia: No se encontró configuración para el escenario '{nombre}'. Se usarán valores por defecto.")
            config_escenario = {}

        # Extraer métricas de resultados (outputs)
        hitos = metricas.get("hitos_vacunacion", {})
        tiempos_espera = metricas.get("tiempos_espera_minutos", {})
        cola = metricas.get("longitud_cola", {})
        generales = metricas.get("generales", {})
        rendimiento = metricas.get("rendimiento", {})
        costos = metricas.get("costos", {})

        fila = {
            # Identificación
            "Escenario": nombre,
            
            # Parámetros de Entrada (Inputs)
            "N° Cabinas": config_escenario.get("num_cabinas"),
            "Horas por Jornada": config_escenario.get("horas_operacion_por_dia"),
            "Tasa de Asistencia (%)": config_escenario.get("tasa_asistencia", 0) * 100,
            "Política de Asignación": "Estándar", # Placeholder, ya que no es un parámetro simple
            
            # Métricas de Rendimiento (Outputs)
            "Días para Vacunar 80%": hitos.get("80_porciento", {}).get("dias"),
            "Días para Vacunar 100%": hitos.get("100_porciento", {}).get("dias"),
            "Tiempo Espera Promedio (min)": tiempos_espera.get("promedio"),
            "Tiempo Espera Máximo (min)": tiempos_espera.get("maximo"),
            "Longitud Máxima de Cola": cola.get("maxima"),
            "Total Reprogramaciones": generales.get("total_reprogramados"),
            "Utilización Cabinas (%)": rendimiento.get("utilizacion_promedio_cabinas_porcentual"),
            
            # Métricas de Costo (Outputs)
            "Costo Total": costos.get("costo_total_campana"),
            "Costo por Vacunado": costos.get("costo_por_paciente_vacunado")
        }
        datos_tabla.append(fila)
    
    if not datos_tabla:
        print("No se generaron datos para la tabla consolidada.")
        return

    df_consolidado = pd.DataFrame(datos_tabla)
    
    # Formatear columnas para mejor legibilidad
    format_dict = {
        'Tasa de Asistencia (%)': '{:.0f}%',
        'Días para Vacunar 80%': '{:.1f}',
        'Días para Vacunar 100%': '{:.1f}',
        'Tiempo Espera Promedio (min)': '{:,.1f}',
        'Tiempo Espera Máximo (min)': '{:,.1f}',
        'Longitud Máxima de Cola': '{:,.0f}',
        'Total Reprogramaciones': '{:,.0f}',
        'Utilización Cabinas (%)': '{:.1f}%',
        'Costo Total': 'S/ {:,.0f}',
        'Costo por Vacunado': 'S/ {:,.2f}'
    }
    
    df_display = df_consolidado.copy()
    for col, fmt in format_dict.items():
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(lambda x: fmt.format(x) if pd.notna(x) else 'N/A')

    ruta_csv = os.path.join(ruta_salida, "resumen_consolidado_escenarios.csv")
    df_consolidado.to_csv(ruta_csv, index=False, float_format='%.2f')
    
    print(f"Tabla consolidada guardada en: {ruta_csv}")
    print("\nResumen de Escenarios:")
    print(df_display.to_string())


def generar_graficos_comparativos():
    """
    Carga las métricas guardadas de múltiples escenarios y genera
    visualizaciones y tablas comparativas.
    """
    print("--- Iniciando la generación de resultados comparativos ---")

    ruta_base_output = os.path.join("data", "output")
    ruta_salida_comparativa = os.path.join(ruta_base_output, "comparativas")
    os.makedirs(ruta_salida_comparativa, exist_ok=True)

    metricas_por_escenario = {}

    try:
        # Excluir 'comparativas' y cualquier archivo (como .DS_Store)
        nombres_escenarios = [d.name for d in os.scandir(ruta_base_output) if d.is_dir() and d.name != "comparativas"]
    except FileNotFoundError:
        print(f"Error: El directorio base de resultados '{ruta_base_output}' no fue encontrado.")
        print("Asegúrate de haber ejecutado las simulaciones primero con 'python -m src.main'.")
        return

    if not nombres_escenarios:
        print("No se encontraron directorios de escenarios en 'data/output/'.")
        return

    print(f"Escenarios encontrados: {', '.join(nombres_escenarios)}")

    for nombre_escenario in nombres_escenarios:
        ruta_metricas_json = os.path.join(ruta_base_output, nombre_escenario, "metricas.json")
        if os.path.exists(ruta_metricas_json):
            try:
                with open(ruta_metricas_json, 'r') as f:
                    metricas = json.load(f)
                metricas_por_escenario[nombre_escenario] = metricas
                print(f"Métricas cargadas para el escenario: '{nombre_escenario}'")
            except Exception as e:
                print(f"Advertencia: No se pudieron cargar las métricas para '{nombre_escenario}': {e}. Se omitirá.")
        else:
            print(f"Advertencia: No se encontró 'metricas.json' para '{nombre_escenario}'. Se omitirá.")

    if not metricas_por_escenario:
        print("\nNo se cargaron métricas. No se pueden generar resultados comparativos.")
        return

    # --- Generar Gráficos ---
    print("\nGenerando visualizaciones comparativas...")
    metricas_a_graficar = [
        ('costos.costo_total_campana', 'Comparación de Costo Total por Escenario'),
        ('tiempos_espera_minutos.promedio', 'Comparación de Tiempo de Espera Promedio por Escenario'),
        ('hitos_vacunacion.100_porciento.dias', 'Comparación de Días para Vacunar al 100%'),
        ('generales.tasa_abandono_porcentual', 'Comparación de Tasa de Abandono (%) por Escenario'),
        ('costos.costo_diario_promedio', 'Comparación de Costo Diario Promedio por Escenario')
    ]
    for clave_metrica, titulo in metricas_a_graficar:
        try:
            plot_comparacion_escenarios(metricas_por_escenario, clave_metrica, titulo, ruta_salida_comparativa)
        except Exception as e:
            print(f"Error al generar el gráfico '{titulo}': {e}")
    print(f"Visualizaciones comparativas guardadas en: {ruta_salida_comparativa}")

    # --- Generar Tabla Consolidada ---
    generar_tabla_consolidada(metricas_por_escenario, ruta_salida_comparativa)

    print("\n--- Proceso de generación de resultados finalizado ---")

if __name__ == '__main__':
    generar_graficos_comparativos()
