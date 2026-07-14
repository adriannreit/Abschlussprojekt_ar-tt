from gps_auswertung import GPSAuswertung
import plotting_utils 
import matplotlib.pyplot as plt
from kraft_Leistungsberechnung import Kraftberechnung
from Battery.battery_simulator import BatterySimulator
from Battery.battery_LiPo import Battery_LiPo
from Battery.battery_NMC import Battery_NMC

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
input("Enter drücken zum Schließen der Plots und Öffnen der Akku-Simulation...")
plt.close("all")


def battery_plt(battery, battery_typ: str):
    df = Kb.motorstrom()
    sim = BatterySimulator(battery)
    sim.simulate(df)

    plotting_utils.plot_soc_zeit(sim.zeit_verlauf, sim.soc_verlauf, battery_typ)
    plotting_utils.plot_spannung_zeit(sim.zeit_verlauf, sim.spannung_verlauf, battery_typ)


battery_plt(Battery_LiPo(capacity_nom_Ah_cell=150.0), "LiPo"), battery_plt(Battery_NMC(capacity_nom_Ah_cell=150.0), "NMC")

plt.show(block=False)
input("Enter drücken zum Schließen der Plots...")
plt.close("all")