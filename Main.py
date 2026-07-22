from gps_auswertung import GPSAuswertung
import plotting_utils 
import matplotlib.pyplot as plt
from kraft_Leistungsberechnung import Kraftberechnung
from Battery.battery_simulator import BatterySimulator
from Battery.battery_LiPo import Battery_LiPo
from Battery.battery_NMC import Battery_NMC
from parameterstudie import parameterstudie

gps = GPSAuswertung("final_project_input_data.csv")
Kb1 = Kraftberechnung("final_project_input_data.csv")

parametersaetze = [
    {"masse_kg": 80,  "cW": 0.5625, "rad": 27},
    {"masse_kg": 100, "cW": 0.5625, "rad": 27},
    {"masse_kg": 80,  "cW": 0.40,   "rad": 27},
    {"masse_kg": 80,  "cW": 0.5625, "rad": 29},
]


def geschwindigkeit_plt():
    df = gps.geschwindigkeit()
    plotting_utils.plot_geschwindigkeit_zeit(df)

def beschleunigung_plt():
    df = gps.beschleunigung()
    plotting_utils.plot_beschleunigung_zeit(df)

def steigung_plt():
    df = gps.steigung()
    plotting_utils.plot_hoehenprofil_distanz(df)

def leistung_plt(Kraftberechnung):
    df = Kraftberechnung.leistung()
    plotting_utils.plot_leistung_zeit(df)



geschwindigkeit_plt(), beschleunigung_plt(), steigung_plt(), leistung_plt(Kb1), #leistung_plt(Kb2)
plt.show(block=False)
input("Enter drücken zum Schließen der Plots und Öffnen der Akku-Simulation...")
plt.close("all")


#--------------------Battery Simulation--------------------------------

def battery_plt(battery, battery_typ: str, Kraftberechnung):
    df = Kraftberechnung.motorstrom()
    sim = BatterySimulator(battery)
    sim.simulate(df)

    plotting_utils.plot_soc_zeit(sim.zeit_verlauf, sim.soc_verlauf, battery_typ)
    plotting_utils.plot_spannung_zeit(sim.zeit_verlauf, sim.spannung_verlauf, battery_typ)



battery_plt(Battery_LiPo(capacity_nom_Ah_cell= 32.0), "LiPo", Kb1), battery_plt(Battery_NMC(capacity_nom_Ah_cell=32.0), "NMC", Kb1)

plt.show(block=False)
input("Enter drücken zum Schließen der Plots und öffnen der Parameterstudie...")
plt.close("all")


#------------------------Parameterstudie-----------------------

ergebnisse_LiPo = parameterstudie("final_project_input_data.csv", parametersaetze, Battery_LiPo)
ergebnisse_NMC = parameterstudie("final_project_input_data.csv", parametersaetze, Battery_NMC)
print(ergebnisse_LiPo)
print(ergebnisse_NMC)

plotting_utils.plot_parameterstudie_vergleich(ergebnisse_LiPo, "LiPo")
plotting_utils.plot_parameterstudie_vergleich(ergebnisse_NMC, "NMC")

plt.show(block=False)
input("Enter drücken zum Schließen der Plots...")
plt.close("all")