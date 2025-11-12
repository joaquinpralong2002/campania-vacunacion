# src/analysis.py

import pandas as pd
import numpy as np
from src.config import ConfiguracionSimulacion

def calcular_metricas_principales(resultados_df: pd.DataFrame, config_escenario: dict, duracion_dias: int) -> dict:
    """
    Calcula las métricas de rendimiento clave a partir de los datos de la simulación.

    Args:
        resultados_df (pd.DataFrame): DataFrame con los datos crudos de la simulación.
        config_escenario (dict): Diccionario con los parámetros del escenario simulado.
        duracion_dias (int): Duración de la simulación en días.

    Returns:
        dict: Un diccionario con todas las métricas calculadas.
    """
    if resultados_df.empty:
        return {"error": "El DataFrame de resultados está vacío. No se pueden calcular métricas."}

    # --- Filtrar eventos ---
    vacunados_df = resultados_df[resultados_df["evento"] == "Vacunado"].copy()
    reprogramados_df = resultados_df[resultados_df["evento"] == "Reprogramacion"].copy()

    # --- Métricas Generales ---
    total_vacunados = len(vacunados_df)
    total_reprogramados = len(reprogramados_df)
    total_pacientes_procesados = total_vacunados + total_reprogramados
    tasa_abandono = (total_reprogramados / total_pacientes_procesados) if total_pacientes_procesados > 0 else 0

    # --- Estadísticas de Cola y Tiempos (solo para pacientes vacunados) ---
    if total_vacunados > 0:
        tiempo_espera_promedio = vacunados_df['tiempo_espera_minutos'].mean()
        tiempo_espera_maximo = vacunados_df['tiempo_espera_minutos'].max()
        tiempo_espera_minimo = vacunados_df['tiempo_espera_minutos'].min()
        
        tiempo_en_sistema_promedio = vacunados_df['tiempo_en_sistema_minutos'].mean()
        
        longitud_cola_promedio = resultados_df['longitud_cola_actual'].mean()
        longitud_cola_maxima = resultados_df['longitud_cola_actual'].max()
    else:
        tiempo_espera_promedio = 0
        tiempo_espera_maximo = 0
        tiempo_espera_minimo = 0
        tiempo_en_sistema_promedio = 0
        longitud_cola_promedio = 0
        longitud_cola_maxima = resultados_df['longitud_cola_actual'].max() if not resultados_df.empty else 0

    # --- Utilización de Puestos ---
    tiempo_total_servicio = total_vacunados * config_escenario["tiempo_promedio_vacunacion_minutos"]
    tiempo_total_disponible = config_escenario["num_cabinas"] * config_escenario["horas_operacion_por_dia"] * 60 * duracion_dias
    utilizacion_promedio_cabinas = (tiempo_total_servicio / tiempo_total_disponible) if tiempo_total_disponible > 0 else 0

    # --- Cálculo de Costos ---
    costos_config = ConfiguracionSimulacion.COSTOS
    costo_fijo_total = costos_config["costo_fijo_por_cabina_por_dia"] * config_escenario["num_cabinas"] * duracion_dias
    costo_total_dosis = costos_config["costo_por_dosis"] * total_vacunados
    costo_total_reprogramaciones = costos_config["costo_por_reprogramacion"] * total_reprogramados
    
    costo_total_campana = costo_fijo_total + costo_total_dosis + costo_total_reprogramaciones
    costo_por_paciente_vacunado = (costo_total_campana / total_vacunados) if total_vacunados > 0 else 0

    # --- Ensamblar diccionario de resultados ---
    metricas = {
        "generales": {
            "total_pacientes_procesados": total_pacientes_procesados,
            "total_vacunados": total_vacunados,
            "total_reprogramados": total_reprogramados,
            "tasa_abandono_porcentual": tasa_abandono * 100,
        },
        "tiempos_espera_minutos": {
            "promedio": tiempo_espera_promedio,
            "maximo": tiempo_espera_maximo,
            "minimo": tiempo_espera_minimo,
        },
        "longitud_cola": {
            "promedio": longitud_cola_promedio,
            "maxima": longitud_cola_maxima,
        },
        "rendimiento": {
            "tiempo_promedio_en_sistema_minutos": tiempo_en_sistema_promedio,
            "utilizacion_promedio_cabinas_porcentual": utilizacion_promedio_cabinas * 100,
        },
        "costos": {
            "costo_total_campana": costo_total_campana,
            "costo_fijo_total": costo_fijo_total,
            "costo_total_dosis": costo_total_dosis,
            "costo_total_reprogramaciones": costo_total_reprogramaciones,
            "costo_por_paciente_vacunado": costo_por_paciente_vacunado,
        }
    }
    
    return metricas

# --- Bloque para Pruebas ---
if __name__ == '__main__':
    # Crear un DataFrame de ejemplo para probar la función de análisis
    datos_prueba = {
        "tiempo_simulacion": [10, 20, 25, 30, 35],
        "paciente_id": ["P1", "P2", "P3", "P4", "P5"],
        "evento": ["Vacunado", "Vacunado", "Reprogramacion", "Vacunado", "Reprogramacion"],
        "longitud_cola_actual": [2, 3, 5, 1, 4],
        "tiempo_espera_minutos": [5, 15, 0, 2, 0],
        "tiempo_en_sistema_minutos": [8, 18, 0, 5, 0],
    }
    df_prueba = pd.DataFrame(datos_prueba)
    
    # Cargar configuración del escenario base para los cálculos
    config_prueba = ConfiguracionSimulacion.obtener_configuracion_escenario("base")
    
    print("--- Ejecutando análisis de prueba con datos de ejemplo ---")
    metricas_calculadas = calcular_metricas_principales(df_prueba, config_prueba, duracion_dias=1)
    
    # Imprimir los resultados de forma legible
    import json
    print(json.dumps(metricas_calculadas, indent=4))

    # Prueba con DataFrame vacío
    print("\n--- Probando con un DataFrame vacío ---")
    metricas_vacias = calcular_metricas_principales(pd.DataFrame(), config_prueba, duracion_dias=1)
    print(json.dumps(metricas_vacias, indent=4))
