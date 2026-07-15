"""Geometrische Hilfsfunktionen zur Berechnung der Geschwindigkeit, Distanz und Steigungswinkel anhand von GPS-Daten"""
import numpy as np
import pandas as pd
from meteostat import Point, hourly, Station

earth_radius_m = 6371000

def haversine_distance(lat1, lon1, lat2, lon2):
    """Horizontale Distanz zwischen zwei GPS-Punkten in Metern."""
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
 
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    a = np.clip(a, 0, 1)
 
    return 2 * earth_radius_m * np.arcsin(np.sqrt(a))
 
 
def distance_3d(h_distance, d_ele):
    """Kombiniert horizontale Distanz und Höhenänderung zur tatsächlich zurückgelegten Strecke."""
    return np.sqrt(h_distance**2 + d_ele**2)
 
 
def steigungswinkel(d_ele, h_distance):
    """Steigungswinkel in rad. Bei h_distance == 0 wird 0 zurückgegeben um Division durch 0 zu vermeiden."""
    with np.errstate(divide="ignore", invalid="ignore"):
        winkel = np.arctan(np.where(h_distance != 0, d_ele / h_distance, 0.0))
    return np.nan_to_num(winkel, nan=0.0, posinf=0.0, neginf=0.0)

def himmelsrichtung(lat1, lon1, lat2, lon2):
    """Berechnet die Himmelsrichtung (Azimut) zwischen zwei GPS-Punkten in Grad."""
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    dlon = lon2 - lon1

    x = np.sin(dlon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)

    azimuth_rad = np.arctan2(x, y)
    azimuth_deg = (np.degrees(azimuth_rad) + 360) % 360
    directions = ["N", "NNO", "NO", "ONO", "O", "OSO", "SO", "SSO", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = int((azimuth_deg + 11.25) % 360 / 22.5)
    return directions[index], azimuth_deg


def moving_average(values: pd.Series, window_size: int = 5) -> pd.Series:
    """Berechnet den gleitenden Durchschnitt über eine gegebene Fenstergröße."""
    return values.rolling(window=window_size, min_periods=1).mean()

def wetter_daten_auslesen(lat, lon, timestamp):
    """Liest Wetterdaten für einen einzelnen GPS-Punkt und einen einzelnen Zeitpunkt aus."""
    location = Point(float(lat), float(lon))

    if pd.isna(timestamp):
        return {"wspd": None, "wdir": None}

    if hasattr(timestamp, "to_pydatetime"):
        dt_start = timestamp.to_pydatetime()
    else:
        dt_start = pd.to_datetime(timestamp).to_pydatetime()

    if getattr(dt_start, "tzinfo", None) is not None:
        dt_start = dt_start.replace(tzinfo=None)

    dt_end = dt_start + pd.Timedelta(hours=1).to_pytimedelta()

    data = hourly(location, dt_start, dt_end)
    fetched = data.fetch()

    if fetched is None or getattr(fetched, "empty", True):
        return {"wspd": None, "wdir": None}

    row = fetched.iloc[0]
    return {"wspd": row.get("wspd"), "wdir": row.get("wdir")}


def debug_wetterabfrage(lat, lon, timestamp):
    """Debug-Funktion zur Wetterdatenabfrage mit Meteostat."""
    print("\n" + "="*50)
    print("DEBUG: Wetterabfrage gestartet")
    print("="*50)

    # Standort definieren
    location = Point(float(lat), float(lon))
    print(f"Standort: lat={lat}, lon={lon}")

    # Timestamp konvertieren
    if hasattr(timestamp, "to_pydatetime"):
        dt_start = timestamp.to_pydatetime()
    else:
        dt_start = pd.to_datetime(timestamp).to_pydatetime()

    if getattr(dt_start, "tzinfo", None) is not None:
        dt_start = dt_start.replace(tzinfo=None)
    print(f"Startzeitpunkt: {dt_start}")

    # Endzeitpunkt (1 Stunde später)
    dt_end = dt_start + pd.Timedelta(hours=1).to_pytimedelta()
    print(f"Endzeitpunkt: {dt_end}")

    # Wetterdaten abrufen
    fetched = None  # Initialisiere fetched mit None
    try:
        data = hourly(location, dt_start, dt_end)
        fetched = data.fetch()
        print("\nDaten erfolgreich abgerufen.")
    except Exception as e:
        print(f"\nFehler bei der Wetterdatenabfrage: {e}")

    # Prüfe, ob Daten vorhanden sind
    if fetched is not None and not fetched.empty:
        print("\nWetterdaten:")
        print(fetched[["temp", "windspeed", "winddir"]].head())
    else:
        print("\nKeine Wetterdaten für den Zeitraum gefunden oder Abfrage fehlgeschlagen.")

    print("\n" + "="*50)
    print("DEBUG: Wetterabfrage beendet")
    print("="*50 + "\n")
    return fetched

if __name__ == "__main__":
    debug_wetterabfrage(47.583114, 12.170826, pd.to_datetime("2024-08-23T16:21:14.187Z"))
   