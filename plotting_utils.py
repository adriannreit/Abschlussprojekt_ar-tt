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

def plot_leistung_zeit(df, time_col="time", leistung_col="Leistung"):
    """Plottet die Leistung über die Zeit.
 
    Parameters
    ----------
    df : pandas.DataFrame
        Ergebnis von GPSAuswertung.beschleunigung(). Muss `time_col` und `leistung_col` enthalten.
    time_col : str
        Name der Zeitspalte (muss datetime-artig sein, siehe prepare_data()).
    leistung_col : str
        Name der zu plottenden Leistungsspalte (in W).
 
    Returns
    -------
    matplotlib.axes.Axes
    """
    _, ax = plt.subplots(figsize=(10, 4))
    elapsed_minutes = (df[time_col] - df[time_col].iloc[0]).dt.total_seconds() / 60
    ax.plot(elapsed_minutes, df[leistung_col], linewidth=1)
    ax.set_xlabel("Fahrtzeit [min]")
    ax.set_ylabel(leistung_col)
    ax.set_title("Leistung über Zeit [W]")
    ax.grid(True, alpha=0.3)
    ax.figure.autofmt_xdate()

    return ax

def plot_soc_zeit(zeit, soc_verlauf, battery_typ: str):
    """Plottet den State of Charge (SoC) über die Zeit.

    Parameters
    ----------
    zeit : array-like
        Zeitwerte (z.B. Fahrtzeit in Minuten seit Start).
    soc_verlauf : array-like
        SoC-Werte im Bereich [0, 1], z.B. BatterySimulator.soc_verlauf.
    battery_typ : string der im plot zur beschriftung verwendet wird

    Returns
    -------
    matplotlib.axes.Axes
    """
    _, ax = plt.subplots(figsize=(10, 4))

    ax.plot(zeit, np.array(soc_verlauf) * 100, linewidth=1, color="tab:red")
    ax.set_xlabel("Fahrtzeit [min]")
    ax.set_ylabel("SoC [%]")
    ax.set_title(f"{battery_typ} Ladezustand (SoC) über Zeit")
    ax.grid(True, alpha=0.3)

    return ax

def plot_spannung_zeit(zeit, spannung_verlauf, battery_typ: str):
    """Plottet den State of Charge (SoC) über die Zeit.

    Parameters
    ----------
    zeit : array-like
        Zeitwerte (z.B. Fahrtzeit in Minuten seit Start).
    spannung_verlauf : array-like
        Spannung-Werte über die Fahrt
    battery_typ : string der im plot zur beschriftung verwendet wird

    Returns
    -------
    matplotlib.axes.Axes
    """
    _, ax = plt.subplots(figsize=(10, 4))

    ax.plot(zeit, np.array(spannung_verlauf) * 100, linewidth=1, color="tab:red")
    ax.set_xlabel("Fahrtzeit [min]")
    ax.set_ylabel("Spannung [V]")
    ax.set_title(f"{battery_typ} Spannungszustand über Zeit")
    ax.grid(True, alpha=0.3)

    return ax

def plot_parameterstudie_vergleich(ergebnisse, wert_col="benoetigte_Ah", label_col=None):
    """Plottet den Vergleich der verschiedenen Parametern für das Ebike.
    
    Parameters
    ----------
    ergebnisse : list
        Parametersätze
    wert_col : string 
        Name der verwendeten Spalte. Standard ist ``"benoetigte_Ah"``.
    label_col : string
        Name der Spalte, deren Werte als Beschriftung der x-Achse verwendet
        werden. Standart ist ``None``
    """
    if label_col is None:
        label_col = ergebnisse.index.astype(str)
    else:
        label_col = ergebnisse[label_col]

    _, ax = plt.subplots(figsize=(8, 4))
    ax.bar(label_col.astype(str), ergebnisse[wert_col], color="tab:blue")
    ax.set_ylabel(wert_col)
    ax.set_title(f"Parametervergleich: {wert_col}")
    ax.grid(True, axis="y", alpha=0.3)
    return ax