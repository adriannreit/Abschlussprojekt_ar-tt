# Abschlussprojekt_ar-tt
Python-Anwendung zur Auslegung eines E-Bikes auf Basis realer GPS-Tracking-Daten. Basierend auf einem aufgezeichneten Fahrt-Datensatz mit Zeitstempel, Höhe, Position und Temperatur werden Geschwindigkeit, Beschleunigung, Steigung, Kraft, Leistung und Motorstrom berechnet und daraus die benötigte Motorleistung abgeleitet. Außerdem wird der Ladezustand (SoC) und Spannungsverlauf für zwei unterschiedliche Akku-Typen (LiPo und NMC) über die Fahrt simuliert und verglichen.



## Projektstruktur

Im folgenden ist die Projektstruktur angegeben. Gesteuert wird das gesamte Projekt aus Main.py:

```
.
├── Main.py                        # Orchestriert Auswertung, Simulation und Plots
├── gps_auswertung.py               # GPSAuswertung: CSV einlesen, Kinematik berechnen
├── geo_utils.py                    # Zustandslose geometrische Hilfsfunktionen
├── kraft_Leistungsberechnung.py     # Kraftberechnung(GPSAuswertung):
│										Kraft/Leistung/Motorstrom
├── luftdruckberechnung.py           # Luftdichte in Abhängigkeit von Höhe & Temperatur
├── plotting_utils.py                # Plot-Funktionen (Geschwindigkeit, SoC, 			
|										Höhenprofil, ...)
├── Battery/
│   ├── battery_base.py             # BatteryBase: gemeinsame Akku-Logik
│   ├── battery_LiPo.py             # Battery_LiPo(BatteryBase): LiPo-Kennlinie
│   ├── battery_NMC.py              # Battery_NMC(BatteryBase): NMC-Kennlinie
│   └── battery_simulator.py        # BatterySimulator: SoC-/Spannungsverlauf simulieren
└── final_project_input_data.csv     # GPS-Rohdaten (Zeitstempel, lat/lon, ele, 												temperature)
```



### Klassendiagramm


![Klassendiagramm](D:\MCI\Programmieren\Abschlussprojekt\Abschlussprojekt_ar-tt\img\klassendiagramm.png)





### Aktivitätsdiagramm


![Aktivitätsdiagramm](D:\MCI\Programmieren\Abschlussprojekt\Abschlussprojekt_ar-tt\img\aktivitaetsdiagramm.png)

## Verwendung

Die Simulation und das Aufrufen der Plots werden aus dem Script `Main.py` gesteuert. 

```python
python Main.py
```

Nach Ausführung werden die GPS-Daten aus `final_project_input_data.csv` ausgelesen und daraus schrittweise folgende Punkte berechnet:

**1. Kinematik** (`GPSAuswertung`): Geschwindigkeit, Beschleunigung, Steigung, Höhenprofil – geglättet 	über einen gleitenden Mittelwert, um GPS-Messrauschen auszugleichen.

**2. Kräfte & Leistung** (`Kraftberechnung`, erbt von `GPSAuswertung`): Luftwiderstand, Antriebskraft (Beschleunigung + Steigung + Luftwiderstand), mechanische Leistung, Drehmoment und daraus den Motorstrom.

**3. Batteriesimulation** (`BatterySimulator`): wendet das Motorstrom-Profil Zeitschritt für Zeitschritt auf ein `Battery_LiPo`- bzw. `Battery_NMC`-Objekt an und zeichnet SoC- und Spannungsverlauf auf.



Daraufhin werden die Plots Geschwindigkeit, Beschleunigung, Höhenprofil und Leistung angezeigt, wobei <Enter> im Terminal diese schließt. Darauf folgend werden die Plots der SoC und Spannung für die verschiedenen Akku-Typen angezeigt.



## Tests

Die Scripts `gps_auswertung` und `kraft_leistungsberechnung ` sind mit Unit-Tests versehen. Hierbei werden verschiedene Funktionen auf ihre korrekte Funktionalität geprüft. Die Tests können mittels

```python
python -m pytest
```

ausgeführt und somit die Software geprüft werden.