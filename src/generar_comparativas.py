# src/generar_comparativas.py

import os
import json
from src.visualization import plot_comparacion_escenarios

def generar_graficos_comparativos():
    """
    Carga las métricas guardadas de múltiples escenarios y genera
    visualizaciones comparativas.
    """
    print("--- Iniciando la generación de gráficos comparativos ---")

    ruta_base_output = os.path.join("data", "output")
    ruta_salida_comparativa = os.path.join(ruta_base_output, "comparativas")
    os.makedirs(ruta_salida_comparativa, exist_ok=True)

    metricas_por_escenario = {}

    # Escanear directorios de escenarios en busca de archivos de métricas
    try:
        nombres_escenarios = [d.name for d in os.scandir(ruta_base_output) if d.is_dir() and d.name != "comparativas"]
    except FileNotFoundError:
        print(f"Error: El directorio base de resultados '{ruta_base_output}' no fue encontrado.")
        print("Asegúrate de haber ejecutado las simulaciones primero con 'python -m src.main'.")
        return

    if not nombres_escenarios:
        print("No se encontraron directorios de escenarios en 'data/output/'.")
        print("Asegúrate de haber ejecutado las simulaciones primero.")
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
            except json.JSONDecodeError:
                print(f"Advertencia: El archivo de métricas para '{nombre_escenario}' está corrupto o vacío. Se omitirá.")
            except Exception as e:
                print(f"Advertencia: No se pudieron cargar las métricas para '{nombre_escenario}': {e}. Se omitirá.")
        else:
            print(f"Advertencia: No se encontró el archivo 'metricas.json' para el escenario '{nombre_escenario}'. Se omitirá.")

    # Generar visualizaciones comparativas si se cargaron métricas
    if metricas_por_escenario:
        print("\nGenerando visualizaciones comparativas...")

        # Lista de métricas a graficar
        metricas_a_graficar = [
            ('costos.costo_total_campana', 'Comparación de Costo Total por Escenario'),
            ('generales.total_vacunados', 'Comparación de Total de Vacunados por Escenario'),
            ('tiempos_espera_minutos.promedio', 'Comparación de Tiempo de Espera Promedio por Escenario'),
            ('costos.eficiencia_costo_tiempo_por_dia', 'Comparación de Eficiencia Costo/Tiempo por Escenario'),
            ('hitos_vacunacion.100_porciento.dias', 'Comparación de Días para Vacunar al 100% de la Población')
        ]

        for clave_metrica, titulo in metricas_a_graficar:
            try:
                plot_comparacion_escenarios(metricas_por_escenario, clave_metrica, titulo, ruta_salida_comparativa)
            except KeyError as e:
                print(f"Advertencia: No se pudo generar el gráfico '{titulo}' porque la clave '{clave_metrica}' no existe en todos los escenarios. Detalle: {e}")
            except Exception as e:
                print(f"Error al generar el gráfico '{titulo}': {e}")

        print(f"\nVisualizaciones comparativas guardadas en: {ruta_salida_comparativa}")
    else:
        print("\nNo se cargaron métricas de ningún escenario. No se pueden generar gráficos comparativos.")

    print("--- Proceso de generación de gráficos finalizado ---")

if __name__ == '__main__':
    generar_graficos_comparativos()
