"""
Funciones de partición, validación y resumen de resultados.

Las usan los notebooks 02 (Sección IV) y 03 (Sección V) para que ambos trabajen
exactamente con la misma partición y las mismas métricas.
"""
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import (accuracy_score, f1_score, precision_score, recall_score,
                             roc_auc_score)
from sklearn.model_selection import StratifiedGroupKFold

SEMILLA = 42
K_FOLDS = 5

# Métricas evaluadas (la búsqueda de hiperparámetros escoge el mejor modelo por F1)
METRICAS = {
    "f1": "f1",
    "roc_auc": "roc_auc",
    "recall": "recall",
    "precision": "precision",
    "accuracy": "accuracy",
}
METRICA_PRINCIPAL = "f1"
NOMBRES_METRICAS = {"f1": "F1", "roc_auc": "AUC-ROC", "recall": "Sensibilidad",
                    "precision": "Precisión", "accuracy": "Exactitud"}


def validacion_cruzada(semilla=SEMILLA):
    """Validación cruzada estratificada y agrupada (las filas idénticas no se separan)."""
    return StratifiedGroupKFold(n_splits=K_FOLDS, shuffle=True, random_state=semilla)


def particion_prueba(X, y, grupos, semilla=SEMILLA):
    """Separa ~20 % de los datos para prueba, estratificado y respetando los grupos."""
    entrenamiento, prueba = next(validacion_cruzada(semilla).split(X, y, grupos))
    return entrenamiento, prueba


def muestra_agrupada(y, grupos, n, semilla=SEMILLA):
    """
    Toma una muestra de aproximadamente n filas, estratificada y sin partir grupos.
    Se usa para KNN y SVM, cuyo costo computacional crece mucho con el número de muestras.
    """
    pliegues = max(2, int(round(len(y) / n)))
    sgk = StratifiedGroupKFold(n_splits=pliegues, shuffle=True, random_state=semilla)
    _, muestra = next(sgk.split(np.zeros(len(y)), y, grupos))
    return np.sort(muestra)


def intervalo_confianza(valores, nivel=0.95):
    """Media y semiancho del intervalo de confianza (t de Student) de los k pliegues."""
    valores = np.asarray(valores, dtype=float)
    k = len(valores)
    media = valores.mean()
    semiancho = stats.t.ppf((1 + nivel) / 2, k - 1) * valores.std(ddof=1) / np.sqrt(k)
    return media, semiancho


def tabla_busqueda(busqueda, parametros):
    """
    Convierte cv_results_ de GridSearchCV en una tabla con media e IC95 % por combinación,
    para entrenamiento y validación.
    """
    cv = busqueda.cv_results_
    filas = []
    for i in range(len(cv["params"])):
        fila = {p: cv["params"][i][p] for p in parametros}
        for m in METRICAS:
            for parte, prefijo in [("val", "test"), ("ent", "train")]:
                vals = [cv[f"split{j}_{prefijo}_{m}"][i] for j in range(K_FOLDS)
                        if f"split{j}_{prefijo}_{m}" in cv]
                if vals:
                    media, ic = intervalo_confianza(vals)
                    fila[f"{m}_{parte}"] = media
                    fila[f"{m}_{parte}_ic"] = ic
        fila["tiempo_ajuste_s"] = cv["mean_fit_time"][i]
        fila["rango"] = cv[f"rank_test_{METRICA_PRINCIPAL}"][i]
        filas.append(fila)
    tabla = pd.DataFrame(filas)
    for p in parametros:  # conservar los valores tal cual (None, tuplas), sin convertirlos a float
        tabla[p] = pd.Series([f[p] for f in filas], dtype=object)
    return tabla.sort_values("rango", kind="stable").reset_index(drop=True)


def puntajes(modelo, X):
    """Puntaje continuo para el AUC: probabilidad si existe, si no la función de decisión."""
    if hasattr(modelo, "predict_proba"):
        return modelo.predict_proba(X)[:, 1]
    return modelo.decision_function(X)


def metricas_prueba(modelo, X, y):
    pred = modelo.predict(X)
    return {
        "f1": f1_score(y, pred),
        "roc_auc": roc_auc_score(y, puntajes(modelo, X)),
        "recall": recall_score(y, pred),
        "precision": precision_score(y, pred),
        "accuracy": accuracy_score(y, pred),
    }


def fmt(media, ic=None, dec=3):
    """Formato '0,812 ± 0,004' (coma decimal, como en el informe)."""
    texto = f"{media:.{dec}f}"
    if ic is not None:
        texto += f" ± {ic:.{dec}f}"
    return texto.replace(".", ",")
