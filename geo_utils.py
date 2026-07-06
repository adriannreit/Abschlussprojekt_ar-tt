"""Geometrische Hilfsfunktionen zur Berechnung der Geschwindigkeit, Distanz und Steigungswinkel anhand von GPS-Daten"""
import numpy as np

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
