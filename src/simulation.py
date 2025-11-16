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
    dia_semana = dia % 5
    digitos_hoy = config["asignacion_digitos_dias"].get(dia_semana, [])
    
    if not digitos_hoy:
        return

    pacientes_por_digito = config["poblacion_total"] / 10
    pacientes_esperados_hoy = len(digitos_hoy) * pacientes_por_digito
    pacientes_que_asisten = int(pacientes_esperados_hoy * config["tasa_asistencia"])

    minutos_operacion = config["horas_operacion_por_dia"] * 60
    if pacientes_que_asisten > 0:
        tasa_llegada_promedio = pacientes_que_asisten / minutos_operacion
        
        # --- OPTIMIZACIÓN: Pre-generar todos los tiempos y dígitos de una vez ---
        tiempos_entre_llegadas = [random.expovariate(tasa_llegada_promedio) for _ in range(pacientes_que_asisten)]
        digitos_pacientes = random.choices(digitos_hoy, k=pacientes_que_asisten)

        for i in range(pacientes_que_asisten):
            # Si el objetivo ya se alcanzó, no generar más llegadas
            if config["estado_sim"]["objetivo_alcanzado"].triggered:
                break
            
            yield env.timeout(tiempos_entre_llegadas[i])
            
            id_paciente = f"Dia{dia}_Digito{digitos_pacientes[i]}_Pac{i}"
            env.process(proceso_paciente(env, id_paciente, centro_vacunacion, config, dia, digitos_pacientes[i], datos_simulacion))

def fuente_de_llegadas(env, centro_vacunacion, config, duracion_dias, datos_simulacion):
    """
    Proceso maestro que orquesta la generación de llegadas para cada día de la simulación.
    """
    minutos_por_dia = config["horas_operacion_por_dia"] * 60
    for dia in range(duracion_dias):
        # Si el objetivo ya se alcanzó, detener la fuente de llegadas
        if config["estado_sim"]["objetivo_alcanzado"].triggered:
            break
        
        env.process(generar_llegadas_por_dia(env, dia, centro_vacunacion, config, datos_simulacion))
        yield env.timeout(minutos_por_dia)


def proceso_paciente(env, nombre_paciente, centro_vacunacion, config, dia, digito_dni, datos_simulacion):
    """Modela el flujo completo de un paciente en el centro de vacunación."""
    tiempo_llegada = env.now
    
    if centro_vacunacion.count == centro_vacunacion.capacity:
        if random.random() < config["probabilidad_reprogramacion"]:
            registrar_evento(env, nombre_paciente, "Reprogramacion", len(centro_vacunacion.queue), 0, 0, dia, digito_dni, datos_simulacion)
            return

    with centro_vacunacion.request() as solicitud:
        yield solicitud
        tiempo_inicio_servicio = env.now
        tiempo_espera = tiempo_inicio_servicio - tiempo_llegada
        
        tiempo_vacunacion = random.expovariate(1.0 / config["tiempo_promedio_vacunacion_minutos"])
        yield env.timeout(tiempo_vacunacion)
        
        tiempo_salida = env.now
        tiempo_en_sistema = tiempo_salida - tiempo_llegada
        
        registrar_evento(env, nombre_paciente, "Vacunado", len(centro_vacunacion.queue), tiempo_espera, tiempo_en_sistema, dia, digito_dni, datos_simulacion)

        # --- NUEVO: Comprobar si se alcanzó el objetivo de vacunación ---
        estado_sim = config["estado_sim"]
        estado_sim["contador_vacunados"] += 1
        
        if estado_sim["contador_vacunados"] >= config["poblacion_total"]:
            if not estado_sim["objetivo_alcanzado"].triggered:
                estado_sim["objetivo_alcanzado"].succeed()

def registrar_evento(env, paciente_id, evento, longitud_cola, tiempo_espera, tiempo_sistema, dia, digito_dni, datos_simulacion):
    """Registra un evento clave de la simulación."""
    datos_simulacion.append((
        env.now,
        dia,
        paciente_id,
        digito_dni,
        evento,
        longitud_cola,
        tiempo_espera,
        tiempo_sistema,
    ))

def ejecutar_simulacion(config_escenario: dict, duracion_dias: int):
    """Configura y ejecuta un escenario completo de la simulación."""
    datos_simulacion = []
    env = simpy.Environment()

    # --- NUEVO: Añadir estado para parada temprana ---
    estado_sim = {
        "contador_vacunados": 0,
        "objetivo_alcanzado": env.event()
    }
    config_escenario["estado_sim"] = estado_sim

    centro_vacunacion = simpy.Resource(env, capacity=config_escenario["num_cabinas"])
    
    env.process(fuente_de_llegadas(env, centro_vacunacion, config_escenario, duracion_dias, datos_simulacion))
    
    duracion_total_minutos = config_escenario["horas_operacion_por_dia"] * 60 * duracion_dias
    
    # --- MODIFICADO: Correr hasta que se cumpla el objetivo o el tiempo límite ---
    # Se usa el operador | (OR) para combinar eventos en SimPy
    env.run(until=estado_sim["objetivo_alcanzado"] | env.timeout(duracion_total_minutos))

    columnas = [
        "tiempo_simulacion", "dia", "paciente_id", "digito_dni", "evento",
        "longitud_cola_actual", "tiempo_espera_minutos", "tiempo_en_sistema_minutos"
    ]
    return pd.DataFrame(datos_simulacion, columns=columnas)

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
