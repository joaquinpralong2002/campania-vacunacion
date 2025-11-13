# tests/test_visualization.py

import pytest
import pandas as pd
import numpy as np
import os
from src.visualization import (
    generar_visualizaciones_escenario, 
    plot_comparacion_escenarios
)

@pytest.fixture
def datos_simulacion_completos():
    """Crea un DataFrame de ejemplo con datos variados para las pruebas."""
    datos = {
        "tiempo_simulacion": np.arange(0, 100, 0.5),
        "paciente_id": [f"P{i}" for i in range(200)],
        "evento": np.random.choice(["Vacunado", "Reprogramacion"], 200, p=[0.7, 0.3]),
        "longitud_cola_actual": np.random.randint(0, 50, 200),
        "tiempo_espera_minutos": np.random.gamma(2, 10, 200),
        "tiempo_en_sistema_minutos": np.random.gamma(3, 10, 200),
    }
    return pd.DataFrame(datos)

@pytest.fixture
def metricas_comparacion_ejemplo():
    """Crea un diccionario de métricas de ejemplo para probar la comparación de escenarios."""
    return {
        "escenario_base": {
            "generales": {"total_vacunados": 1000},
            "costos": {"costo_total_campana": 5000000}
        },
        "escenario_7_cabinas": {
            "generales": {"total_vacunados": 1400},
            "costos": {"costo_total_campana": 6500000}
        }
    }

def test_generar_visualizaciones_escenario_crea_archivos(datos_simulacion_completos, tmp_path):
    """
    Verifica que la función principal de visualización crea los archivos de gráficos esperados.
    `tmp_path` es una fixture de pytest que provee un directorio temporal.
    """
    ruta_guardado = tmp_path / "graficos_escenario"
    generar_visualizaciones_escenario(datos_simulacion_completos, str(ruta_guardado))

    # Verificar que el directorio fue creado
    assert os.path.isdir(ruta_guardado)

    # Verificar que los archivos de gráficos existen
    archivos_esperados = [
        "vacunados_acumulados.png",
        "longitud_cola.png",
        "histograma_tiempos_espera.png"
    ]
    for archivo in archivos_esperados:
        assert os.path.isfile(ruta_guardado / archivo)

def test_plot_comparacion_escenarios_crea_archivo(metricas_comparacion_ejemplo, tmp_path):
    """
    Verifica que la función de comparación de escenarios crea el archivo de gráfico esperado.
    """
    ruta_guardado = tmp_path / "graficos_comparacion"
    os.makedirs(ruta_guardado) # La función de comparación no crea el dir, así que lo hacemos manualmente

    plot_comparacion_escenarios(
        metricas_por_escenario=metricas_comparacion_ejemplo,
        metrica='costos.costo_total_campana',
        titulo='Test Comparación Costos',
        ruta_guardado=str(ruta_guardado)
    )

    assert os.path.isfile(ruta_guardado / "comparacion_costos.costo_total_campana.png")

def test_visualizacion_con_dataframe_vacio(tmp_path):
    """
    Verifica que las funciones de visualización no fallen si reciben un DataFrame vacío.
    """
    ruta_guardado = tmp_path / "graficos_vacios"
    df_vacio = pd.DataFrame()

    # Usamos un bloque try/except para asegurar que no se lance ninguna excepción
    try:
        generar_visualizaciones_escenario(df_vacio, str(ruta_guardado))
    except Exception as e:
        pytest.fail(f"generar_visualizaciones_escenario falló con un DataFrame vacío: {e}")

    # Verificamos que el directorio se crea, pero no se generan los archivos de gráficos
    assert os.path.isdir(ruta_guardado)
    assert not os.path.isfile(ruta_guardado / "vacunados_acumulados.png")

def test_histograma_sin_tiempos_de_espera(tmp_path):
    """
    Verifica que la función de histograma no falle si no hay tiempos de espera (ej. todos > 0).
    """
    datos = {
        "tiempo_simulacion": [10, 20],
        "paciente_id": ["P1", "P2"],
        "evento": ["Vacunado", "Vacunado"],
        "longitud_cola_actual": [0, 0],
        "tiempo_espera_minutos": [0, 0], # Tiempos de espera son cero
        "tiempo_en_sistema_minutos": [3, 3],
    }
    df_sin_espera = pd.DataFrame(datos)
    ruta_guardado = tmp_path / "graficos_sin_espera"

    try:
        generar_visualizaciones_escenario(df_sin_espera, str(ruta_guardado))
    except Exception as e:
        pytest.fail(f"generar_visualizaciones_escenario falló con tiempos de espera cero: {e}")

    # El histograma no debería crearse porque la función tiene una guarda para esto
    assert not os.path.isfile(ruta_guardado / "histograma_tiempos_espera.png")
    # Pero los otros gráficos sí deberían crearse
    assert os.path.isfile(ruta_guardado / "vacunados_acumulados.png")
