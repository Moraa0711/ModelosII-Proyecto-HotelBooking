# Predicción de cancelaciones de reservas hoteleras

Proyecto del curso **Modelos y Simulación de Sistemas II** – Universidad de Antioquia.

**Integrantes:** Juan Camilo Morales Villada · Juan Sebastián Andraus López · Jose Miguel Fajardo Fernández

Se construye un sistema de aprendizaje supervisado que predice si una reserva de hotel será cancelada, usando el
dataset *Hotel Booking Demand* (119.390 reservas de dos hoteles de Portugal, 2015–2017).

## Estructura

```
├── data/
│   └── hotel_booking.csv          # datos originales (Kaggle)
├── notebooks/
│   ├── 01_descripcion_y_preprocesamiento.ipynb   # Secciones I–III del informe
│   ├── 02_entrenamiento_y_evaluacion.ipynb       # Sección IV (en construcción)
│   └── 03_reduccion_de_dimension.ipynb           # Sección V (en construcción)
├── src/
│   └── preprocesamiento.py        # limpieza y codificación usadas por todos los notebooks
├── figuras/                       # figuras generadas por los notebooks
├── resultados/                    # tablas de resultados generadas por los notebooks
├── reporte/                       # informe final en PDF
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
Ejecutar los notebooks en orden (01, 02, 03), cada uno de principio a fin.

### Opción 2: en Google Colab
Abrir el notebook con el enlace y ejecutar las celdas en orden (la primera celda descarga el repositorio):

- [01 · Descripción y preprocesamiento](https://colab.research.google.com/github/Moraa0711/ModelosII-Proyecto-HotelBooking/blob/main/notebooks/01_descripcion_y_preprocesamiento.ipynb)

## Decisiones principales de preprocesamiento
- Se eliminan las 4 columnas sintéticas de Kaggle y las 3 con fuga de información
  (`reservation_status`, `reservation_status_date`, `assigned_room_type`).
- Faltantes: `children` → 0; `country` → "Desconocido"; `agent` y `company` → indicadores binarios.
- Se eliminan 187 registros inválidos (categoría "Undefined", reservas sin huéspedes y tarifas anómalas).
- Las filas repetidas (reservas de grupo) se conservan y se mantienen juntas en las particiones
  (`StratifiedGroupKFold`) para evitar que una misma reserva quede en entrenamiento y en prueba.
- Codificación One-Hot para categóricas y estandarización para numéricas, ajustadas solo con datos de entrenamiento.
