# Instructivo de Ejecución de la Simulación de Campaña de Vacunación

Este documento describe los pasos necesarios ejecutar la simulación de la campaña de vacunación.

## 1. Prerrequisitos

- Tener instalado Python 3.8 o una versión superior.
- Tener instalado `pip` (el gestor de paquetes de Python).

## 2. Instalación de Dependencias

Instala todas las bibliotecas necesarias que se encuentran en el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 3. Ejecución de la Simulación

El script principal que orquesta la ejecución de los diferentes escenarios de simulación es `src/main.py`.

### a. Ejecutar Todos los Escenarios

Para correr la simulación se debe cambiar la lista nombres_escenarios y descomentar la línea correspondiente al escenario que se quiera ejecutar.
Luego se ejecuta el siguiente comando desde la raíz del proyecto:

```bash
python3 src/main.py
```

El script se encargará de:

1.  Ejecutar la simulación para cada escenario.
2.  Guardar los datos crudos de la simulación en formato CSV.
3.  Generar análisis estadísticos (como métricas de tiempo de espera, utilización, etc.).
4.  Crear y guardar las visualizaciones (gráficos) correspondientes a cada escenario.

### b. Generar Gráficos Comparativos

Después de que `main.py` haya finalizado y generado los resultados para todos los escenarios individuales, ejecutar el script `generar_comparativas.py` para crear gráficos que comparen las métricas clave entre los diferentes escenarios.

```bash
python3 src/generar_comparativas.py
```

## 4. Revisión de los Resultados

Todos los archivos generados por la simulación y el análisis se guardan en el directorio `data/output/`.

La estructura de la simulación es la siguiente:

```
data/output/
├───[nombre-del-escenario-1]/     # Ej: base, acelerado, etc.
│   ├───analisis_escenario.txt
│   ├───datos_simulacion.csv
│   └───grafico_ocupacion.png
│   └───... (otros gráficos)
│
├───[nombre-del-escenario-2]/
│   └───...
│
└───comparativas/
    ├───comparativa_costo_total.png
    ├───comparativa_tiempo_total.png
    └───... (otros gráficos comparativos)
```

- **Archivos `.csv`**: Contienen los datos en bruto de cada evento de la simulación.
- **Archivos `.txt`**: Presentan un resumen de las métricas de rendimiento clave para cada escenario.
- **Archivos `.png`**: Son los gráficos generados que visualizan los resultados.
