# src/visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

def configurar_estilo_graficos():
    """Configura un estilo visual consistente y agradable para todos los gráficos."""
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 7)
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['axes.labelsize'] = 12

def plot_vacunados_acumulados(resultados_df: pd.DataFrame, ruta_guardado: str, horas_operacion_dia: int):
    """
    Genera y guarda un gráfico de la cantidad de pacientes vacunados acumulados a lo largo del tiempo.
    """
    if resultados_df.empty or "evento" not in resultados_df.columns:
        print("Advertencia: DataFrame vacío o sin columna 'evento'. No se puede generar gráfico de vacunados.")
        return

    vacunados_df = resultados_df[resultados_df["evento"] == "Vacunado"].copy()
    if vacunados_df.empty:
        print("Advertencia: No hay datos de vacunados para graficar.")
        return

    vacunados_df['vacunados_acumulados'] = range(1, len(vacunados_df) + 1)
    
    # Creación del gráfico
    plt.figure()
    # Dibujado del gráfico
    plt.plot(vacunados_df['tiempo_simulacion'] / (60 * horas_operacion_dia), vacunados_df['vacunados_acumulados'])
    plt.title('Pacientes Vacunados Acumulados vs. Tiempo')
    plt.xlabel('Tiempo (días)')
    plt.ylabel('Total de Pacientes Vacunados')
    plt.grid(True)
    # Guardado como archivo png
    plt.savefig(os.path.join(ruta_guardado, 'vacunados_acumulados.png'))
    # Liberación de memoria
    plt.close()

def plot_longitud_cola_vs_tiempo(resultados_df: pd.DataFrame, ruta_guardado: str, horas_operacion_dia: int):
    """
    Genera y guarda un gráfico de la longitud de la cola a lo largo del tiempo.
    """
    if resultados_df.empty or "longitud_cola_actual" not in resultados_df.columns:
        print("Advertencia: DataFrame vacío o sin columna 'longitud_cola_actual'. No se puede generar gráfico de cola.")
        return

    plt.figure()
    plt.plot(resultados_df['tiempo_simulacion'] / (60 * horas_operacion_dia), resultados_df['longitud_cola_actual'], alpha=0.7)
    plt.title('Evolución de la Longitud de la Cola vs. Tiempo')
    plt.xlabel('Tiempo (días)')
    plt.ylabel('Número de Pacientes en Cola')
    plt.grid(True)
    plt.savefig(os.path.join(ruta_guardado, 'longitud_cola.png'))
    plt.close()

def plot_histograma_tiempos_espera(resultados_df: pd.DataFrame, ruta_guardado: str):
    """
    Genera y guarda un histograma de los tiempos de espera de los pacientes que fueron vacunados.
    """
    if resultados_df.empty or "evento" not in resultados_df.columns:
        print("Advertencia: DataFrame vacío o sin columna 'evento'. No se puede generar histograma.")
        return

    vacunados_df = resultados_df[resultados_df["evento"] == "Vacunado"]
    if vacunados_df.empty or vacunados_df['tiempo_espera_minutos'].sum() == 0:
        print("Advertencia: No hay tiempos de espera para graficar.")
        return

    plt.figure()
    # kde=True para aladir línea suave que estima distribución
    sns.histplot(data=vacunados_df, x='tiempo_espera_minutos', kde=True, bins=30)
    plt.title('Distribución de los Tiempos de Espera')
    plt.xlabel('Tiempo de Espera (minutos)')
    plt.ylabel('Frecuencia (Nº de Pacientes)')
    plt.grid(True)
    plt.savefig(os.path.join(ruta_guardado, 'histograma_tiempos_espera.png'))
    plt.close()

def plot_comparacion_escenarios(metricas_por_escenario: dict, metrica: str, titulo: str, ruta_guardado: str):
    """
    Genera un gráfico de barras para comparar una métrica específica entre diferentes escenarios.

    Args:
        metricas_por_escenario (dict): Un diccionario donde las claves son nombres de escenarios
                                      y los valores son los diccionarios de métricas de cada uno.
        metrica (str): La clave de la métrica a comparar (ej. 'costo_total_campana').
        titulo (str): Título del gráfico.
        ruta_guardado (str): Ruta para guardar el gráfico.
    """
    # no recibe el DataFrame de una simulación, sino un diccionario que contiene las métricas ya calculadas de varias simulaciones
    nombres_escenarios = list(metricas_por_escenario.keys())
    
    # Navegar la estructura anidada del diccionario de métricas
    valores = []
    for nombre in nombres_escenarios:
        valor = metricas_por_escenario[nombre]
        # Asumimos que la métrica puede estar anidada (ej. 'costos.costo_total_campana')
        claves_anidadas = metrica.split('.')
        for clave in claves_anidadas:
            valor = valor.get(clave, {})
        valores.append(valor if isinstance(valor, (int, float)) else 0)

    plt.figure()
    barplot = sns.barplot(x=nombres_escenarios, y=valores)
    plt.title(titulo)
    plt.ylabel(metrica.replace('_', ' ').title())
    plt.xlabel('Escenario')
    plt.xticks(rotation=45, ha='right')
    
    # Añadir etiquetas de valor sobre las barras
    for i, v in enumerate(valores):
        barplot.text(i, v + 0.5, f'{v:,.2f}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(ruta_guardado, f'comparacion_{metrica}.png'))
    plt.close()

def generar_visualizaciones_escenario(resultados_df: pd.DataFrame, ruta_escenario: str, config_escenario: dict):
    """
    Genera y guarda todas las visualizaciones para un único escenario. Simplifica el main.py, para que solo tenga que llamar a esta función.
    """
    # Asegurar que la carpeta destino existe
    if not os.path.exists(ruta_escenario):
        os.makedirs(ruta_escenario)
    
    # Configurar estilo de gráficos
    configurar_estilo_graficos()
    
    horas_operacion_dia = config_escenario["horas_operacion_por_dia"]

    # Llamar a cada una de las funciones de gráficos individuales
    plot_vacunados_acumulados(resultados_df, ruta_escenario, horas_operacion_dia)
    plot_longitud_cola_vs_tiempo(resultados_df, ruta_escenario, horas_operacion_dia)
    plot_histograma_tiempos_espera(resultados_df, ruta_escenario)
    
    print(f"Gráficos para el escenario guardados en: {ruta_escenario}")

# --- Bloque para Pruebas ---
if __name__ == '__main__':
    
    # Crear datos de prueba
    datos_prueba = {
        "tiempo_simulacion": np.arange(0, 100, 0.5),
        "paciente_id": [f"P{i}" for i in range(200)],
        "evento": np.random.choice(["Vacunado", "Reprogramacion"], 200, p=[0.7, 0.3]),
        "longitud_cola_actual": np.random.randint(0, 50, 200),
        "tiempo_espera_minutos": np.random.gamma(2, 10, 200),
        "tiempo_en_sistema_minutos": np.random.gamma(3, 10, 200),
    }
    df_prueba = pd.DataFrame(datos_prueba)
    
    # Cargar configuración del escenario base para los cálculos
    from src.config import ConfiguracionSimulacion
    config_prueba = ConfiguracionSimulacion.obtener_configuracion_escenario("base")
    
    # Ruta para guardar los gráficos de prueba
    ruta_prueba = "data/output/plots_prueba"
    
    print(f"--- Generando visualizaciones de prueba en '{ruta_prueba}' ---")
    generar_visualizaciones_escenario(df_prueba, ruta_prueba, config_prueba)

    # --- Prueba para el gráfico de comparación ---
    metricas_prueba = {
        "escenario_base": {
            "generales": {"total_vacunados": 1000},
            "costos": {"costo_total_campana": 5000000}
        },
        "escenario_10_cabinas": {
            "generales": {"total_vacunados": 1400},
            "costos": {"costo_total_campana": 6500000}
        },
        "escenario_pocas_llegadas": {
            "generales": {"total_vacunados": 500},
            "costos": {"costo_total_campana": 2500000}
        }
    }
    
    print("\n--- Generando gráfico de comparación de escenarios ---")
    plot_comparacion_escenarios(
        metricas_por_escenario=metricas_prueba,
        metrica='costos.costo_total_campana',
        titulo='Comparación de Costo Total por Escenario',
        ruta_guardado=ruta_prueba
    )
    plot_comparacion_escenarios(
        metricas_por_escenario=metricas_prueba,
        metrica='generales.total_vacunados',
        titulo='Comparación de Total de Vacunados por Escenario',
        ruta_guardado=ruta_prueba
    )
    print("Gráficos de comparación guardados.")
