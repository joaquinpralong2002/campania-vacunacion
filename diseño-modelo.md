# Diseño de modelo

Paso a paso para el diseño del modelo de simulación:

1\. Objetivos de la simulación de la campaña de vacunación.

Objetivos:

1\. Diseñar y analizar un modelo dinámico discreto en tiempo para una campaña de vacunación.  
 2\. Determinar si es posible vacunar a toda la población con la configuración actual de puestos.  
 3\. Estimar el tiempo necesario para vacunar a toda la población.  
 4\. Estimar el costo de incorporar más puestos de vacunación (cabinas).  
 5\. Evaluar si la política de asignación actual permite vacunar a la población objetivo sin generar colas masivas.  
 6\. Determinar cuántos puestos (cabinas) son necesarios para completar la vacunación en un plazo de 12 semanas.  
 7\. Modelar un esquema de 2 dosis y analizar cómo afecta la logística y el tiempo para la vacunación (primera dosis y esquema completo).  
 8\. Proponer y comparar, mediante simulación, políticas operativas para reducir el tiempo total de la campaña (ej. reasignación de dígitos, turnos virtuales, jornadas extraordinarias).  
 9\. Calcular el tiempo (en días y semanas) hasta vacunar al 70%, 80% y 100% de la población para diferentes escenarios.  
 10\. Obtener estadísticas de cola, como tiempo máximo/mínimo, longitud máxima/mínima, tasa de abandono y tiempo promedio de espera.

2\. Entidades Clave:

1. Puestos de Vacunación (Cabinas): Son los recursos que atienden a los pacientes. Su número es una variable clave en la simulación.
2. Pacientes: Son las personas que llegan al centro de vacunación para ser atendidas. Tienen características como tiempo de llegada y necesidad de vacunación.
3. Cola de Espera: Es el lugar donde los pacientes esperan si todos los puestos de vacunación están ocupados.  
   4\. Centro de Vacunación: El sistema general que engloba los puestos, las colas y el proceso de atención.

   3\. Flujo del Proceso (Eventos):

- Llegada de Pacientes: Los pacientes llegan al centro de vacunación siguiendo una distribución de probabilidad.
- Espera en Cola: Si todos los puestos están ocupados, el paciente entra en una cola de espera.
- Inicio de la Vacunación: Cuando un puesto se desocupa, el siguiente paciente en la cola (si hay) comienza su proceso de vacunación.
- Proceso de Vacunación: El tiempo que toma vacunar a un paciente, que puede ser constante o seguir una distribución (ej. Exponencial).
- Salida del Sistema: Una vez vacunado, el paciente abandona el centro.

![][image1]  
 4\. Parámetros y Variables del Modelo:

Parámetros del Modelo (Inputs Configurables): Estos son los valores que se definen antes de ejecutar la simulación y que se puede modificar para crear diferentes escenarios.

- Número de Puestos de Vacunación: Cantidad de cabinas disponibles para vacunar.

  - Valor base: 5\.

- Tasa de Llegada de Pacientes: Número de personas que llegan al centro por unidad de tiempo.

  - Valor base: 30 personas por minuto.

- Tiempo Promedio de Vacunación: Duración del servicio de vacunación para una persona.

  - Valor base: 3 minutos.

- Probabilidad de Reprogramación: Probabilidad de que una persona decida no esperar en la cola si la encuentra.

  - Valor base: 20% (0.20).

- Duración de la Jornada: El tiempo total que el centro está abierto cada día.

  - Valor base: 10 horas (de 8:00 a 18:00).

- Tasa de Asistencia: Porcentaje de personas que realmente asisten en su día asignado (para escenarios avanzados).

  - Valores para experimentar: 60%, 80%, 95%.

- Disponibilidad diaria de dosis

- Costos:
  - Costo Fijo por Cabina: $55,000 por día.
  - Costo por Dosis: $2,000 por dosis administrada.
  - Costo por Reprogramación: $300 por persona que reprograma.
  - Costo por Cabina Adicional: $150,000 (pago único).  

- Costos a estimar
  - Costo acumulado por día
  - Costo por persona vacunada
  - Costo por escenario
  - Comparación de eficiencia costo/tiempo entre escenarios

Variables y Métricas de Desempeño (Outputs): Estos son los valores que el modelo calculará y registrará durante y al final de la simulación para evaluar el rendimiento del sistema.

- Pacientes Vacunados: Número total de personas que han recibido la vacuna.
- Longitud de la Cola: Número de personas esperando en la cola en un momento dado.
- Longitud Mínima y Máxima de la Cola: El número más alto y más bajo de personas que estuvieron en la cola simultáneamente.
- Tiempo de Espera Promedio: El tiempo medio que un paciente pasa en la cola antes de ser atendido.
- Tiempo Mínimo y Máximo de Espera: El tiempo más largo y más corto que cualquier paciente tuvo que esperar.
- Número de Reprogramaciones: Cantidad total de personas que decidieron no esperar y solicitaron reprogramación.
- Tasa de abandono de cola: Personas que decidieron abandonar la cola y solicitar una reprogramación.
- Utilización de Puestos: Porcentaje del tiempo que los puestos de vacunación están ocupados.
- Costo Total Acumulado: Suma de todos los costos (cabinas, dosis, reprogramaciones) a lo largo de la simulación.
- Tiempo Total de Simulación: El tiempo transcurrido en la simulación (en minutos, horas o días) para alcanzar un objetivo (ej. vacunar al 80% de la población).
- Estadísticas de servicio: Tiempo promedio de vacunación, Tiempo máximo, mínimo.

Gráficos a generar:

- Vacunados acumulados vs. tiempo, cola acumulada vs. tiempo, ocupación diaria de puestos.

- Histograma de Tiempos de Espera:

  - La distribución de los tiempos de espera de los pacientes. El eje X sería el tiempo de espera en rangos (ej. 0-2 min, 2-4 min, etc.) y el eje Y la cantidad de pacientes en cada rango.
  - Por qué es útil: Permite ver no solo el promedio, sino cuántos pacientes esperaron mucho tiempo y cuántos fueron atendidos rápidamente. Es excelente para visualizar la experiencia del paciente.

- Gráfico de Tasa de Abandono (Reprogramaciones) a lo Largo del Día:

  - Qué muestra: Cómo cambia el número de personas que abandonan la cola en diferentes momentos del día. El eje X sería la hora del día y el eje Y el número de reprogramaciones.
  - Por qué es útil: Ayuda a identificar "horas pico" de frustración, que probablemente coinciden con los momentos de mayor longitud de cola. Podría justificar la asignación de más personal en esos horarios.

- Gráfico de Costo Acumulado vs. Tiempo:

  - Qué muestra: Cómo crece el costo total de la campaña a medida que pasan los días. El eje X es el tiempo (días) y el eje Y es el costo total en pesos.
  - Por qué es útil: Visualiza el impacto financiero a lo largo del tiempo y permite comparar directamente la evolución del costo entre diferentes escenarios (ej. con 5 vs. 7 cabinas).

- Gráfico de Dispersión (Scatter Plot): Tiempo de Espera vs. Longitud de Cola:

  - Qué muestra: Cada punto representa un paciente, mostrando la longitud de la cola que había cuando llegó (eje X) y cuánto tiempo terminó esperando (eje Y).
  - Por qué es útil: Demuestra visualmente la correlación directa entre el tamaño de la cola y el tiempo de espera individual, reforzando las conclusiones sobre la necesidad de gestionar la cola.

- Gráfico de Barras Comparativo de Métricas Clave por Escenario:
  - Qué muestra: Compara métricas finales importantes (ej. tiempo total para vacunar al 100%, costo total, tiempo de espera promedio) entre los diferentes escenarios que simules (escenario base, más cabinas, etc.).
  - Por qué es útil: Es la forma más clara y directa de presentar tus conclusiones finales y justificar tus recomendaciones sobre qué escenario es el más eficiente.
