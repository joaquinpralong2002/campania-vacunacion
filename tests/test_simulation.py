# tests/test_simulation.py

import pytest
from src.simulation import ejecutar_simulacion

def test_ejecucion_smoke_test():
    """
    Prueba una ejecución simple para asegurar que la simulación corre y 
    genera una salida con la estructura correcta.
    """
    # Usar una configuración simple para la prueba
    config_test = {
        "num_cabinas": 1,
        "tasa_llegada_por_minuto": 1,
        "tiempo_promedio_vacunacion_minutos": 3,
        "probabilidad_reprogramacion": 0.1,
        "horas_operacion_por_dia": 1, # Simular solo por 1 hora
        "tasa_asistencia": 0.9,
    }
    
    # Ejecutar la simulación por 1 día (que en esta config es solo 1 hora)
    resultados_df = ejecutar_simulacion(config_test, duracion_dias=1)

    # 1. Asegurar que la simulación produjo un DataFrame
    assert resultados_df is not None
    
    # Si se produjeron eventos, verificar la estructura
    if not resultados_df.empty:
        # 2. Asegurar que el DataFrame tiene las columnas esperadas
        columnas_esperadas = [
            "tiempo_simulacion", "paciente_id", "evento", 
            "longitud_cola_actual", "tiempo_espera_minutos", "tiempo_en_sistema_minutos"
        ]
        for col in columnas_esperadas:
            assert col in resultados_df.columns

        # 3. Asegurar que los tipos de eventos son los esperados
        eventos_posibles = {"Vacunado", "Reprogramacion"}
        eventos_en_df = set(resultados_df["evento"].unique())
        assert eventos_en_df.issubset(eventos_posibles)

def test_simulacion_sin_reprogramacion():
    """
    Prueba una ejecución donde la probabilidad de reprogramación es cero,
    asegurando que no ocurran eventos de este tipo.
    """
    config_test = {
        "num_cabinas": 1,
        "tasa_llegada_por_minuto": 5, # Tasa alta para forzar cola
        "tiempo_promedio_vacunacion_minutos": 3,
        "probabilidad_reprogramacion": 0.0, # <-- Punto clave de la prueba
        "horas_operacion_por_dia": 1,
        "tasa_asistencia": 1.0,
    }
    
    resultados_df = ejecutar_simulacion(config_test, duracion_dias=1)

    if not resultados_df.empty:
        # Asegurar que no hay ningún evento "Reprogramacion"
        assert "Reprogramacion" not in resultados_df["evento"].unique()
