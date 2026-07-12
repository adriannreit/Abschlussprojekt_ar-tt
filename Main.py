from gps_auswertung import GPSAuswertung
import plotting_utils 
import matplotlib.pyplot as plt
from kraft_Leistungsberechnung import Kraftberechnung

gps = GPSAuswertung("final_project_input_data.csv")
Kb = Kraftberechnung("final_project_input_data.csv")

def geschwindigkeit_plt():
    df = gps.geschwindigkeit()
    plotting_utils.plot_geschwindigkeit_zeit(df)

def beschleunigung_plt():
    df = gps.beschleunigung()
    plotting_utils.plot_beschleunigung_zeit(df)

def steigung_plt():
    df = gps.steigung()
    plotting_utils.plot_hoehenprofil_distanz(df)

def leistung_plt():
    df = Kb.leistung()
    plotting_utils.plot_leistung_zeit(df)


geschwindigkeit_plt(), beschleunigung_plt(), steigung_plt(), leistung_plt()
plt.show(block=False)
input("Enter drücken zum Schließen aller Plots...")
plt.close("all")
