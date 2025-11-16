# src/analysis.py

import pandas as pd
import numpy as np
from src.config import ConfiguracionSimulacion

def calcular_tiempo_para_hitos_vacunacion(vacunados_df: pd.DataFrame, poblacion_total: int, horas_operacion_dia: int) -> dict:
    """
    Calcula el tiempo (días y semanas) para alcanzar hitos de vacunación (70%, 80%, 100%).

    Args:
        vacunados_df (pd.DataFrame): DataFrame con los datos de los pacientes vacunados.
        poblacion_total (int): Tamaño total de la población objetivo.
        horas_operacion_dia (int): Horas de operación del centro por día.

    Returns:
        dict: Un diccionario con los tiempos para cada hito.
    """
    hitos = {
        "70_porciento": 0.70,
        "80_porciento": 0.80,
        "100_porciento": 1.0,
    }
    
    #Diccionario para almecenar resultados
    resultados_hitos = {}

    #Chequeo para valores nulos
    if vacunados_df.empty or poblacion_total == 0:
        for hito_nombre in hitos:
            resultados_hitos[hito_nombre] = {"dias": "N/A", "semanas": "N/A", "vacunados_necesarios": "N/A"}
        return resultados_hitos

    # Asegurarse de que el df esté ordenado por tiempo
    vacunados_df = vacunados_df.sort_values(by="tiempo_simulacion").reset_index(drop=True)
    vacunados_df["vacunados_acumulados"] = vacunados_df.index + 1

    minutos_por_dia_operativo = horas_operacion_dia * 60

    for hito_nombre, hito_porcentaje in hitos.items():

        # Calcular el número de vacunados necesarios para el hito
        vacunados_necesarios = int(poblacion_total * hito_porcentaje)
        
        # Buscar la primera vez que se alcanza el hito
        df_hito = vacunados_df[vacunados_df["vacunados_acumulados"] >= vacunados_necesarios]
        
        if not df_hito.empty:
            tiempo_en_minutos = df_hito.iloc[0]["tiempo_simulacion"]
            
            # Convertir minutos a días y semanas operativos
            dias_necesarios = tiempo_en_minutos / minutos_por_dia_operativo
            semanas_necesarias = dias_necesarios / 5  # Asumiendo operación 5 días/semana
            
            resultados_hitos[hito_nombre] = {
                "dias": round(dias_necesarios, 2),
                "semanas": round(semanas_necesarias, 2),
                "vacunados_necesarios": vacunados_necesarios
            }
        else:
            # Si el hito nunca se alcanzó en la simulación
            resultados_hitos[hito_nombre] = {
                "dias": "No alcanzado",
                "semanas": "No alcanzado",
                "vacunados_necesarios": vacunados_necesarios
            }
            
    return resultados_hitos


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
    # solo las filas donde el evento fue "Vacunado"
    vacunados_df = resultados_df[resultados_df["evento"] == "Vacunado"].copy()
    # solo las filas donde el evento fue "Reprogramacion"
    reprogramados_df = resultados_df[resultados_df["evento"] == "Reprogramacion"].copy()

    # --- Métricas Generales  ---
    # cuenta cuántas filas hay en vacunados_df
    total_vacunados = int(len(vacunados_df))
    # cuenta cuántas filas hay en reprogramados_df
    total_reprogramados = int(len(reprogramados_df))
    # La suma de los dos anteriores
    total_pacientes_procesados = total_vacunados + total_reprogramados
    # porcentaje de pacientes que reprogramaron sobre el total.
    tasa_abandono = (total_reprogramados / total_pacientes_procesados) if total_pacientes_procesados > 0 else 0

    # --- Estadísticas de Cola y Tiempos  ---
    if total_vacunados > 0:
        tiempo_espera_promedio = float(vacunados_df['tiempo_espera_minutos'].mean())
        tiempo_espera_maximo = float(vacunados_df['tiempo_espera_minutos'].max())
        tiempo_espera_minimo = float(vacunados_df['tiempo_espera_minutos'].min())
        
        tiempo_en_sistema_promedio = float(vacunados_df['tiempo_en_sistema_minutos'].mean())
        
        longitud_cola_promedio = float(resultados_df['longitud_cola_actual'].mean())
        longitud_cola_maxima = int(resultados_df['longitud_cola_actual'].max())
    else:
        tiempo_espera_promedio = 0.0
        tiempo_espera_maximo = 0.0
        tiempo_espera_minimo = 0.0
        tiempo_en_sistema_promedio = 0.0
        longitud_cola_promedio = 0.0
        longitud_cola_maxima = int(resultados_df['longitud_cola_actual'].max()) if not resultados_df.empty else 0

    # --- Utilización de Puestos ---
    # cuánto tiempo se invirtió en total vacunando
    tiempo_total_servicio = total_vacunados * config_escenario["tiempo_promedio_vacunacion_minutos"]
    # tiempo total que las cabinas estuvieron disponibles
    tiempo_total_disponible = config_escenario["num_cabinas"] * config_escenario["horas_operacion_por_dia"] * 60 * duracion_dias
    # división del tiempo de servicio entre el tiempo disponible.
    utilizacion_promedio_cabinas = (tiempo_total_servicio / tiempo_total_disponible) if tiempo_total_disponible > 0 else 0

    # --- Cálculo de Costos ---
    costos_config = ConfiguracionSimulacion.COSTOS
    #Costo por cabina por día
    costo_fijo_total = costos_config["costo_fijo_por_cabina_por_dia"] * config_escenario["num_cabinas"] * duracion_dias
    costo_total_dosis = costos_config["costo_por_dosis"] * total_vacunados
    costo_total_reprogramaciones = costos_config["costo_por_reprogramacion"] * total_reprogramados
    
    costo_total_campana = costo_fijo_total + costo_total_dosis + costo_total_reprogramaciones
    costo_por_paciente_vacunado = (costo_total_campana / total_vacunados) if total_vacunados > 0 else 0

    # Métrica de costo diario: Costo total por día de campaña.
    costo_diario_promedio = (costo_total_campana / duracion_dias) if duracion_dias > 0 else 0

    # --- Cálculo de Tiempos para Hitos de Vacunación ---
    poblacion_total = config_escenario.get("poblacion_total", 0)
    horas_operacion = config_escenario.get("horas_operacion_por_dia", 1)
    tiempos_hitos = calcular_tiempo_para_hitos_vacunacion(vacunados_df, poblacion_total, horas_operacion)

    # --- Ensamblar diccionario de resultados ---
    metricas = {
        "parametros_escenario": {
            "num_cabinas": config_escenario.get("num_cabinas"),
            "tasa_asistencia": config_escenario.get("tasa_asistencia"),
            "tiempo_promedio_vacunacion_minutos": config_escenario.get("tiempo_promedio_vacunacion_minutos"),
        },
        "generales": {
            "total_pacientes_procesados": total_pacientes_procesados,
            "total_vacunados": total_vacunados,
            "total_reprogramados": total_reprogramados,
            "tasa_abandono_porcentual": float(tasa_abandono * 100),
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
            "utilizacion_promedio_cabinas_porcentual": float(utilizacion_promedio_cabinas * 100),
        },
        "costos": {
            "costo_total_campana": float(costo_total_campana),
            "costo_fijo_total": float(costo_fijo_total),
            "costo_total_dosis": float(costo_total_dosis),
            "costo_total_reprogramaciones": float(costo_total_reprogramaciones),
            "costo_por_paciente_vacunado": float(costo_por_paciente_vacunado),
            "costo_diario_promedio": float(costo_diario_promedio),
        },
        "hitos_vacunacion": tiempos_hitos,
    }
    
    return metricas
