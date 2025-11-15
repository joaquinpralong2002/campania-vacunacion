# src/simulation.py

import simpy # librería principal para la simulación de eventos discretos. Nos proporciona el entorno (Environment), los procesos y los recursos
import random # para introducir aleatoriedad en el modelo, como el tiempo entre llegadas de pacientes o el tiempo que toma una vacunación
import pandas as pd # para almacenar y analizar los datos generados por la simulación en un DataFrame
from src.config import ConfiguracionSimulacion # importamos la clase desde el archivo config.py para poder acceder a los parámetros de cada escenario

# Lista para recolectar datos de la simulación. Cada vez que ocurra un evento importante 
# (un paciente es vacunado, uno reprograma, etc.), guardamos un registro en esta lista.
datos_simulacion = []

def generar_llegadas(env, centro_vacunacion, config):
    """Genera la llegada de pacientes al centro de vacunación."""
    id_paciente = 0
    while True:
        # El tiempo entre llegadas sigue una distribución exponencial para un proceso de Poisson
        tasa_llegada = config["tasa_llegada_por_minuto"]

        # Tiempo de pausa que simula el tiempo entre la llegada de un paciente y el siguiente.
        yield env.timeout(random.expovariate(tasa_llegada))

        id_paciente += 1
        
        # Se considera la tasa de asistencia para determinar si el paciente llega
        # Se genera un número aleatorio entre 0 y 1. Si ese número es menor que
        # la tasa de asistencia (por ejemplo, 0.80), entonces el paciente asiste.
        if random.random() < config.get("tasa_asistencia", 1.0):
            # Si el paciente asiste, se crea un nuevo proceso para él.
            env.process(proceso_paciente(env, f'Paciente_{id_paciente}', centro_vacunacion, config))

def proceso_paciente(env, nombre_paciente, centro_vacunacion, config):
    """Modela el flujo completo de un paciente, incluyendo una o dos dosis."""
    
    # --- Proceso para la Primera Dosis ---
    tiempo_llegada_d1 = env.now
    
    # Decisión de reprogramar para la primera dosis
    if centro_vacunacion.count == centro_vacunacion.capacity:
        if random.random() < config["probabilidad_reprogramacion"]:
            longitud_cola_al_llegar = len(centro_vacunacion.queue)
            registrar_evento(env, nombre_paciente, "Reprogramacion", longitud_cola_al_llegar, 0, 0, dosis_numero=1)
            return

    with centro_vacunacion.request() as solicitud_d1:
        yield solicitud_d1
        
        tiempo_inicio_servicio_d1 = env.now
        tiempo_espera_d1 = tiempo_inicio_servicio_d1 - tiempo_llegada_d1
        
        tiempo_vacunacion_d1 = random.expovariate(1.0 / config["tiempo_promedio_vacunacion_minutos"])
        yield env.timeout(tiempo_vacunacion_d1)
        
        tiempo_salida_d1 = env.now
        tiempo_en_sistema_d1 = tiempo_salida_d1 - tiempo_llegada_d1
        
        longitud_cola_al_salir_d1 = len(centro_vacunacion.queue)
        registrar_evento(env, nombre_paciente, "Vacunado", longitud_cola_al_salir_d1, tiempo_espera_d1, tiempo_en_sistema_d1, dosis_numero=1)

    # --- Programación y Proceso para la Segunda Dosis (si aplica) ---
    if config.get("esquema_dos_dosis_habilitado", False):
        # El paciente "espera" el intervalo para su segunda dosis
        intervalo_minutos = config["intervalo_dos_dosis_dias"] * config["horas_operacion_por_dia"] * 60
        yield env.timeout(intervalo_minutos)
        
        # --- El paciente "regresa" para la segunda dosis ---
        tiempo_llegada_d2 = env.now
        
        # Para la segunda dosis, se asume que el paciente no reprograma y espera lo necesario.
        with centro_vacunacion.request() as solicitud_d2:
            yield solicitud_d2
            
            tiempo_inicio_servicio_d2 = env.now
            tiempo_espera_d2 = tiempo_inicio_servicio_d2 - tiempo_llegada_d2
            
            tiempo_vacunacion_d2 = random.expovariate(1.0 / config["tiempo_promedio_vacunacion_minutos"])
            yield env.timeout(tiempo_vacunacion_d2)
            
            tiempo_salida_d2 = env.now
            tiempo_en_sistema_d2 = tiempo_salida_d2 - tiempo_llegada_d2
            
            longitud_cola_al_salir_d2 = len(centro_vacunacion.queue)
            registrar_evento(env, nombre_paciente, "Vacunado", longitud_cola_al_salir_d2, tiempo_espera_d2, tiempo_en_sistema_d2, dosis_numero=2)

def registrar_evento(env, paciente_id, evento, longitud_cola, tiempo_espera, tiempo_sistema, dosis_numero=None):
    """Registra un evento clave de la simulación en la lista de datos. Toma la información de un evento (quién, qué pasó, cuándo, cuánto esperó, etc.) 
    y la añade como un diccionario a la lista global datos_simulacion."""
    datos_simulacion.append({
        "tiempo_simulacion": env.now,
        "paciente_id": paciente_id,
        "evento": evento,
        "longitud_cola_actual": longitud_cola,
        "tiempo_espera_minutos": tiempo_espera,
        "tiempo_en_sistema_minutos": tiempo_sistema,
        "dosis_numero": dosis_numero
    })

def ejecutar_simulacion(config_escenario: dict, duracion_dias: int):
    """
    Configura y ejecuta un escenario completo de la simulación. 
    
    Args:
        config_escenario (dict): Diccionario con los parámetros del escenario.
        duracion_dias (int): Número de días que durará la simulación.
        
    Returns:
        pd.DataFrame: Un DataFrame de pandas con los datos recolectados durante la simulación.
    """
    # Limpia los datos de cualquier ejecución anterior.
    datos_simulacion.clear()
    
    # Crea el entorno de simulación, que es el reloj y gestor de todos los eventos
    env = simpy.Environment()
    
    # Crear el recurso que representa las cabinas de vacunación
    centro_vacunacion = simpy.Resource(env, capacity=config_escenario["num_cabinas"])
    
    # Iniciar el proceso que genera las llegadas de pacientes
    env.process(generar_llegadas(env, centro_vacunacion, config_escenario))
    
    # Calcular la duración total de la simulación en minutos
    duracion_total_minutos = config_escenario["horas_operacion_por_dia"] * 60 * duracion_dias

    # Línea que inicia la simulación. Le dice a SimPy que empiece a avanzar el tiempo y a ejecutar los eventos hasta que se
    # alcance la duración total de la simulación en minutos.
    env.run(until=duracion_total_minutos)
    
    # Una vez que la simulación termina, convierte la lista de diccionarios en un DataFrame de Pandas, que es
    # utilizado para el análisis posterior.
    return pd.DataFrame(datos_simulacion)

# --- Bloque para Pruebas ---
if __name__ == '__main__':
    # Cargar la configuración para un escenario de prueba (ej. "base")
    config_base = ConfiguracionSimulacion.obtener_configuracion_escenario("base")
    
    print("Ejecutando simulación de prueba para el escenario base (duración: 1 día)...")
    
    # Ejecutar la simulación para un solo día a modo de prueba
    resultados_df = ejecutar_simulacion(config_base, duracion_dias=1)
    
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
