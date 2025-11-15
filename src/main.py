# src/main.py

import pandas as pd
import os
from src.config import ConfiguracionSimulacion
from src.simulation import ejecutar_simulacion
from src.analysis import calcular_metricas_principales
from src.visualization import generar_visualizaciones_escenario, plot_comparacion_escenarios

def main():
    """
    Función principal para ejecutar la simulación de la campaña de vacunación
    a través de diferentes escenarios, analizar los resultados y generar visualizaciones.
    """
    print("Iniciando la simulación de la campaña de vacunación...")

    # Definir los escenarios a ejecutar
    # Asegúrate de que estos nombres coincidan con los definidos en ConfiguracionSimulacion
    nombres_escenarios = ["base", "10_cabinas", "80_asistencia","95_asistencia", "60_asistencia", "dos_dosis", "acelerado"] 
    
    # Duración de la simulación en días para todos los escenarios
    # Se reduce a 2 días para obtener resultados rápidos y evitar que la simulación se cuelgue
    # con parámetros extremos. Ajusta este valor según la necesidad de tu análisis.
    duracion_simulacion_dias = 2 

    # Diccionario para almacenar las métricas de cada escenario para comparaciones
    metricas_por_escenario = {}

    for nombre_escenario in nombres_escenarios:
        print(f"\n--- Ejecutando escenario: {nombre_escenario} ---")
        
        # 1. Cargar configuración del escenario
        config_actual = ConfiguracionSimulacion.obtener_configuracion_escenario(nombre_escenario)
        
        # 2. Ejecutar la simulación
        # Se añade un try-except para manejar posibles errores en la simulación
        try:
            resultados_df = ejecutar_simulacion(config_actual, duracion_simulacion_dias)
            print(f"Simulación '{nombre_escenario}' completada. Eventos registrados: {len(resultados_df)}")
        except Exception as e:
            print(f"Error al ejecutar la simulación para el escenario '{nombre_escenario}': {e}")
            continue # Pasar al siguiente escenario si hay un error

        # Crear directorio de salida para el escenario actual
        ruta_salida_escenario = os.path.join("data", "output", nombre_escenario)
        os.makedirs(ruta_salida_escenario, exist_ok=True)

        # 3. Guardar los datos crudos de la simulación
        nombre_archivo_csv = os.path.join(ruta_salida_escenario, f"resultados_{nombre_escenario}.csv")
        resultados_df.to_csv(nombre_archivo_csv, index=False)
        print(f"Resultados crudos guardados en: {nombre_archivo_csv}")

        # 4. Analizar los resultados
        metricas = calcular_metricas_principales(resultados_df, config_actual, duracion_simulacion_dias)
        metricas_por_escenario[nombre_escenario] = metricas
        
        print(f"Métricas clave para el escenario '{nombre_escenario}':")
        # Imprimir algunas métricas clave para la consola
        print(f"  Total Vacunados: {metricas['generales']['total_vacunados']}")
        print(f"  Tasa de Abandono: {metricas['generales']['tasa_abandono_porcentual']:.2f}%")
        print(f"  Tiempo Espera Promedio: {metricas['tiempos_espera_minutos']['promedio']:.2f} min")
        print(f"  Costo Total Campaña: ${metricas['costos']['costo_total_campana']:,.2f}")

        # 5. Generar visualizaciones para el escenario actual
        print(f"Generando visualizaciones para el escenario '{nombre_escenario}'...")
        generar_visualizaciones_escenario(resultados_df, ruta_salida_escenario)
        print(f"Visualizaciones guardadas en: {ruta_salida_escenario}")

    # 6. Generar visualizaciones comparativas entre escenarios
    print("\n--- Generando visualizaciones comparativas entre escenarios ---")
    ruta_salida_comparativa = os.path.join("data", "output", "comparativas")
    os.makedirs(ruta_salida_comparativa, exist_ok=True)

    # Ejemplo de gráficos comparativos
    if metricas_por_escenario: # Solo si hay métricas para comparar
        plot_comparacion_escenarios(
            metricas_por_escenario,
            metrica='costos.costo_total_campana',
            titulo='Comparación de Costo Total por Escenario',
            ruta_guardado=ruta_salida_comparativa
        )
        plot_comparacion_escenarios(
            metricas_por_escenario,
            metrica='generales.total_vacunados',
            titulo='Comparación de Total de Vacunados por Escenario',
            ruta_guardado=ruta_salida_comparativa
        )
        plot_comparacion_escenarios(
            metricas_por_escenario,
            metrica='tiempos_espera_minutos.promedio',
            titulo='Comparación de Tiempo de Espera Promedio por Escenario',
            ruta_guardado=ruta_salida_comparativa
        )
        plot_comparacion_escenarios(
            metricas_por_escenario,
            metrica='costos.eficiencia_costo_tiempo_por_dia',
            titulo='Comparación de Eficiencia Costo/Tiempo por Escenario',
            ruta_guardado=ruta_salida_comparativa
        )
        print(f"Visualizaciones comparativas guardadas en: {ruta_salida_comparativa}")
    else:
        print("No hay métricas para comparar entre escenarios.")

    print("\nSimulación de la campaña de vacunación finalizada.")

if __name__ == '__main__':
    main()
