class BatterySimulator:
    """Simuliert den SoC- und Spannungsverlauf eines Battery-Objekts anhand
    eines Motorstrom-Profils"""

    def __init__(self, battery) -> None:
        self.battery = battery
        self.soc_verlauf = []
        self.spannung_verlauf = []
        self.abgebrochen = False
        self.abbruch_index = None

    def simulate(self, df, strom_col="Motorstrom", dt_col="delta_t", time_col="time"):
        self.soc_verlauf = []
        self.spannung_verlauf = []
        self.zeit_verlauf = []
        self.abgebrochen = False
        self.abbruch_index = None

        start_zeit = df[time_col].iloc[0]

        for i, (strom, dt, zeit) in enumerate(zip(df[strom_col], df[dt_col], df[time_col])):
            
            self.soc_verlauf.append(self.battery.soc)
            self.spannung_verlauf.append(self.battery.voltage(current=strom))
            self.zeit_verlauf.append((zeit - start_zeit).total_seconds() / 60)

            if self.battery.is_empty() and strom > 0:
                print(f"Warnung: Akku bei Index {i} leer - Simulation abgebrochen.")
                self.abgebrochen = True
                self.abbruch_index = i
                break

            self.battery.apply_current(current=strom, duration=dt)

            if self.battery.is_full() and strom < 0:
                print(f"Hinweis: Akku bei Index {i} voll - Bremswiderstand nötig.")

        return self.soc_verlauf, self.spannung_verlauf