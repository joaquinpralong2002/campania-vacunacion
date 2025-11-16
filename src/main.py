# src/main.py

import pandas as pd
import os
import multiprocessing
from functools import partial
from src.config import ConfiguracionSimulacion
from src.simulation import ejecutar_simulacion
from src.analysis import calcular_metricas_principales
from src.visualization import generar_visualizaciones_escenario, plot_comparacion_escenarios

def ejecutar_escenario(nombre_escenario: str, duracion_simulacion_dias: int) -> tuple[str, dict]:
    """
    Ejecuta la simulación y el análisis para un único escenario.
    """
    print(f"\n--- Ejecutando escenario: {nombre_escenario} ---")
    
    # 1. Cargar configuración del escenario
    config_actual = ConfiguracionSimulacion.obtener_configuracion_escenario(nombre_escenario)
    
    # 2. Ejecutar la simulación
    try:
        resultados_df = ejecutar_simulacion(config_actual, duracion_simulacion_dias)
        print(f"Simulación '{nombre_escenario}' completada. Eventos registrados: {len(resultados_df)}")
    except Exception as e:
        print(f"Error al ejecutar la simulación para el escenario '{nombre_escenario}': {e}")
        return nombre_escenario, {}

    # Crear directorio de salida
    ruta_salida_escenario = os.path.join("data", "output", nombre_escenario)
    os.makedirs(ruta_salida_escenario, exist_ok=True)

    # 3. Guardar datos crudos
    nombre_archivo_csv = os.path.join(ruta_salida_escenario, f"resultados_{nombre_escenario}.csv")
    resultados_df.to_csv(nombre_archivo_csv, index=False)
    print(f"Resultados crudos para '{nombre_escenario}' guardados en: {nombre_archivo_csv}")

    # 4. Analizar resultados
    metricas = calcular_metricas_principales(resultados_df, config_actual, duracion_simulacion_dias)
    
    # Imprimir métricas clave
    print(f"Métricas clave para el escenario '{nombre_escenario}':")
    print(f"  Total Vacunados: {metricas.get('generales', {}).get('total_vacunados', 'N/A')}")
    print(f"  Tasa de Abandono: {metricas.get('generales', {}).get('tasa_abandono_porcentual', 0):.2f}%")
    hitos = metricas.get('hitos_vacunacion', {})
    print(f"  Tiempo para 100% población: {hitos.get('100_porciento', {}).get('dias', 'N/A')} días")

    # 5. Generar visualizaciones
    print(f"Generando visualizaciones para '{nombre_escenario}'...")
    generar_visualizaciones_escenario(resultados_df, ruta_salida_escenario)
    print(f"Visualizaciones para '{nombre_escenario}' guardadas en: {ruta_salida_escenario}")
    
    return nombre_escenario, metricas

def main():
    """
    Función principal para ejecutar la simulación de la campaña de vacunación
    en paralelo para diferentes escenarios.
    """
    print("Iniciando la simulación de la campaña de vacunación en paralelo...")

    nombres_escenarios = ["base", "10_cabinas", "80_asistencia", "95_asistencia", "horario_extendido", "dos_dosis", "acelerado"]
    duracion_simulacion_dias = 200

    # Usar multiprocessing para ejecutar escenarios en paralelo
    num_procesos = max(1, multiprocessing.cpu_count() // 2)  # Usar la mitad de los núcleos de CPU
    print(f"Utilizando {num_procesos} procesos para ejecutar {len(nombres_escenarios)} escenarios...")

    # `partial` permite pre-llenar un argumento de la función
    func_ejecutar = partial(ejecutar_escenario, duracion_simulacion_dias=duracion_simulacion_dias)
    
    with multiprocessing.Pool(processes=num_procesos) as pool:
        resultados = pool.map(func_ejecutar, nombres_escenarios)

    # Convertir la lista de resultados en un diccionario
    metricas_por_escenario = {nombre: metricas for nombre, metricas in resultados if metricas}

    # 6. Generar visualizaciones comparativas
    if metricas_por_escenario:
        print("\n--- Generando visualizaciones comparativas entre escenarios ---")
        ruta_salida_comparativa = os.path.join("data", "output", "comparativas")
        os.makedirs(ruta_salida_comparativa, exist_ok=True)

        plot_comparacion_escenarios(metricas_por_escenario, 'costos.costo_total_campana', 'Comparación de Costo Total por Escenario', ruta_salida_comparativa)
        plot_comparacion_escenarios(metricas_por_escenario, 'generales.total_vacunados', 'Comparación de Total de Vacunados por Escenario', ruta_salida_comparativa)
        plot_comparacion_escenarios(metricas_por_escenario, 'tiempos_espera_minutos.promedio', 'Comparación de Tiempo de Espera Promedio por Escenario', ruta_salida_comparativa)
        plot_comparacion_escenarios(metricas_por_escenario, 'costos.eficiencia_costo_tiempo_por_dia', 'Comparación de Eficiencia Costo/Tiempo por Escenario', ruta_salida_comparativa)
        plot_comparacion_escenarios(metricas_por_escenario, 'hitos_vacunacion.100_porciento.dias', 'Comparación de Días para Vacunar al 100% de la Población', ruta_salida_comparativa)
        
        print(f"Visualizaciones comparativas guardadas en: {ruta_salida_comparativa}")
    else:
        print("No se generaron métricas para comparar.")

    print("\nSimulación de la campaña de vacunación finalizada.")

if __name__ == '__main__':
    main()
