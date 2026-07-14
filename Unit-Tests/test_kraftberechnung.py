import numpy as np
import pandas as pd
import pytest

from kraft_Leistungsberechnung import Kraftberechnung


@pytest.fixture
def kb():
    """Erzeugt ein Kraftberechnung-Objekt mit Testdaten."""
    obj = Kraftberechnung("dummy.csv", masse_kg=100)

    obj.ele_col = "hoehe"
    obj.temp_col = "temperatur"

    obj.df = pd.DataFrame({
        "geschw._m/s": [5.0, 10.0],
        "beschleunigung": [0.5, 1.0],
        "steigung": [0.0, 0.1],
        "hoehe": [100, 100],
        "temperatur": [20, 20]
    })

    return obj


def test_luftwiderstandskraft(monkeypatch, kb):
    """Test der Luftwiderstandskraft."""

    monkeypatch.setattr(
        "kraft_Leistungsberechnung.rho",
        lambda hoehe, temp: np.array([1.2, 1.2])
    )

    df = kb.luftwiderstandskraft()

    erwartet = 0.5 * 1.2 * kb.cW * (df["geschw._m/s"] ** 2)

    assert np.allclose(df["Luftwiderstandskraft"], erwartet)


def test_kraft(monkeypatch, kb):
    """Test der Gesamtkraft."""

    monkeypatch.setattr(
        "kraft_Leistungsberechnung.rho",
        lambda hoehe, temp: np.array([1.2, 1.2])
    )

    kb.luftwiderstandskraft()
    df = kb.kraft()

    erwartet = (
        kb.masse_kg * df["beschleunigung"]
        + kb.masse_kg * 9.81 * np.sin(df["steigung"])
        + df["Luftwiderstandskraft"]
    )

    assert np.allclose(df["Kraft"], erwartet)


def test_leistung(monkeypatch, kb):
    monkeypatch.setattr(
        "kraft_Leistungsberechnung.rho",
        lambda hoehe, temp: np.array([1.2, 1.2])
    )

    kb.luftwiderstandskraft()
    kb.kraft()
    df = kb.leistung()

    erwartet = df["Kraft"] * df["geschw._m/s"]

    assert np.allclose(df["Leistung"], erwartet)


def test_drehmoment(monkeypatch, kb):
    monkeypatch.setattr(
        "kraft_Leistungsberechnung.rho",
        lambda hoehe, temp: np.array([1.2, 1.2])
    )

    kb.luftwiderstandskraft()
    kb.kraft()
    df = kb.drehmoment()

    erwartet = df["Kraft"] * kb.rad

    assert np.allclose(df["Drehmoment"], erwartet)


def test_motorstrom(monkeypatch, kb):
    monkeypatch.setattr(
        "kraft_Leistungsberechnung.rho",
        lambda hoehe, temp: np.array([1.2, 1.2])
    )

    kb.luftwiderstandskraft()
    kb.kraft()
    kb.drehmoment()
    df = kb.motorstrom()

    erwartet = df["Drehmoment"] / 0.35

    assert np.allclose(df["Motorstrom"], erwartet)