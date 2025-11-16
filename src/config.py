# src/config.py

class ConfiguracionSimulacion:
    """
    Parámetros de configuración para la simulación de la campaña de vacunación.
    """

    # Parámetros del Escenario Base - en base a contexto del problema
    ESCENARIO_BASE = {
        "num_cabinas": 5,  # Número de puestos de vacunación
        "tasa_llegada_por_minuto": 30,  # Pacientes que llegan por minuto
        "tiempo_promedio_vacunacion_minutos": 3,  # Tiempo promedio para vacunar a una persona
        "probabilidad_reprogramacion": 0.20,  # Probabilidad de que un paciente reprograme si la cola es larga
        "horas_operacion_por_dia": 10,  # Horas de operación diarias (8:00 a 18:00)
        "tasa_asistencia": 0.70,  # Porcentaje de personas que realmente asisten en su día asignado
        "dosis_diarias_disponibles": float('inf'), # Dosis diarias disponibles, se asume infinito si no hay límite
        "tamano_poblacion": 198000, # Tamaño de la población a vacunar (ejemplo, necesita ser definido para "Concordia")
        "dias_simulacion": 365, # Días máximos para ejecutar la simulación
    }

    # Parámetros de Costos
    COSTOS = {
        "costo_fijo_por_cabina_por_dia": 55000,
        "costo_por_dosis": 2000,
        "costo_por_reprogramacion": 300,
        "costo_por_cabina_adicional_una_vez": 150000,   # cada cabina nueva a alquilar 150.000 por vez
        "costo_por_minuto_espera_por_persona": 3
    }


    # Configuraciones de escenarios específicos
    # Cada escenario es un diccionario predefinido que contiene parametros de configuracion especificos de cada escenario
    # Escenario con 10 cabinas
    ESCENARIO_10_CABINAS = ESCENARIO_BASE.copy()
    ESCENARIO_10_CABINAS["num_cabinas"] = 10

    ESCENARIO_20_CABINAS = ESCENARIO_BASE.copy()
    ESCENARIO_20_CABINAS["num_cabinas"] = 20
    # Escenarios con 60, 80 y 95% de tasa de asistencia
    
    # Tasa de asistencia del 60%
    ESCENARIO_BASE_60_ASISTENCIA = ESCENARIO_BASE.copy()
    ESCENARIO_BASE_60_ASISTENCIA["tasa_asistencia"] = 0.60
    # Tasa de asistencia del 80%
    ESCENARIO_80_ASISTENCIA = ESCENARIO_BASE.copy()
    ESCENARIO_80_ASISTENCIA["tasa_asistencia"] = 0.80 
    # Tasa de asistencia del 95%
    ESCENARIO_BASE_95_ASISTENCIA = ESCENARIO_BASE.copy()
    ESCENARIO_BASE_95_ASISTENCIA["tasa_asistencia"] = 0.95

    #Escenario acelerado con tasa de llegada por minuto de 50 pacientes y el tiempo de vacunacion 2 minutos
    ESCENARIO_ACELERADO = ESCENARIO_BASE.copy()
    ESCENARIO_ACELERADO["tiempo_promedio_vacunacion_minutos"] = 2

    # Para el esquema de dos dosis, esto podría implicar una lógica más compleja dentro del modelo de simulación
    # en lugar de solo un parámetro de configuración, pero podemos añadir un indicador aquí.
    ESCENARIO_DOS_DOSIS = ESCENARIO_BASE.copy()
    ESCENARIO_DOS_DOSIS["esquema_dos_dosis_habilitado"] = True
    ESCENARIO_DOS_DOSIS["intervalo_dos_dosis_dias"] = 21

    ESCENARIO_HORARIO_EXTENDIDO = ESCENARIO_BASE.copy()
    ESCENARIO_HORARIO_EXTENDIDO["horas_operacion_por_dia"] = 12  # Operación de 8:00 a 20:00

    #Metodo estatico que devuelve un diccionario con los parámetros de configuración específicos para un escenario de simulación de vacunación dado.
    @staticmethod
    def obtener_configuracion_escenario(nombre_escenario: str) -> dict:
        """
        Devuelve la configuración para un nombre de escenario dado.
        """
        if nombre_escenario == "base":
            return ConfiguracionSimulacion.ESCENARIO_BASE
        elif nombre_escenario == "10_cabinas":
            return ConfiguracionSimulacion.ESCENARIO_10_CABINAS
        elif nombre_escenario == "20_cabinas":
            return ConfiguracionSimulacion.ESCENARIO_20_CABINAS
        elif nombre_escenario == "80_asistencia":
            return ConfiguracionSimulacion.ESCENARIO_80_ASISTENCIA
        elif nombre_escenario == "95_asistencia":
            return ConfiguracionSimulacion.ESCENARIO_BASE_95_ASISTENCIA
        elif nombre_escenario == "dos_dosis":
            return ConfiguracionSimulacion.ESCENARIO_DOS_DOSIS
        elif nombre_escenario == "acelerado":
            return ConfiguracionSimulacion.ESCENARIO_ACELERADO
        elif nombre_escenario == "horario_extendido":
            return ConfiguracionSimulacion.ESCENARIO_HORARIO_EXTENDIDO
        else:
            raise ValueError(f"Escenario desconocido: {nombre_escenario}")

