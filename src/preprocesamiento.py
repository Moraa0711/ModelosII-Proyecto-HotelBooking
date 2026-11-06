"""
Funciones de carga, limpieza y codificación del dataset Hotel Booking.

Todas las decisiones implementadas aquí están justificadas en la Sección II del informe
y en el notebook 01_descripcion_y_preprocesamiento.ipynb.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ---------------------------------------------------------------------------
# Definición de columnas
# ---------------------------------------------------------------------------
OBJETIVO = "is_canceled"

# Columnas agregadas artificialmente en la versión de Kaggle (no son datos reales)
COLUMNAS_SINTETICAS = ["name", "email", "phone-number", "credit_card"]

# Columnas con fuga de información: contienen la respuesta o se conocen después de reservar
COLUMNAS_FUGA = ["reservation_status", "reservation_status_date", "assigned_room_type"]

# Categóricas nominales que se codifican con One-Hot
NOMINALES = ["hotel", "meal", "market_segment", "distribution_channel",
             "reserved_room_type", "deposit_type", "customer_type"]

# country se codifica aparte: los países poco frecuentes se agrupan en una sola categoría
PAIS = ["country"]
MIN_RESERVAS_PAIS = 100

NUMERICAS = ["lead_time", "stays_in_weekend_nights", "stays_in_week_nights", "adults",
             "children", "babies", "previous_cancellations", "previous_bookings_not_canceled",
             "booking_changes", "days_in_waiting_list", "adr", "required_car_parking_spaces",
             "total_of_special_requests"]

TEMPORALES = ["arrival_date_year", "arrival_date_month", "arrival_date_week_number",
              "arrival_date_day_of_month"]

BINARIAS = ["is_repeated_guest", "tiene_agente", "tiene_compania"]

MESES = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
         "July": 7, "August": 8, "September": 9, "October": 10, "November": 11,
         "December": 12}

ADR_MAXIMO = 1000  # solo existe un valor por encima (5.400), muy alejado del resto


# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------
def cargar_datos(ruta):
    """Lee el CSV original de Kaggle (usar siempre el CSV, no el Excel)."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta}. Descargue hotel_booking.csv de "
            "https://www.kaggle.com/datasets/mojtaba142/hotel-booking y guárdelo en la carpeta data/.")
    return pd.read_csv(ruta)


# ---------------------------------------------------------------------------
# Limpieza
# ---------------------------------------------------------------------------
def limpiar_datos(df):
    """
    Aplica las reglas de limpieza definidas en la Sección II del informe.

    Devuelve el DataFrame limpio y una bitácora con las filas que quedan después de cada paso.
    Ninguna regla aprende nada de los datos (son reglas fijas, fila por fila), por lo que
    pueden aplicarse antes de dividir en entrenamiento y prueba sin generar fuga.
    """
    d = df.copy()
    bitacora = [("Base original", len(d), d.shape[1])]

    def registrar(paso):
        bitacora.append((paso, len(d), d.shape[1]))

    # 1. Quitar columnas sintéticas y columnas con fuga de información
    d = d.drop(columns=COLUMNAS_SINTETICAS + COLUMNAS_FUGA)
    registrar("Quitar 4 columnas sintéticas y 3 con fuga")

    # 2. Imputación de faltantes
    d["children"] = d["children"].fillna(0).astype(int)          # 4 faltantes -> moda (0)
    d["country"] = d["country"].fillna("Desconocido")             # 488 faltantes
    d["tiene_agente"] = d["agent"].notna().astype(int)            # faltante = sin agente
    d["tiene_compania"] = d["company"].notna().astype(int)        # faltante = sin compañía
    d = d.drop(columns=["agent", "company"])
    registrar("Imputar children y country; agent/company -> indicadores")

    # 3. Categoría 'Undefined'
    d["meal"] = d["meal"].replace({"Undefined": "SC"})            # Undefined y SC = sin plan
    d = d[(d["market_segment"] != "Undefined") & (d["distribution_channel"] != "Undefined")]
    registrar("Quitar 'Undefined' en market_segment y distribution_channel")

    # 4. Registros inconsistentes
    sin_huespedes = (d["adults"] + d["children"] + d["babies"]) == 0
    d = d[~sin_huespedes]
    registrar("Quitar reservas sin huéspedes")
    d = d[(d["adr"] >= 0) & (d["adr"] <= ADR_MAXIMO)]
    registrar("Quitar adr negativo y adr atípico (5.400)")

    # 5. Mes de llegada: texto -> número
    d["arrival_date_month"] = d["arrival_date_month"].map(MESES).astype(int)

    d = d.reset_index(drop=True)
    bitacora = pd.DataFrame(bitacora, columns=["Paso", "Filas", "Columnas"])
    bitacora["Filas eliminadas"] = (-bitacora["Filas"].diff()).fillna(0).astype(int)
    return d, bitacora


# ---------------------------------------------------------------------------
# Variables de entrada, objetivo y grupos
# ---------------------------------------------------------------------------
def columnas_entrada(incluir_pais=True):
    return NOMINALES + (PAIS if incluir_pais else []) + NUMERICAS + TEMPORALES + BINARIAS


def separar_xy(d, incluir_pais=True):
    X = d[columnas_entrada(incluir_pais)].copy()
    y = d[OBJETIVO].astype(int).to_numpy()
    return X, y


def grupos_repetidos(d):
    """
    Asigna el mismo número a las filas idénticas en todas las variables de entrada.

    Se usa con StratifiedGroupKFold para que las reservas repetidas (por ejemplo, las de un
    mismo grupo) queden siempre en el mismo lado de cada partición y no aparezcan a la vez
    en entrenamiento y en prueba.
    """
    cols = columnas_entrada(incluir_pais=True)
    return d.groupby(cols, sort=False, dropna=False).ngroup().to_numpy()


# ---------------------------------------------------------------------------
# Codificación
# ---------------------------------------------------------------------------
def _one_hot(**kwargs):
    # sparse_output existe desde scikit-learn 1.2
    return OneHotEncoder(sparse_output=False, **kwargs)


def construir_preprocesador(incluir_pais=True, escalar=True):
    """
    ColumnTransformer que codifica las variables. Se ajusta SOLO con datos de entrenamiento
    (dentro de un Pipeline), así que la agrupación de países poco frecuentes y el escalado
    tampoco generan fuga.
    """
    numericas = NUMERICAS + TEMPORALES
    transformadores = [
        ("nominales", _one_hot(handle_unknown="ignore"), NOMINALES),
        ("numericas", StandardScaler() if escalar else "passthrough", numericas),
        ("binarias", "passthrough", BINARIAS),
    ]
    if incluir_pais:
        transformadores.insert(1, ("pais", _one_hot(handle_unknown="infrequent_if_exist",
                                                    min_frequency=MIN_RESERVAS_PAIS), PAIS))
    return ColumnTransformer(transformadores, verbose_feature_names_out=False)
