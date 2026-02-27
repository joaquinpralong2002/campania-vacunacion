# Simulación de Campaña de Vacunación con Eventos Discretos (SimPy)

Proyecto académico-profesional orientado al análisis operativo de una campaña de vacunación, usando **simulación de eventos discretos** para evaluar tiempos, colas, costos y capacidad bajo distintos escenarios.

## Resumen ejecutivo

Este repositorio modela el flujo completo de pacientes en un centro de vacunación con:

- llegadas estocásticas (proceso de Poisson),
- atención con recursos limitados (cabinas SimPy),
- reprogramación por congestión,
- y evaluación comparativa de escenarios operativos.

El objetivo es responder preguntas de gestión: **¿cuánto tarda la campaña?, ¿qué tan grande es la cola?, ¿cuánto cuesta?, ¿qué configuración conviene?**

## Problema abordado

Se simula una campaña para una población de Concordia con asignación por último dígito de DNI y operación diaria en cabinas de vacunación.

Preguntas clave del análisis:

- Tiempo para alcanzar 70%, 80% y 100% de cobertura.
- Impacto de aumentar cabinas o cambiar la asistencia.
- Efecto sobre tiempos de espera, abandono/reprogramación y costo total.

## Qué implementa el proyecto

### 1) Motor de simulación (SimPy)

- Modela llegadas por día según dígitos de DNI asignados.
- Genera tiempos entre llegadas y de servicio con distribuciones exponenciales.
- Gestiona cola de espera y capacidad de cabinas.
- Registra eventos por paciente: `Vacunado` o `Reprogramacion`.

### 2) Cálculo de métricas de desempeño

- Totales: vacunados, reprogramados, pacientes procesados.
- Calidad de servicio: espera promedio/máxima/mínima y tiempo en sistema.
- Congestión: longitud de cola promedio y máxima.
- Rendimiento: utilización de cabinas.
- Economía: costo total, costo por vacunado y eficiencia costo/tiempo.
- Cobertura: estimación de hitos 70/80/100%.

### 3) Visualización y comparación de escenarios

- Curva de vacunados acumulados vs. tiempo.
- Evolución de cola vs. tiempo.
- Histograma de tiempos de espera.
- Gráficos comparativos entre escenarios (costos, vacunados, espera, etc.).

### 4) Automatización de ejecución

- Ejecución multiproceso de escenarios para acelerar corridas.
- Persistencia de resultados en `CSV` + métricas en `JSON` + gráficos `PNG`.

## Escenarios contemplados en configuración

- `base`
- `10_cabinas`
- `20_cabinas`
- `80_asistencia`
- `95_asistencia`
- `acelerado`
- `dos_dosis`
- `horario_extendido`

> La lista de escenarios efectivamente ejecutados se define en `src/main.py`.

## Estructura del repositorio

```text
campania-vacunacion/
├── src/
│   ├── config.py               # Parámetros y escenarios
│   ├── simulation.py           # Lógica de eventos discretos
│   ├── analysis.py             # Métricas operativas y de costos
│   ├── visualization.py        # Gráficos por escenario y comparativas
│   ├── generar_comparativas.py # Agregación multi-escenario
│   └── main.py                 # Pipeline principal
├── tests/                      # Pruebas unitarias
├── notebooks/                  # Análisis exploratorio
├── data/output/                # Artefactos generados por simulación
├── diseño-modelo.md            # Diseño conceptual del modelo
└── Trabajo Final Integrador.md # Consigna y objetivos del trabajo
```

## Stack tecnológico

- **Python**
- **SimPy** (simulación de eventos discretos)
- **Pandas / NumPy** (análisis de datos)
- **Matplotlib / Seaborn** (visualización)
- **Pytest** (testing)

## Cómo ejecutar

### 1) Crear y activar entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3) Ejecutar simulaciones

```bash
python -m src.main
```

Esto genera por escenario:

- `data/output/<escenario>/resultados_<escenario>.csv`
- `data/output/<escenario>/metricas.json`
- gráficos `.png`

### 4) Generar gráficos comparativos entre escenarios

```bash
python -m src.generar_comparativas
```

Salida esperada:

- `data/output/comparativas/*.png`

### 5) Ejecutar tests

```bash
pytest -q
```

## Calidad y validación

El proyecto incluye pruebas unitarias sobre:

- configuración de escenarios,
- ejecución mínima de simulación,
- cálculo de métricas,
- generación de visualizaciones.

Esto asegura reproducibilidad básica y estabilidad del pipeline analítico.
