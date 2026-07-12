import matplotlib.pyplot as plt
import numpy as np

def plot_geschwindigkeit_zeit(df, time_col="time", speed_col="geschw._km/h"):
    """Plottet die Geschwindigkeit über die Zeit.
 
    Parameters
    ----------
    df : pandas.DataFrame
        Ergebnis von GPSAuswertung.geschwindigkeit(). Muss `time_col` und `speed_col`
        enthalten.
    time_col : str
        Name der Zeitspalte (muss datetime-artig sein, siehe prepare_data()).
    speed_col : str
        Name der zu plottenden Geschwindigkeitsspalte, z.B. "geschw._km/h" oder "geschw._m/s".
 
    Returns
    -------
    matplotlib.axes.Axes
    """
    _, ax = plt.subplots(figsize=(10, 4))
    elapsed_minutes = (df[time_col] - df[time_col].iloc[0]).dt.total_seconds() / 60
    ax.plot(elapsed_minutes, df[speed_col], linewidth=1)
    ax.set_xlabel("Fahrtzeit [min]")
    ax.set_ylabel(speed_col)
    ax.set_title("Geschwindigkeit über Zeit")
    ax.grid(True, alpha=0.3)
    ax.figure.autofmt_xdate()

    return ax

def plot_beschleunigung_zeit(df, time_col="time", accel_col="beschleunigung"):
    """Plottet die Beschleunigung über die Zeit.
 
    Parameters
    ----------
    df : pandas.DataFrame
        Ergebnis von GPSAuswertung.beschleunigung(). Muss `time_col` und `accel_col` enthalten.
    time_col : str
        Name der Zeitspalte (muss datetime-artig sein, siehe prepare_data()).
    accel_col : str
        Name der zu plottenden Beschleunigungsspalte (in m/s^2).
 
    Returns
    -------
    matplotlib.axes.Axes
    """
    _, ax = plt.subplots(figsize=(10, 4))
 
    elapsed_minutes = (df[time_col] - df[time_col].iloc[0]).dt.total_seconds() / 60
    ax.plot(elapsed_minutes, df[accel_col], linewidth=1)
    ax.set_xlabel("Fahrtzeit [min]")
    ax.set_ylabel(f"{accel_col} [m/s²]")
    ax.set_title("Beschleunigung über Zeit")
    ax.grid(True, alpha=0.3)
    ax.figure.autofmt_xdate()
 
    return ax
 
 
def plot_hoehenprofil_distanz(df, distance_col="distance", ele_col="ele"):
    """Plottet das Höhenprofil über die zurückgelegte Distanz.

    Parameters
    ----------
    df : pandas.DataFrame
        Ergebnis von GPSAuswertung.geschwindigkeit() (oder .beschleunigung()/.steigung()).
        Muss `distance_col` und `ele_col` enthalten.
    distance_col : str
        Name der Segment-Distanzspalte (wird intern kumuliert für "Distanz seit Start").
    ele_col : str
        Name der Höhenspalte in Metern (Standard aus prepare_data(): "ele").

    Returns
    -------
    matplotlib.axes.Axes
    """
    kumulierte_distanz = df[distance_col].cumsum()

    _, ax = plt.subplots(figsize=(10, 4))

    ax.plot(kumulierte_distanz, df[ele_col], linewidth=1, color="tab:brown")
    ax.fill_between(kumulierte_distanz, df[ele_col], df[ele_col].min(), alpha=0.15, color="tab:brown")
    ax.set_xlabel("Distanz [m]")
    ax.set_ylabel("Höhe [m]")
    ax.set_title("Höhenprofil")
    ax.grid(True, alpha=0.3)

    return ax