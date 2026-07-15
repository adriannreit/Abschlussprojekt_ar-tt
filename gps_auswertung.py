from pathlib import Path
import numpy as np
import pandas as pd
from geo_utils import haversine_distance, distance_3d, steigungswinkel, himmelsrichtung, moving_average, wetter_daten_auslesen


class GPSAuswertung:
    def __init__(self, gps_data) -> None:
        self.gps_data = gps_data
        self.df = None
        self.lat_col = None
        self.lon_col = None
        self.ele_col = None
        self.time_col = None
        self.temp_col = None

    def set_data_source(self, gps_data) -> None:
        self.gps_data = gps_data
        self.df = None
        self.lat_col = None
        self.lon_col = None
        self.ele_col = None
        self.time_col = None
        self.temp_col = None

    def _resolve_path(self, path):
        if isinstance(path, Path):
            return path

        path_obj = Path(path)
        if path_obj.is_absolute():
            return path_obj
        return (Path(__file__).resolve().parent / path_obj).resolve()

    def csv_read(self):
        if isinstance(self.gps_data, pd.DataFrame):
            self.df = self.gps_data.copy()
            return self.df

        path = self._resolve_path(self.gps_data)
        if not path.exists():
            raise FileNotFoundError(f"Datei nicht gefunden: {path}")

        try:
            self.df = pd.read_csv(path, sep=";")
        except Exception:
            self.df = pd.read_csv(path)
        return self.df

    def prepare_data(self, lat="lat", lon="lon", ele="ele", time="time", temp="temperature"):
        if self.df is None:
             self.csv_read()

        if self.df is None:
            raise ValueError("Konnte die GPS-Daten nicht lesen; self.df ist None.")

        required = [lat, lon, ele, time, temp]
        missing = [col for col in required if col not in self.df.columns]
        if missing:
            raise ValueError(f"Fehlende Spalten: {missing}")

        self.lat_col = lat
        self.lon_col = lon
        self.ele_col = ele
        self.time_col = time
        self.temp_col = temp

        self.df[self.time_col] = pd.to_datetime(self.df[self.time_col], errors="coerce")
        self.df = self.df.dropna(subset=[self.time_col]).sort_values(self.time_col).reset_index(drop=True)

        self.df[self.lat_col] = pd.to_numeric(self.df[self.lat_col], errors="coerce")
        self.df[self.lon_col] = pd.to_numeric(self.df[self.lon_col], errors="coerce")
        self.df[self.ele_col] = pd.to_numeric(self.df[self.ele_col], errors="coerce")
        self.df[self.temp_col] = pd.to_numeric(self.df[self.temp_col], errors="coerce")
        return self.df

    def geschwindigkeit(self):
        if self.df is None or None in (self.lat_col, self.lon_col, self.ele_col, self.time_col):
            self.prepare_data()

        if self.df is None or None in (self.lat_col, self.lon_col, self.ele_col, self.time_col):
            raise ValueError("Daten müssen mit prepare_data() vorbereitet werden, bevor geschwindigkeit() aufgerufen wird.")

        self.df["delta_t"] = (self.df[self.time_col].shift(-1) - self.df[self.time_col]).dt.total_seconds().fillna(0)

        lat1 = self.df[self.lat_col]
        lon1 = self.df[self.lon_col]
        lat2 = self.df[self.lat_col].shift(-1)
        lon2 = self.df[self.lon_col].shift(-1)


        self.df["h_distance"] = haversine_distance(lat1, lon1, lat2, lon2).fillna(0)
        self.df["d_ele"] = (self.df[self.ele_col].shift(-1) - self.df[self.ele_col]).fillna(0)
        self.df["distance"] = distance_3d(self.df["h_distance"], self.df["d_ele"]).fillna(0)
        self.df["geschw._m/s"] = np.where(self.df["delta_t"] > 0, self.df["distance"] / self.df["delta_t"], 0)
        self.df["geschw._m/s"]= moving_average(self.df["geschw._m/s"], window_size=5)
        self.df["geschw._km/h"] = self.df["geschw._m/s"] * 3.6

        return self.df

    def beschleunigung(self):
        if self.df is None or "geschw._m/s" not in self.df.columns:
            self.geschwindigkeit()

        if self.df is None or "geschw._m/s" not in self.df.columns:
            raise ValueError("Daten müssen mit geschwindigkeit() vorbereitet werden, bevor beschleunigung() aufgerufen wird.")

        self.df["delta_v"] = (self.df["geschw._m/s"].shift(-1) - self.df["geschw._m/s"]).fillna(0)
        self.df["beschleunigung"] = np.where(self.df["delta_t"] > 0, self.df["delta_v"] / self.df["delta_t"], 0)
        self.df["beschleunigung"]= moving_average(self.df["beschleunigung"], window_size=5)

        return self.df

    def steigung(self):
        if self.df is None or "d_ele" not in self.df.columns or "h_distance" not in self.df.columns:
            self.geschwindigkeit()
        
        if self.df is None or "d_ele" not in self.df.columns or "h_distance" not in self.df.columns:
            raise ValueError("Daten konnten nicht ausgelesen oder vorberitet werden.")
            
        self.df["steigung"]= steigungswinkel(self.df["d_ele"], self.df["h_distance"])
        self.df["steigung"]= moving_average(self.df["steigung"], window_size=5)

        return self.df
    
    def himmelsrichtung(self):
        """Berechnet Himmelsrichtung und Azimut für alle Streckenabschnitte."""
        if self.df is None or None in (self.lat_col, self.lon_col):
            self.prepare_data()

        if self.df is None or None in (self.lat_col, self.lon_col):
            raise ValueError("Daten müssen mit prepare_data() vorbereitet werden, bevor himmelsrichtung() aufgerufen wird.")
        
        directions_list = [None] * len(self.df)
        azimuth_list = [None] * len(self.df)

        for i in range(len(self.df) - 1):
            lat1 = self.df[self.lat_col].iloc[i]
            lon1 = self.df[self.lon_col].iloc[i]
            lat2 = self.df[self.lat_col].iloc[i + 1]
            lon2 = self.df[self.lon_col].iloc[i + 1]

            directions, azimuth_deg = himmelsrichtung(lat1, lon1, lat2, lon2)
            directions_list[i] = directions
            azimuth_list[i] = azimuth_deg

        self.df["himmelsrichtung"] = directions_list
        self.df["azimuth_deg"] = azimuth_list

        return self.df
    
    def wind(self):
        if self.df is None or None in (self.lat_col, self.lon_col, self.time_col):
            self.prepare_data()

        if self.df is None or None in (self.lat_col, self.lon_col, self.time_col):
            raise ValueError("Daten müssen mit prepare_data() vorbereitet werden.")

        wind_geschw = []
        wind_richtung_dg = []

        for i in range(len(self.df)):
            lat = self.df[self.lat_col].iloc[i]
            lon = self.df[self.lon_col].iloc[i]
            timestamp = self.df[self.time_col].iloc[i]

            data = wetter_daten_auslesen(lat, lon, timestamp)
            wind_geschw.append(np.nan if data.get("wspd") is None else data["wspd"])
            wind_richtung_dg.append(np.nan if data.get("wdir") is None else data["wdir"])

        self.df = self.df.copy()
        self.df["wind_geschw"] = pd.Series(wind_geschw, index=self.df.index)
        self.df["wind_richtung_dg"] = pd.Series(wind_richtung_dg, index=self.df.index)

        return self.df

if __name__ == "__main__":
    gps = GPSAuswertung("final_project_input_data.csv")
    df = gps.geschwindigkeit()
    #df = gps.beschleunigung()
    #df = gps.steigung()
    df = gps.himmelsrichtung()
    #df = gps.wind()
    print(df[["h_distance","geschw._m/s", "himmelsrichtung", "azimuth_deg" ]].head(30))

