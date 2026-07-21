import numpy as np
from gps_auswertung import GPSAuswertung
from luftdruckberechnung import rho

class Kraftberechnung(GPSAuswertung):
    def __init__(self, gps_data , masse_kg: float = 80, cW: float= 0.5625, rad: float = 27)-> None:
        super().__init__(gps_data)
        self.masse_kg = masse_kg
        self.cW = cW
        self.rad = rad * 0.0254/2
        self.df = None

    def luftwiderstandskraft(self):
        if self.df is None or "geschw._m/s" not in self.df.columns:
            self.geschwindigkeit()

        if self.df is None or "geschw._m/s" not in self.df.columns:
            raise ValueError("Daten müssen mit geschwindigkeit() vorbereitet werden, bevor luftwiderstandskraft() aufgerufen wird.")
        
        p = rho(self.df[self.ele_col], self.df[self.temp_col])

        self.df["Luftwiderstandskraft"] = 0.5 * p * self.cW * (self.df["geschw._m/s"] ** 2)
        return self.df
    
    def rollwiderstandskraft(self, rollwiederstandsbeiwert: float = 0.004):
        if self.df is None or "steigung" not in self.df.columns:
            self.steigung()

        if self.df is None or "steigung" not in self.df.columns:
            raise ValueError("Daten müssen mit steigung() vorbereitet werden, bevor rollwiderstandskraft() aufgerufen wird.")

        self.df["rollwiderstandskraft"] = rollwiederstandsbeiwert * self.masse_kg * 9.81 * np.cos(self.df["steigung"])
        return self.df
    
    def kraft(self):
        if self.df is None or "beschleunigung" not in self.df.columns or "steigung" not in self.df.columns or "Luftwiderstandskraft" not in self.df.columns or "rollwiderstandskraft" not in self.df.columns:
            self.beschleunigung()
            self.steigung()
            self.luftwiderstandskraft()
            self.rollwiderstandskraft()

        if self.df is None or "beschleunigung" not in self.df.columns:
            raise ValueError("Daten müssen mit beschleunigung(), steigung(), rollwiderstandskraft() und luftwiderstandskraft() vorbereitet werden, bevor kraft() aufgerufen wird.")

        self.df["Kraft"] = self.masse_kg * self.df["beschleunigung"] + self.masse_kg * 9.81 * np.sin(self.df["steigung"]) + self.df["Luftwiderstandskraft"] + self.df["rollwiderstandskraft"] 
        return self.df
    
    def leistung(self):
        if self.df is None or "Kraft" not in self.df.columns or "geschw._m/s" not in self.df.columns:
            self.kraft() 

        if self.df is None or "Kraft" not in self.df.columns or "geschw._m/s" not in self.df.columns:
            raise ValueError("Daten müssen mit kraft() vorbereitet werden, bevor leistung() aufgerufen wird.")

        self.df["Leistung"] = self.df["Kraft"] * self.df["geschw._m/s"]
        return self.df
    
    def drehmoment(self,):
        if self.df is None or "Kraft" not in self.df.columns:
            self.kraft()

        if self.df is None or "Kraft" not in self.df.columns:
            raise ValueError("Daten müssen mit kraft() vorbereitet werden, bevor drehmoment() aufgerufen wird.")
        self.df["Drehmoment"] = self.df["Kraft"] * self.rad
        return self.df
    
    def motorstrom(self, Motorstromkonstante = 1.5):
        if self.df is None or "Drehmoment" not in self.df.columns:
            self.drehmoment()

        if self.df is None or "Drehmoment" not in self.df.columns:
            raise ValueError("Daten müssen mit drehmoment() vorbereitet werden, bevor motorstrom() aufgerufen wird.")
        self.df["Motorstrom"] = self.df["Drehmoment"] / Motorstromkonstante
        return self.df

if __name__ == "__main__":
    Kb =  Kraftberechnung("final_project_input_data.csv", masse_kg = 100)
    df = Kb.kraft()
    df = Kb.leistung()
    df = Kb.drehmoment()
    df = Kb.motorstrom()
    print(df[["Kraft","geschw._m/s", "Luftwiderstandskraft", "Motorstrom"]].head(10))
