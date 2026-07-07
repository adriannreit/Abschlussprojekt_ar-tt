import numpy as np
from gps_auswertung import GPSAuswertung
from luftdruckberechnung import rho

class Kraftberechnung(GPSAuswertung):
    def __init__(self, gps_data):
        super().__init__(gps_data)
        self.df = None

    def luftwiderstandskraft(self, cW = 0.8):
        if self.df is None or "geschw._m/s" not in self.df.columns:
            self.geschwindigkeit()

        if self.df is None or "geschw._m/s" not in self.df.columns:
            raise ValueError("Daten müssen mit geschwindigkeit() vorbereitet werden, bevor luftwiderstandskraft() aufgerufen wird.")
        
        p = rho(self.df[self.ele_col], self.df[self.temp_col])

        self.df["Luftwiderstandskraft"] = 0.5 * p * cW * (self.df["geschw._m/s"] ** 2)
        return self.df
    
    def kraft(self, masse_kg):
        if self.df is None or "beschleunigung" not in self.df.columns or "steigung" not in self.df.columns or "Luftwiderstandskraft" not in self.df.columns:
            self.beschleunigung()
            self.steigung()
            self.luftwiderstandskraft()

        if self.df is None or "beschleunigung" not in self.df.columns:
            raise ValueError("Daten müssen mit beschleunigung(), steigung() und luftwiderstandskraft() vorbereitet werden, bevor kraft() aufgerufen wird.")

        self.df["Kraft"] = masse_kg * self.df["beschleunigung"] + masse_kg * 9.81 * np.sin(self.df["steigung"]) + self.df["Luftwiderstandskraft"]
        return self.df
    
    def leistung(self, masse_kg):
        if self.df is None or "Kraft" not in self.df.columns or "geschw._m/s" not in self.df.columns:
            self.kraft(masse_kg)  # Beispielmasse, kann angepasst werden

        if self.df is None or "Kraft" not in self.df.columns or "geschw._m/s" not in self.df.columns:
            raise ValueError("Daten müssen mit kraft() vorbereitet werden, bevor leistung() aufgerufen wird.")

        self.df["Leistung"] = self.df["Kraft"] * self.df["geschw._m/s"]
        return self.df

if __name__ == "__main__":
    Kb =  Kraftberechnung("final_project_input_data.csv")
    df = Kb.kraft(masse_kg= 100)
    df = Kb.leistung(masse_kg = 100)
    print(df[["Kraft","geschw._m/s", "Luftwiderstandskraft"]].head(10))
