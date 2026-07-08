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
    ax.plot(df[time_col], df[speed_col], linewidth=1)
    ax.set_xlabel("Zeit")
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
 
    ax.plot(df[time_col], df[accel_col], linewidth=1, color="tab:orange")
    ax.axhline(0, color="grey", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Zeit")
    ax.set_ylabel(f"{accel_col} [m/s²]")
    ax.set_title("Beschleunigung über Zeit")
    ax.grid(True, alpha=0.3)
    ax.figure.autofmt_xdate()
 
    return ax
 
 
def plot_steigung_zeit(df, time_col="time", steigung_col="steigung", unit="prozent"):
    """Plottet die Steigung über die Zeit.
 
    Parameters
    ----------
    df : pandas.DataFrame
        Ergebnis von GPSAuswertung.steigung(). Muss `time_col` und `steigung_col` enthalten.
    time_col : str
        Name der Zeitspalte (muss datetime-artig sein, siehe prepare_data()).
    steigung_col : str
        Name der Steigungsspalte. Wird als Winkel in rad erwartet (so wie sie
        von geo_utils.steigungswinkel() geliefert wird).
    unit : {"prozent", "grad", "rad"}
        Einheit, in der die Steigung dargestellt werden soll. 
 
    Returns
    -------
    matplotlib.axes.Axes
    """
    if unit == "prozent":
        werte = np.tan(df[steigung_col]) * 100
        ylabel = "Steigung [%]"
    elif unit == "grad":
        werte = np.degrees(df[steigung_col])
        ylabel = "Steigung [°]"
    elif unit == "rad":
        werte = df[steigung_col]
        ylabel = "Steigung [rad]"
    else:
        raise ValueError(f"Unbekannte unit: {unit!r} (erlaubt: 'prozent', 'grad', 'rad')")
 
    
    _, ax = plt.subplots(figsize=(10, 4))
 
    ax.plot(df[time_col], werte, linewidth=1, color="tab:green")
    ax.axhline(0, color="grey", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Zeit")
    ax.set_ylabel(ylabel)
    ax.set_title("Steigung über Zeit")
    ax.grid(True, alpha=0.3)
    ax.figure.autofmt_xdate()
 
    return ax


