
## Simulación de Campaña de Vacunación

---

## 1. CONTEXTO DEL PROBLEMA

Un centro regional organiza una campaña de vacunación contra una enfermedad respiratoria (ej. COVID-19).

**Población objetivo:** Todos los habitantes de la ciudad de Concordia.

**Sistema de turnos:** A cada persona se le asigna un día de la semana según la última cifra de su número de documento.

**Recursos disponibles:**

- Número variable de puestos de vacunación (cabinas)
- Horario de atención específico
- Ritmo operacional por puesto

**Factores logísticos:**

- Tasa de asistencia
- Disponibilidad diaria de dosis
- Posibilidad de dosis de refuerzo (dos dosis)
- Limitaciones de horario/recursos

**Objetivo:** Diseñar y analizar un modelo dinámico discreto en tiempo que permita responder:

- ¿Es posible vacunar a toda la población con la configuración actual?
- ¿En cuánto tiempo?
- ¿Cuál es el costo de incorporar más puestos de vacunación?

---

## 2. PARÁMETROS DEL SISTEMA

### 2.1 Parámetros Operativos

1. **Cabinas disponibles:** 5 cabinas para vacunación
2. **Horario de atención:** 08:00 a 18:00 hs (sin límites en cola de espera dentro del horario)
3. **Tasa de llegada:** 30 personas por minuto (promedio)
4. **Tiempo de vacunación:** 3 minutos por persona (promedio)
5. **Tasa de reprogramación:** 20% de los asistentes decide no esperar y solicita reprogramación

### 2.2 Estructura de Costos

|Concepto|Valor estimado|
|---|---|
|Costo fijo por cabina|$55.000 / día|
|Costo por dosis|$2.000 / día|
|Costo por reprogramación|$300 / persona|
|Costo por cabina adicional|$150.000 (por única vez)|
|Costo por espera|$3 / minuto / persona|

### 2.3 Costos a Estimar

- Costo acumulado por día
- Costo por persona vacunada
- Costo por escenario
- Comparación de eficiencia costo/tiempo entre escenarios

---

## 3. TAREAS A REALIZAR

### 3.1 Programación

Desarrollar una simulación que implemente el modelo y permita variar parámetros.

### 3.2 Escenarios a Comparar (mínimo)

- **Escenario base:** Con parámetros por defecto
- **Variación de puestos:** Diferentes números de cabinas de vacunación
- **Variación de asistencia:** Diferentes tasas (ej. 60%, 80%, 95%)
- **Escenario acelerado**

### 3.3 Salidas Requeridas

**Métricas temporales:**

- Tiempo (en días y semanas) hasta vacunar al 70%, 80% y 100% de la población según cada escenario

**Gráficas:**

- Vacunados acumulados vs. tiempo
- Cola acumulada vs. tiempo
- Ocupación diaria de puestos
- Otros gráficos a criterio del alumno

**Tablas/Resúmenes:**

- Tabla con parámetros y tiempo final para cada escenario
- Tabla con análisis de costos por cada escenario

**Análisis:**

- Breve discusión de limitaciones y recomendaciones operativas (p. ej., cuántos puestos son necesarios para terminar en X semanas)

---

## 4. PREGUNTAS A RESPONDER

1. **Tiempo de vacunación:** ¿Cuánto tiempo (en días y semanas) se necesita para vacunar al 70%, 80% y 100% de la población según cada escenario?
    
2. **Recomendaciones operativas:** Breve discusión de limitaciones y recomendaciones (ej., cuántos puestos son necesarios para terminar en X semanas)
    
3. **Estadísticas de cola:**
    
    - Tiempo máximo y mínimo
    - Longitud máxima y mínima
    - Tasa de abandono
    - Tiempo promedio de espera
4. **Estadísticas de servicio:**
    
    - Tiempo promedio de vacunación
    - Tiempo máximo y mínimo
5. **Visualizaciones:**
    
    - Gráficas: vacunados acumulados vs. tiempo, cola acumulada vs. tiempo, ocupación diaria de puestos
6. **Resumen de escenarios:**
    
    - Tabla con parámetros y tiempo final para cada escenario

---

## 5. OBSERVACIONES Y CASOS ESPECIALES

### 5.1 Validación del Modelo

1. Construir e implementar el modelo y validar que con los parámetros base se obtienen resultados coherentes con la aproximación analítica mostrada.

### 5.2 Preguntas de Análisis

2. ¿Con la política de asignación (último dígito → día), es posible vacunar a la población objetivo sin generar colas masivas?
    
3. ¿Cuántos puestos (cabinas) son necesarios para completar la vacunación en 12 semanas?
    
4. **Esquema de 2 dosis:** Modelar el esquema de 2 dosis (intervalo 21 días). ¿Cómo cambia la logística y el tiempo para dar al menos una dosis a toda la población? ¿Y para completar las dos dosis?
    
5. **Políticas alternativas:** Proponer políticas operativas para reducir el tiempo total, por ejemplo:
    
    - Reasignar últimos dígitos a días con menor carga
    - Incorporar turnos virtuales para días restantes
    - Jornadas extraordinarias los fines de semana
    - Comparar mediante simulación

---

## 6. ENTREGABLES

### 6.1 Componentes Obligatorios

1. **Código fuente** (con instrucciones para ejecutar)
    
2. **Informe breve** (máximo 5 páginas) que incluya:
    
    - Supuestos del modelo
    - Resultados obtenidos
    - Figuras y gráficas
    - Recomendaciones
    - **Justificación de la elección de los generadores de números pseudoaleatorios**
    - **Justificación de la distribución de probabilidad utilizada en cada caso**
3. **Formato del informe:** PDF
    
4. **Archivo de datos de salida:** CSV
    

### 6.2 Modalidad de Entrega

- Subir el trabajo final a través del campus, en el espacio asignado
- Realización: individual o grupal (hasta 2 integrantes)
- **Importante:** Por motivos de seguridad, cada alumno debe subir el trabajo de manera individual, aunque el desarrollo sea grupal
- **No se aceptarán trabajos fuera de tiempo**
- Se deben respetar todos los puntos especificados en entregables

---

## 7. CRITERIOS DE EVALUACIÓN

|Criterio|Peso|
|---|---|
|Correcta definición del modelo y justificación de supuestos|25%|
|Implementación correcta y reproducible del código|25%|
|Calidad de los experimentos y análisis de sensibilidad|25%|
|Presentación (gráficas claras, tablas) y conclusiones operativas razonadas|15%|
|Documentación / comentarios en código y entrega de informes|10%|
|**TOTAL**|**100%**|

---

## RESUMEN DE PUNTOS CLAVE

✓ Simular campaña de vacunación con modelo dinámico discreto  
✓ Analizar múltiples escenarios (base, variaciones de cabinas, tasas de asistencia)  
✓ Calcular costos asociados a cada escenario  
✓ Generar gráficas y estadísticas detalladas  
✓ Responder preguntas específicas sobre tiempos y recursos necesarios  
✓ Considerar esquema de 2 dosis y proponer mejoras operativas  
✓ Entregar código, informe (máx. 5 páginas) y datos en CSV  
✓ Justificar elección de generadores aleatorios y distribuciones de probabilidad