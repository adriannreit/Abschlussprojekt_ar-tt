from gps_auswertung import GPSAuswertung
from plotting_utils import plot_geschwindigkeit_zeit, plot_beschleunigung_zeit, plot_hoehenprofil_distanz
import matplotlib.pyplot as plt
from kraft_Leistungsberechnung import Kraftberechnung

gps = GPSAuswertung("final_project_input_data.csv")
Kb = Kraftberechnung("final_project_input_data.csv")

def geschwindigkeit_plt():
    df = gps.geschwindigkeit()
    plot_geschwindigkeit_zeit(df)

def beschleunigung_plt():
    df = gps.beschleunigung()
    plot_beschleunigung_zeit(df)

def steigung_plt():
    df = gps.steigung()
    plot_hoehenprofil_distanz(df)

geschwindigkeit_plt(), beschleunigung_plt(), steigung_plt()
plt.show()
