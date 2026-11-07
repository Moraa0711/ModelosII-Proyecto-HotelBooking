# Predicción de cancelaciones de reservas hoteleras

Proyecto del curso **Modelos y Simulación de Sistemas II** – Universidad de Antioquia.

**Integrantes:** Juan Camilo Morales Villada · Juan Sebastián Andraus López · Jose Miguel Fajardo Fernández

Se construye un sistema de aprendizaje supervisado que predice si una reserva de hotel será cancelada, usando el
dataset *Hotel Booking Demand* (119.390 reservas de dos hoteles de Portugal, 2015–2017).

**Resultado principal:** XGBoost obtuvo un F1 de 0,820 y un AUC-ROC de 0,943 en el conjunto de prueba.
El informe completo está en [`reporte/Informe_final_HotelBooking.pdf`](reporte/Informe_final_HotelBooking.pdf).

## Estructura

```
├── data/
│   └── hotel_booking.csv          # datos originales (Kaggle)
├── notebooks/
│   ├── 01_descripcion_y_preprocesamiento.ipynb   # Secciones I–III del informe
│   ├── 02_entrenamiento_y_evaluacion.ipynb       # Sección IV: 6 modelos y búsqueda de hiperparámetros
│   └── 03_reduccion_de_dimension.ipynb           # Sección V: análisis de variables, PCA y UMAP
├── src/
│   ├── preprocesamiento.py        # limpieza y codificación usadas por todos los notebooks
│   └── evaluacion.py              # partición, validación cruzada, métricas e intervalos de confianza
├── figuras/                       # figuras generadas por los notebooks
├── resultados/                    # tablas de resultados generadas por los notebooks
├── reporte/
│   ├── Informe_final_HotelBooking.pdf   # informe final (formato IEEE)
│   └── Primera_entrega.pdf              # avance entregado (Secciones II y III)
└── requirements.txt
```

## Cómo reproducir los resultados

### Opción 1: en el computador
```bash
git clone https://github.com/Moraa0711/ModelosII-Proyecto-HotelBooking.git
cd ModelosII-Proyecto-HotelBooking
pip install -r requirements.txt
jupyter notebook notebooks/
```
Ejecutar los notebooks en orden (01, 02, 03), cada uno de principio a fin. El notebook 03 usa los resultados que
guarda el 02 en `resultados/`. Tiempos aproximados en CPU: 01 → 1 min, 02 → 30–60 min, 03 → 30–50 min.

### Opción 2: en Google Colab
Abrir el notebook con el enlace y ejecutar las celdas en orden (la primera celda descarga el repositorio):

- [01 · Descripción y preprocesamiento](https://colab.research.google.com/github/Moraa0711/ModelosII-Proyecto-HotelBooking/blob/main/notebooks/01_descripcion_y_preprocesamiento.ipynb)
- [02 · Entrenamiento y evaluación](https://colab.research.google.com/github/Moraa0711/ModelosII-Proyecto-HotelBooking/blob/main/notebooks/02_entrenamiento_y_evaluacion.ipynb)
- [03 · Reducción de dimensión](https://colab.research.google.com/github/Moraa0711/ModelosII-Proyecto-HotelBooking/blob/main/notebooks/03_reduccion_de_dimension.ipynb)

Los notebooks del repositorio ya están ejecutados: se pueden leer con todos sus resultados sin volver a correrlos.

## Decisiones principales de preprocesamiento
- Se eliminan las 4 columnas sintéticas de Kaggle y las 3 con fuga de información
  (`reservation_status`, `reservation_status_date`, `assigned_room_type`).
- Faltantes: `children` → 0; `country` → "Desconocido"; `agent` y `company` → indicadores binarios.
- Se eliminan 187 registros inválidos (categoría "Undefined", reservas sin huéspedes y tarifas anómalas).
- Las filas repetidas (reservas de grupo) se conservan y se mantienen juntas en las particiones
  (`StratifiedGroupKFold`) para evitar que una misma reserva quede en entrenamiento y en prueba.
- Codificación One-Hot para categóricas y estandarización para numéricas, ajustadas solo con datos de entrenamiento.

## Configuración experimental
- 20 % de las reservas como conjunto de prueba (partición estratificada y agrupada).
- Búsqueda de hiperparámetros con validación cruzada de 5 particiones (`StratifiedGroupKFold`); resultados como
  media ± intervalo de confianza del 95 %.
- Modelos: regresión logística, KNN, Random Forest, XGBoost, red neuronal (MLP) y SVM con kernel RBF.
  KNN y SVM se ajustan con una muestra estratificada de ~15.000 reservas por su costo computacional.
- Métrica principal: F1 de la clase cancelada; también AUC-ROC, sensibilidad, precisión y exactitud.
