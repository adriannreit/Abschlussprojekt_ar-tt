
def einzelsimulation(csv_pfad, masse_kg=80, cW=0.5625, rad=27, battery_klasse=None, capacity_nom_Ah_cell=10.0):
    """Führt Kraftberechnung + Batteriesimulation für einen Parametersatz aus
    und gibt eine Kennzahlen-Zusammenfassung zurück."""
    from kraft_Leistungsberechnung import Kraftberechnung
    from Battery.battery_simulator import BatterySimulator

    Kb = Kraftberechnung(csv_pfad, masse_kg=masse_kg, cW=cW, rad=rad)
    df = Kb.motorstrom()

    battery = battery_klasse(capacity_nom_Ah_cell=capacity_nom_Ah_cell)
    sim = BatterySimulator(battery)
    sim.simulate(df)

    entlade_strom = df["Motorstrom"].clip(lower=0)
    verbrauchte_Ah = (entlade_strom * df["delta_t"]).sum() / 3600

    return {
        "masse_kg": masse_kg,
        "cW": cW,
        "rad_zoll": rad,
        "akku_typ": battery_klasse.__name__,
        "benoetigte_Ah": round(verbrauchte_Ah, 2),
        "max_motorstrom": round(df["Motorstrom"].max(), 1),
        "abgebrochen": sim.abgebrochen,
        "abbruch_index": sim.abbruch_index,
    }


def parameterstudie(csv_pfad, parametersaetze, battery_klasse):
    """Führt einzelsimulation() für jede Parameterkombination aus
    und gibt eine Vergleichstabelle zurück."""
    import pandas as pd

    ergebnisse = [
        einzelsimulation(csv_pfad, battery_klasse=battery_klasse, **params)
        for params in parametersaetze
    ]
    return pd.DataFrame(ergebnisse)