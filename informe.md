# Informe de Simulación: Análisis y Optimización de una Campaña de Vacunación

**Autores:** [Tu Nombre/Nombres]
**Fecha:** 16 de noviembre de 2025

---

## 1. Introducción

La gestión de campañas de vacunación masiva presenta un desafío logístico significativo donde la correcta asignación de recursos es fundamental. Una planificación deficiente puede conducir a aglomeraciones, altos tiempos de espera y, en consecuencia, a la insatisfacción ciudadana y a retrasos en la inmunización de la población.

Este informe presenta un análisis exhaustivo de una campaña de vacunación para una población de 198,000 personas, utilizando un modelo de simulación de eventos discretos. El objetivo principal es desarrollar y analizar dicho modelo para evaluar el rendimiento del sistema bajo diversas configuraciones y proponer recomendaciones operativas que optimicen el proceso. Para ello, se construyó un simulador en Python con la librería SimPy, que permite analizar el impacto de variar parámetros clave como el número de puestos de vacunación y la tasa de asistencia.

Se evaluaron múltiples escenarios para determinar una configuración de recursos que equilibre la eficiencia operativa, los costos y la calidad del servicio. Los objetivos específicos del estudio incluyen:
- Estimar el tiempo necesario para alcanzar hitos de vacunación (70%, 80% y 100%).
- Evaluar el impacto del número de cabinas en las métricas de rendimiento (tiempos de espera, longitud de cola, tasa de abandono).
- Analizar la relación costo-beneficio de añadir recursos.
- Determinar el número de puestos necesarios para completar la campaña en un plazo objetivo (ej. 12 semanas).

---

## 2. Metodología y Modelo de Simulación

### 2.1. Modelo Conceptual y Supuestos

El sistema se modeló como un centro de atención con múltiples servidores (puestos de vacunación) y una única cola de espera.

- **Entidades:** Las entidades clave son los **Pacientes**, que llegan al sistema, y los **Puestos de Vacunación** (cabinas), que son los recursos que proveen el servicio.
- **Flujo del Proceso:**
    1.  **Llegada:** Los pacientes llegan al centro siguiendo una distribución de probabilidad.
    2.  **Decisión de Espera:** Al llegar, si la cola es percibida como muy larga (modelado con una probabilidad), el paciente puede optar por abandonar el sistema y reprogramar.
    3.  **Cola de Espera:** Si decide esperar, el paciente se une a la cola.
    4.  **Servicio:** Cuando un puesto de vacunación se desocupa, atiende al siguiente paciente en la cola. El tiempo de servicio sigue una distribución de probabilidad.
    5.  **Salida:** Una vez vacunado, el paciente abandona el sistema.

- **Supuestos del Modelo:**
    - La población total a vacunar es de 198,000 personas.
    - El horario de atención es de 10 horas diarias (8:00 a 18:00), 5 días a la semana.
    - La llegada de pacientes se distribuye a lo largo de la jornada según una tasa promedio.
    - La probabilidad de que un paciente abandone la cola (`probabilidad_reprogramacion`) es del 20%, independiente de la longitud real de la cola.
    - No se modelan interrupciones del servicio (descansos, fallos, etc.).
    - Existe una disponibilidad ilimitada de dosis diarias para los asistentes.

### 2.2. Justificación de Modelado de Aleatoriedad

La correcta modelización de la aleatoriedad es un criterio fundamental para la validez de la simulación.

- **Generador de Números Pseudoaleatorios (PRNG):** Se utilizó el generador **Mersenne Twister**, implementado en el módulo `random` de Python. Se eligió este PRNG por ser el estándar de facto en la simulación científica, gracias a sus robustas propiedades estadísticas: un período de recurrencia extremadamente largo (2^19937-1) y la equidistribución de sus secuencias en altas dimensiones. Esto asegura que los resultados no estén sesgados por la calidad del generador.

- **Distribución de Llegada de Pacientes (Proceso de Poisson):** El tiempo entre llegadas de pacientes se modeló con una **distribución exponencial** (`random.expovariate`). Esta elección es estándar para simular un **Proceso de Poisson**, donde los eventos ocurren de forma independiente a una tasa promedio constante. La distribución exponencial captura la variabilidad inherente a las llegadas reales (a veces varios pacientes juntos, a veces pausas), lo cual es crucial para un modelo realista.

- **Distribución del Tiempo de Servicio:** El tiempo de vacunación también se modeló con una **distribución exponencial**. Aunque el proceso tiene un promedio definido, esta distribución introduce una variabilidad realista que refleja pequeñas diferencias en el servicio o entre pacientes. Esto proporciona una estimación más precisa de las métricas de cola y espera que un tiempo de servicio constante.

### 2.3. Parámetros de Entrada del Modelo

Los parámetros clave, extraídos de `src/config.py`, se resumen en la siguiente tabla:

| Parámetro                             | Valor Base | Descripción                               |
| ------------------------------------- | ---------- | ----------------------------------------- |
| Número de Cabinas                     | 5          | Puestos de vacunación disponibles.        |
| Tiempo Promedio de Vacunación (min)   | 3          | Duración media del servicio por paciente. |
| Horas de Operación por Día            | 10         | Jornada de trabajo del centro.            |
| Tasa de Asistencia                    | 70%        | Porcentaje de citados que asisten.        |
| Probabilidad de Reprogramación        | 20%        | Prob. de abandono si hay cola.            |
| Población Total                       | 198,000    | Universo total de personas a vacunar.     |

---

## 3. Diseño Experimental y Escenarios

Para evaluar el sistema, se comparó un **Escenario Base** con los parámetros por defecto contra varias alternativas, tal como se define en el código (`src/main.py` y `src/config.py`):

- **Escenario Base:** Configuración inicial con 5 cabinas y 70% de asistencia.
- **Escenario 10 Cabinas:** Se duplica el número de puestos a 10 para medir el impacto en la descongestión.
- **Escenario 95% Asistencia:** Se analiza el efecto de una campaña de concientización exitosa, elevando la asistencia al 95%.
- **Escenario Acelerado:** Se simula una mejora en el proceso, reduciendo el tiempo de vacunación a 2 minutos.
- **Escenario Horario Extendido:** La jornada laboral se amplía a 12 horas diarias.
- **Escenario Objetivo 12 Semanas:** Se calcula el número de cabinas teóricas (17) para cumplir la meta en 12 semanas y se simula ese escenario.

---

## 4. Resultados y Análisis

A continuación, se presentan los resultados obtenidos de la ejecución de los escenarios. Las métricas y gráficos fueron generados por los módulos `analysis.py` y `visualization.py`.

### 4.1. Métricas de Rendimiento y Tiempos

*(Presentar aquí la tabla comparativa principal. Los valores deben ser llenados con los resultados de la simulación)*

**Tabla 1: Comparativa de Métricas Clave por Escenario**

| Métrica                       | Escenario Base | 10 Cabinas | 95% Asistencia | ... (otros escenarios) |
| ----------------------------- | -------------- | ---------- | -------------- | ---------------------- |
| Tiempo Espera Prom. (min)     | [Valor]        | [Valor]    | [Valor]        | [Valor]                |
| Longitud Cola Máx.            | [Valor]        | [Valor]    | [Valor]        | [Valor]                |
| Tasa de Abandono (%)          | [Valor]        | [Valor]    | [Valor]        | [Valor]                |
| Días para 100% Población      | [Valor]        | [Valor]    | [Valor]        | [Valor]                |
| Utilización de Cabinas (%)    | [Valor]        | [Valor]    | [Valor]        | [Valor]                |

### 4.2. Análisis de Costos

*(Presentar aquí la tabla de costos)*

**Tabla 2: Análisis Comparativo de Costos por Escenario**

| Métrica                       | Escenario Base | 10 Cabinas | 95% Asistencia | ... (otros escenarios) |
| ----------------------------- | -------------- | ---------- | -------------- | ---------------------- |
| Costo Total Campaña ($)       | [Valor]        | [Valor]    | [Valor]        | [Valor]                |
| Costo por Paciente Vacunado ($)| [Valor]        | [Valor]    | [Valor]        | [Valor]                |

### 4.3. Visualizaciones Clave

*(Insertar aquí las figuras más relevantes con una breve descripción, como se pide en `diseño-modelo.md`)*

**Figura 1: Comparación de Tiempo para Vacunar al 100% de la Población.**
*<Insertar gráfico de barras comparativo de escenarios>*

**Figura 2: Histograma de Tiempos de Espera (Escenario Base vs. 10 Cabinas).**
*<Insertar `histograma_tiempos_espera.png` para ambos escenarios>*

**Figura 3: Evolución de la Longitud de la Cola en el Tiempo (Escenario Base).**
*<Insertar `longitud_cola.png` del escenario base>*

---

## 5. Recomendaciones Operativas

El análisis de los resultados demuestra que el escenario base es inviable, ya que [mencionar el problema principal, ej: el tiempo para vacunar a todos supera el año y los tiempos de espera son inaceptables].

El incremento a 10 cabinas (Escenario 10 Cabinas) mejora significativamente el rendimiento. Aunque el costo diario es mayor, la campaña finaliza mucho antes, lo que podría incluso reducir el costo total. El tiempo de espera promedio se reduce a [Valor] minutos, un nivel mucho más aceptable para los ciudadanos.

**Recomendaciones:**
1.  **Implementar un mínimo de [Ej: 10] cabinas de vacunación.** Es la medida con el mayor impacto positivo en el rendimiento del sistema para cumplir los objetivos en un plazo razonable.
2.  **Analizar la viabilidad de extender el horario de atención.** Esta medida, si bien es efectiva, debe compararse con el costo y la logística de añadir más cabinas.
3.  **Fomentar la asistencia.** Los resultados del escenario de 95% de asistencia muestran que una mayor concurrencia, si el sistema está preparado para absorberla, acelera drásticamente el cumplimiento de los objetivos.

---

## 6. Conclusiones

La simulación ha demostrado ser una herramienta estratégica para la toma de decisiones, permitiendo cuantificar el impacto de diferentes políticas operativas antes de su implementación. Se concluye que la configuración inicial de 5 cabinas es insuficiente para los objetivos de la campaña. Una inversión en [Ej: 5 cabinas adicionales] está plenamente justificada, ya que reduce drásticamente los tiempos de espera, mejora la experiencia del ciudadano y, fundamentalmente, acelera la inmunización de la población.

Como **trabajo futuro**, el modelo podría refinarse para incluir:
- La logística de una **segunda dosis**, que requeriría programar una segunda llegada para cada paciente vacunado.
- **Variabilidad en la tasa de llegada** durante el día (horas pico).
- Simulación de **políticas de asignación de turnos más dinámicas**.