# tests/test_analysis.py

import pytest
import pandas as pd
from src.analysis import calcular_metricas_principales
from src.config import ConfiguracionSimulacion

@pytest.fixture
def datos_prueba_df():
    """Crea un DataFrame de ejemplo para usar en los tests."""
    datos = {
        "tiempo_simulacion": [10, 20, 25, 30, 35],
        "paciente_id": ["P1", "P2", "P3", "P4", "P5"],
        "evento": ["Vacunado", "Vacunado", "Reprogramacion", "Vacunado", "Reprogramacion"],
        "longitud_cola_actual": [2, 3, 5, 1, 4],
        "tiempo_espera_minutos": [5, 15, 0, 2, 0],
        "tiempo_en_sistema_minutos": [8, 18, 0, 5, 0],
    }
    return pd.DataFrame(datos)

def test_calculo_metricas_generales(datos_prueba_df):
    """Prueba el cálculo de métricas generales."""
    config = ConfiguracionSimulacion.obtener_configuracion_escenario("base")
    metricas = calcular_metricas_principales(datos_prueba_df, config, duracion_dias=1)
    
    assert metricas["generales"]["total_vacunados"] == 3
    assert metricas["generales"]["total_reprogramados"] == 2
    assert metricas["generales"]["tasa_abandono_porcentual"] == pytest.approx(40.0)

def test_calculo_metricas_tiempos(datos_prueba_df):
    """Prueba el cálculo de métricas de tiempo."""
    config = ConfiguracionSimulacion.obtener_configuracion_escenario("base")
    metricas = calcular_metricas_principales(datos_prueba_df, config, duracion_dias=1)

    assert metricas["tiempos_espera_minutos"]["promedio"] == pytest.approx(22 / 3)
    assert metricas["tiempos_espera_minutos"]["maximo"] == 15.0
    # El mínimo tiempo de espera para alguien que FUE vacunado es 2, no 0.
    assert metricas["tiempos_espera_minutos"]["minimo"] == 2.0

def test_calculo_metricas_costos(datos_prueba_df):
    """Prueba el cálculo de métricas de costos."""
    config = ConfiguracionSimulacion.obtener_configuracion_escenario("base")
    metricas = calcular_metricas_principales(datos_prueba_df, config, duracion_dias=1)

    assert metricas["costos"]["costo_total_campana"] == pytest.approx(281600.0)
    assert metricas["costos"]["costo_por_paciente_vacunado"] == pytest.approx(281600.0 / 3)

def test_analisis_dataframe_vacio():
    """Prueba que la función maneja correctamente un DataFrame vacío."""
    config = ConfiguracionSimulacion.obtener_configuracion_escenario("base")
    metricas = calcular_metricas_principales(pd.DataFrame(), config, duracion_dias=1)
    assert "error" in metricas
    assert metricas["error"] == "El DataFrame de resultados está vacío. No se pueden calcular métricas."
