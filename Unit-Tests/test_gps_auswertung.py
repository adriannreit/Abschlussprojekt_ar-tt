import numpy as np
import pandas as pd
import pytest

from gps_auswertung import GPSAuswertung


@pytest.fixture
def test_df():
    return pd.DataFrame({
        "lat": [48.0, 48.0001, 48.0002],
        "lon": [9.0, 9.0001, 9.0002],
        "ele": [500, 501, 502],
        "temperature": [20, 20, 20],
        "time": [
            "2025-01-01 12:00:00",
            "2025-01-01 12:00:10",
            "2025-01-01 12:00:20",
        ]
    })


@pytest.fixture
def gps(test_df):
    return GPSAuswertung(test_df)


def test_prepare_data(gps):

    df = gps.prepare_data()

    assert gps.lat_col == "lat"
    assert gps.lon_col == "lon"
    assert gps.ele_col == "ele"
    assert gps.time_col == "time"
    assert gps.temp_col == "temperature"

    assert pd.api.types.is_datetime64_any_dtype(df["time"])


def test_geschwindigkeit(monkeypatch, gps):

    monkeypatch.setattr(
        "gps_auswertung.haversine_distance",
        lambda lat1, lon1, lat2, lon2: pd.Series([10.0, 10.0, 0.0])
    )

    monkeypatch.setattr(
        "gps_auswertung.distance_3d",
        lambda h, d: pd.Series([10.0, 10.0, 0.0])
    )

    monkeypatch.setattr(
        "gps_auswertung.moving_average",
        lambda x, window_size: x
    )

    df = gps.geschwindigkeit()

    assert np.isclose(df["geschw._m/s"].iloc[0], 1.0)
    assert np.isclose(df["geschw._m/s"].iloc[1], 1.0)


def test_beschleunigung(monkeypatch, gps):

    monkeypatch.setattr(
        "gps_auswertung.moving_average",
        lambda x, window_size: x
    )

    gps.prepare_data()

    gps.df["geschw._m/s"] = [2, 4, 6]
    gps.df["delta_t"] = [2, 2, 0]

    df = gps.beschleunigung()

    assert np.isclose(df["beschleunigung"].iloc[0], 1.0)


def test_steigung(monkeypatch, gps):

    monkeypatch.setattr(
        "gps_auswertung.steigungswinkel",
        lambda d_ele, h: pd.Series([0.1, 0.2, 0.0])
    )

    monkeypatch.setattr(
        "gps_auswertung.moving_average",
        lambda x, window_size: x
    )

    gps.prepare_data()

    gps.df["d_ele"] = [1, 1, 0]
    gps.df["h_distance"] = [10, 10, 0]

    df = gps.steigung()

    assert df["steigung"].iloc[0] == 0.1
    assert df["steigung"].iloc[1] == 0.2


def test_himmelsrichtung(monkeypatch, gps):

    monkeypatch.setattr(
        "gps_auswertung.himmelsrichtung",
        lambda lat1, lon1, lat2, lon2: ("N", 0)
    )

    df = gps.himmelsrichtung()

    assert df["himmelsrichtung"].iloc[0] == "N"
    assert df["azimuth_deg"].iloc[0] == 0


def test_wind(monkeypatch, gps):

    monkeypatch.setattr(
        "gps_auswertung.wetter_daten_auslesen",
        lambda lat, lon, timestamp: {
            "wspd": 5.5,
            "wdir": 180
        }
    )

    df = gps.wind()

    assert all(df["wind_geschw"] == 5.5)
    assert all(df["wind_richtung_dg"] == 180)



#---------------------Fehlerfälle testen----------------------

# Datei existiert nicht
def test_csv_read_file_not_found():
    gps = GPSAuswertung("datei_gibt_es_nicht.csv")

    with pytest.raises(FileNotFoundError):
        gps.csv_read()


# fehlende Spalten im df
def test_prepare_data_missing_column():

    df = pd.DataFrame({
        "lat": [48],
        "lon": [9],
        "ele": [500],
        # temperature fehlt
        "time": ["2025-01-01"]
    })

    gps = GPSAuswertung(df)

    with pytest.raises(ValueError, match="Fehlende Spalten"):
        gps.prepare_data()


# Ungültige Zeitwerte
def test_prepare_data_invalid_time():

    df = pd.DataFrame({
        "lat":[48],
        "lon":[9],
        "ele":[500],
        "temperature":[20],
        "time":["das ist kein Datum"]
    })

    gps = GPSAuswertung(df)

    result = gps.prepare_data()

    assert result.empty


# leerer df
def test_prepare_data_empty_dataframe():

    df = pd.DataFrame(columns=[
        "lat",
        "lon",
        "ele",
        "temperature",
        "time"
    ])

    gps = GPSAuswertung(df)

    result = gps.prepare_data()

    assert result.empty