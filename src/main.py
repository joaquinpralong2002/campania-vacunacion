# src/main.py

import json
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
    generar_visualizaciones_escenario(resultados_df, ruta_salida_escenario, config_actual)
    print(f"Visualizaciones para '{nombre_escenario}' guardadas en: {ruta_salida_escenario}")

    # 6. Guardar métricas en JSON
    ruta_metricas_json = os.path.join(ruta_salida_escenario, "metricas.json")
    try:
        with open(ruta_metricas_json, 'w') as f:
            json.dump(metricas, f, indent=4, default=str) # default=str para manejar tipos no serializables como numpy.int64
        print(f"Métricas para '{nombre_escenario}' guardadas en: {ruta_metricas_json}")
    except Exception as e:
        print(f"Error al guardar las métricas en JSON para '{nombre_escenario}': {e}")

    return nombre_escenario, metricas

def main():
    """
    Función principal para ejecutar la simulación de la campaña de vacunación
    en paralelo para diferentes escenarios.
    
    Esta función ejecuta las simulaciones y guarda los resultados y métricas
    de cada escenario en su respectivo directorio en 'data/output/'.
    """
    print("Iniciando la simulación de la campaña de vacunación...")

    # Escenarios a ejecutar. Puedes comentar o añadir escenarios según sea necesario.
    nombres_escenarios = [
        #"base", 
        #"10_cabinas" 
        # "95_asistencia",
        # "7_cabinas",
        # "60_asistencia",
        # "80_asistencia",
        # "acelerado",
        # "dos_dosis",
        # "horario_extendido",
        # "digito_dni"
        # "12_semanas"
    ]
    duracion_simulacion_dias = 200

    # Usar multiprocessing para ejecutar escenarios en paralelo
    # Se puede ajustar num_procesos a 1 para ejecución secuencial si hay problemas de memoria.
    num_procesos = max(1, multiprocessing.cpu_count() // 2)
    print(f"Utilizando {num_procesos} procesos para ejecutar {len(nombres_escenarios)} escenarios...")

    # `partial` permite pre-llenar un argumento de la función
    func_ejecutar = partial(ejecutar_escenario, duracion_simulacion_dias=duracion_simulacion_dias)
    
    # Ejecutar los escenarios
    with multiprocessing.Pool(processes=num_procesos) as pool:
        # Usamos pool.map para procesar todos los escenarios.
        # Los resultados (métricas) no se usan aquí, pero se podrían registrar si fuera necesario.
        pool.map(func_ejecutar, nombres_escenarios)

    print("\nTodas las simulaciones de escenarios han finalizado.")
    print("Los resultados y métricas de cada escenario se han guardado en sus respectivos directorios en 'data/output/'.")
    print("Para generar los gráficos comparativos, ejecuta el script 'src/generar_comparativas.py'.")

if __name__ == '__main__':
    main()
