# src/simulation.py

import simpy
import random
import pandas as pd
from src.config import ConfiguracionSimulacion

def generar_llegadas_por_dia(env, dia, centro_vacunacion, config, datos_simulacion):
    """
    Genera las llegadas de pacientes para un día específico, con tiempos relativos
    al inicio de ese día. Esta función es iniciada por un proceso maestro.
    """
    # Determinar los dígitos del DNI asignados para el día de la semana actual
    dia_semana = dia % 5
    digitos_hoy = config["asignacion_digitos_dias"].get(dia_semana, [])
    
    # Si no hay dígitos asignados para hoy, no generar llegadas
    if not digitos_hoy:
        return

    # Calcular el número esperado de pacientes que asistirán hoy
    pacientes_por_digito = config["poblacion_total"] / 10
    pacientes_esperados_hoy = len(digitos_hoy) * pacientes_por_digito
    pacientes_que_asisten = int(pacientes_esperados_hoy * config["tasa_asistencia"])

    minutos_operacion = config["horas_operacion_por_dia"] * 60
    if pacientes_que_asisten > 0:
        # Tasa de llegada promedio (pacientes por minuto) para el día.
        tasa_llegada_promedio = pacientes_que_asisten / minutos_operacion
        
        for i in range(pacientes_que_asisten):
            # El tiempo entre llegadas para un proceso de Poisson sigue una distribución exponencial.
            tiempo_entre_llegadas = random.expovariate(tasa_llegada_promedio)
            # Esperar hasta la próxima llegada
            yield env.timeout(tiempo_entre_llegadas)
            
            digito_paciente = random.choice(digitos_hoy)
            id_paciente = f"Dia{dia}_Digito{digito_paciente}_Pac{i}"
            # Iniciar el proceso del paciente
            env.process(proceso_paciente(env, id_paciente, centro_vacunacion, config, dia, digito_paciente, datos_simulacion))

def fuente_de_llegadas(env, centro_vacunacion, config, duracion_dias, datos_simulacion):
    """
    Proceso maestro que orquesta la generación de llegadas para cada día de la simulación.
    Este modelo se basa en la asignación de días de vacunación según el último dígito del DNI.

    Supuesto clave: Las llegadas de pacientes se modelan como un proceso de Poisson.
    Esto implica que los tiempos entre llegadas consecutivas siguen una distribución exponencial.
    Este modelo es apropiado para situaciones donde los eventos (llegadas de pacientes)
    ocurren de forma independiente y a una tasa promedio constante en un intervalo de tiempo dado,
    lo cual es una suposición común y razonable para la llegada de individuos a un servicio.
    """
    minutos_por_dia = config["horas_operacion_por_dia"] * 60
    for dia in range(duracion_dias):
        # Inicia el generador de llegadas para el día actual
        env.process(generar_llegadas_por_dia(env, dia, centro_vacunacion, config, datos_simulacion))
        # Espera a que termine el día para iniciar el siguiente
        yield env.timeout(minutos_por_dia)


def proceso_paciente(env, nombre_paciente, centro_vacunacion, config, dia, digito_dni, datos_simulacion):
    """Modela el flujo completo de un paciente en el centro de vacunación."""
    # Registrar la llegada
    tiempo_llegada = env.now
    
    # Verificar si el centro está lleno y decidir reprogramar
    if centro_vacunacion.count == centro_vacunacion.capacity:
        if random.random() < config["probabilidad_reprogramacion"]:
            registrar_evento(env, nombre_paciente, "Reprogramacion", len(centro_vacunacion.queue), 0, 0, dia, digito_dni, datos_simulacion)
            return

    # Solicitar un puesto de vacunación
    with centro_vacunacion.request() as solicitud:

        # Esperar hasta que se asigne un puesto
        yield solicitud
        # Cuando una cabina se desocupa, el paciente la toma
        tiempo_inicio_servicio = env.now
        tiempo_espera = tiempo_inicio_servicio - tiempo_llegada
        
        # Simular el tiempo de vacunación, que sigue una distribución exponencial por la variabilidad del servicio
        tiempo_vacunacion = random.expovariate(1.0 / config["tiempo_promedio_vacunacion_minutos"])
        # El paciente está siendo vacunado
        yield env.timeout(tiempo_vacunacion)
        
        # Registrar la vacunación completada
        tiempo_salida = env.now
        tiempo_en_sistema = tiempo_salida - tiempo_llegada
        
        # Se registra el evento de vacunación
        registrar_evento(env, nombre_paciente, "Vacunado", len(centro_vacunacion.queue), tiempo_espera, tiempo_en_sistema, dia, digito_dni, datos_simulacion)

def registrar_evento(env, paciente_id, evento, longitud_cola, tiempo_espera, tiempo_sistema, dia, digito_dni, datos_simulacion):
    """Registra un evento clave de la simulación."""
    datos_simulacion.append({
        "tiempo_simulacion": env.now,
        "dia": dia,
        "paciente_id": paciente_id,
        "digito_dni": digito_dni,
        "evento": evento,
        "longitud_cola_actual": longitud_cola,
        "tiempo_espera_minutos": tiempo_espera,
        "tiempo_en_sistema_minutos": tiempo_sistema,
    })

def ejecutar_simulacion(config_escenario: dict, duracion_dias: int):
    """Configura y ejecuta un escenario completo de la simulación."""
    datos_simulacion = []

    # Crear el entorno de simulación y las cabinas de vacunación
    env = simpy.Environment()
    centro_vacunacion = simpy.Resource(env, capacity=config_escenario["num_cabinas"])
    
    # Iniciar el proceso maestro que gestiona las llegadas
    env.process(fuente_de_llegadas(env, centro_vacunacion, config_escenario, duracion_dias, datos_simulacion))
    
    # Ejecutar la simulación por la duración total de minutos
    duracion_total_minutos = config_escenario["horas_operacion_por_dia"] * 60 * duracion_dias
    env.run(until=duracion_total_minutos)

    # Se devuelve un DataFrame con todos los eventos registrados
    return pd.DataFrame(datos_simulacion)

# --- Bloque para Pruebas ---
if __name__ == '__main__':
    config_base = ConfiguracionSimulacion.obtener_configuracion_escenario("base")
    print("Ejecutando simulación de prueba para el escenario 'base' (duración: 5 días)...")
    
    resultados_df = ejecutar_simulacion(config_base, duracion_dias=5)
    
    print(f"Simulación completada. Total de eventos registrados: {len(resultados_df)}")
    
    if not resultados_df.empty:
        print("\n--- Primeros 5 eventos registrados ---")
        print(resultados_df.head())
        
        vacunados_df = resultados_df[resultados_df["evento"] == "Vacunado"]
        reprogramados_df = resultados_df[resultados_df["evento"] == "Reprogramacion"]
        
        print(f"\nTotal de pacientes vacunados: {len(vacunados_df)}")
        print(f"Total de pacientes que reprogramaron: {len(reprogramados_df)}")
        
        if not vacunados_df.empty:
            tiempo_espera_promedio = vacunados_df['tiempo_espera_minutos'].mean()
            print(f"Tiempo de espera promedio para ser vacunado: {tiempo_espera_promedio:.2f} minutos")
            
            print("\n--- Análisis por Día ---")
            vacunados_por_dia = resultados_df[resultados_df['evento'] == 'Vacunado'].groupby('dia').size()
            print("Pacientes vacunados por día:")
            print(vacunados_por_dia)
