# tests/test_config.py

import pytest
from src.config import ConfiguracionSimulacion

def test_obtener_configuracion_escenario_base():
    """Verifica que se pueda obtener la configuración del escenario base correctamente."""
    config = ConfiguracionSimulacion.obtener_configuracion_escenario("base")
    assert isinstance(config, dict)
    assert config["num_cabinas"] == 5


def test_obtener_configuracion_escenario_desconocido():
    """Verifica que se lance un ValueError para un escenario que no existe."""
    with pytest.raises(ValueError) as excinfo:
        ConfiguracionSimulacion.obtener_configuracion_escenario("escenario_inexistente")
    assert "Escenario desconocido" in str(excinfo.value)
