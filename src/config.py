# src/config.py

class ConfiguracionSimulacion:
    """
    Parámetros de configuración para la simulación de la campaña de vacunación.
    """

    # Parámetros del Escenario Base
    ESCENARIO_BASE = {
        "num_cabinas": 5,  # Número de puestos de vacunación
        "tasa_llegada_por_minuto": 30,  # Pacientes que llegan por minuto
        "tiempo_promedio_vacunacion_minutos": 3,  # Tiempo promedio para vacunar a una persona
        "probabilidad_reprogramacion": 0.20,  # Probabilidad de que un paciente reprograme si la cola es larga
        "horas_operacion_por_dia": 10,  # Horas de operación diarias (8:00 a 18:00)
        "tasa_asistencia": 0.70,  # Porcentaje de personas que realmente asisten en su día asignado
        "dosis_diarias_disponibles": float('inf'), # Dosis diarias disponibles, se asume infinito si no hay límite
        "tamano_poblacion": 100000, # Tamaño de la población a vacunar (ejemplo, necesita ser definido para "Concordia")
        "dias_simulacion": 365, # Días máximos para ejecutar la simulación
    }

    # Parámetros de Costos
    COSTOS = {
        "costo_fijo_por_cabina_por_dia": 55000,
        "costo_por_dosis": 2000,
        "costo_por_reprogramacion": 300,
        "costo_por_cabina_adicional_una_vez": 150000,
        "costo_por_minuto_espera_por_persona": 3
    }

    # Configuraciones de escenarios específicos
    # Ejemplo: Escenario con 7 cabinas
    ESCENARIO_7_CABINAS = ESCENARIO_BASE.copy()
    ESCENARIO_7_CABINAS["num_cabinas"] = 7

    # Ejemplo: Escenario con 80% de tasa de asistencia
    ESCENARIO_80_ASISTENCIA = ESCENARIO_BASE.copy()
    ESCENARIO_80_ASISTENCIA["tasa_asistencia"] = 0.80 # Este parámetro necesita ser integrado en la lógica de simulación

    # Añadir más escenarios según sea necesario
    # Para el esquema de dos dosis, esto podría implicar una lógica más compleja dentro del modelo de simulación
    # en lugar de solo un parámetro de configuración, pero podemos añadir un indicador aquí.
    ESCENARIO_DOS_DOSIS = ESCENARIO_BASE.copy()
    ESCENARIO_DOS_DOSIS["esquema_dos_dosis_habilitado"] = True
    ESCENARIO_DOS_DOSIS["intervalo_dos_dosis_dias"] = 21


    @staticmethod
    def obtener_configuracion_escenario(nombre_escenario: str) -> dict:
        """
        Devuelve la configuración para un nombre de escenario dado.
        """
        if nombre_escenario == "base":
            return ConfiguracionSimulacion.ESCENARIO_BASE
        elif nombre_escenario == "7_cabinas":
            return ConfiguracionSimulacion.ESCENARIO_7_CABINAS
        elif nombre_escenario == "80_asistencia":
            return ConfiguracionSimulacion.ESCENARIO_80_ASISTENCIA
        elif nombre_escenario == "dos_dosis":
            return ConfiguracionSimulacion.ESCENARIO_DOS_DOSIS
        else:
            raise ValueError(f"Escenario desconocido: {nombre_escenario}")
