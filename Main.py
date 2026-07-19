from gps_auswertung import GPSAuswertung
import plotting_utils 
import matplotlib.pyplot as plt
from kraft_Leistungsberechnung import Kraftberechnung
from Battery.battery_simulator import BatterySimulator
from Battery.battery_LiPo import Battery_LiPo
from Battery.battery_NMC import Battery_NMC

gps = GPSAuswertung("final_project_input_data.csv")
Kb1 = Kraftberechnung("final_project_input_data.csv")
Kb2 = Kraftberechnung("final_project_input_data.csv", 100, 0.5625 , 29)

def geschwindigkeit_plt():
    df = gps.geschwindigkeit()
    plotting_utils.plot_geschwindigkeit_zeit(df)

def beschleunigung_plt():
    df = gps.beschleunigung()
    plotting_utils.plot_beschleunigung_zeit(df)

def steigung_plt():
    df = gps.steigung()
    plotting_utils.plot_hoehenprofil_distanz(df)

def leistung1_plt():
    df = Kb1.leistung()
    plotting_utils.plot_leistung_zeit(df)

def leistung2_plt():
    df = Kb2.leistung()
    plotting_utils.plot_leistung_zeit(df)



geschwindigkeit_plt(), beschleunigung_plt(), steigung_plt(), leistung1_plt(), leistung2_plt()
plt.show(block=False)
input("Enter drücken zum Schließen der Plots und Öffnen der Akku-Simulation...")
plt.close("all")


def battery1_plt(battery, battery_typ: str):
    df = Kb1.motorstrom()
    sim = BatterySimulator(battery)
    sim.simulate(df)

    plotting_utils.plot_soc_zeit(sim.zeit_verlauf, sim.soc_verlauf, battery_typ)
    plotting_utils.plot_spannung_zeit(sim.zeit_verlauf, sim.spannung_verlauf, battery_typ)

def battery2_plt(battery, battery_typ: str):
    df = Kb2.motorstrom()
    sim = BatterySimulator(battery)
    sim.simulate(df)

    plotting_utils.plot_soc_zeit(sim.zeit_verlauf, sim.soc_verlauf, battery_typ)
    plotting_utils.plot_spannung_zeit(sim.zeit_verlauf, sim.spannung_verlauf, battery_typ)


battery1_plt(Battery_LiPo(capacity_nom_Ah_cell= 30.0), "LiPo"), battery1_plt(Battery_NMC(capacity_nom_Ah_cell=30.0), "NMC")
battery2_plt(Battery_LiPo(capacity_nom_Ah_cell= 30.0), "LiPo"), battery2_plt(Battery_NMC(capacity_nom_Ah_cell= 30.0), "NMC")

plt.show(block=False)
input("Enter drücken zum Schließen der Plots...")
plt.close("all")