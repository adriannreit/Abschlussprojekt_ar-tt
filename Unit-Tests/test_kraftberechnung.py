import numpy as np
import pandas as pd
import pytest

from kraft_Leistungsberechnung import Kraftberechnung


@pytest.fixture
def kb():
    """Erzeugt ein Kraftberechnung-Objekt mit vorbereiteten Testdaten."""

    obj = Kraftberechnung("dummy.csv", masse_kg=100)

    obj.ele_col = "hoehe"
    obj.temp_col = "temperatur"

    obj.df = pd.DataFrame({
        "geschw._m/s": [5.0, 10.0],
        "beschleunigung": [0.5, 1.0],
        "steigung": [0.0, 0.1],
        "hoehe": [100, 100],
        "temperatur": [20, 20],
        "delta_t": [1.0, 1.0],
        "rollwiderstandskraft": [3.924, 3.904]
    })

    return obj


def test_luftwiderstandskraft(monkeypatch, kb):
    """Testet die Berechnung des Luftwiderstands."""

    monkeypatch.setattr(
        "kraft_Leistungsberechnung.rho",
        lambda hoehe, temp: np.array([1.2, 1.2])
    )

    df = kb.luftwiderstandskraft()

    erwartet = (
        0.5
        * 1.2
        * kb.cW
        * (df["geschw._m/s"] ** 2)
    )

    assert np.allclose(
        df["Luftwiderstandskraft"],
        erwartet
    )


def test_rollwiderstandskraft(kb):
    """Testet die Rollwiderstandskraft."""

    df = kb.rollwiderstandskraft()

    erwartet = (
        0.004
        * kb.masse_kg
        * 9.81
        * np.cos(df["steigung"])
    )

    assert np.allclose(
        df["rollwiderstandskraft"],
        erwartet
    )


def test_kraft(monkeypatch, kb):
    """Testet die Gesamtkraft."""

    monkeypatch.setattr(
        "kraft_Leistungsberechnung.rho",
        lambda hoehe, temp: np.array([1.2, 1.2])
    )

    kb.luftwiderstandskraft()
    kb.rollwiderstandskraft()

    df = kb.kraft()

    erwartet = (
        kb.masse_kg * df["beschleunigung"]
        + kb.masse_kg * 9.81 * np.sin(df["steigung"])
        + df["Luftwiderstandskraft"]
        + df["rollwiderstandskraft"]
    )

    assert np.allclose(
        df["Kraft"],
        erwartet
    )


def test_leistung(monkeypatch, kb):
    """Testet die Leistungsberechnung."""

    monkeypatch.setattr(
        "kraft_Leistungsberechnung.rho",
        lambda hoehe, temp: np.array([1.2, 1.2])
    )

    kb.luftwiderstandskraft()
    kb.rollwiderstandskraft()
    kb.kraft()

    df = kb.leistung()

    erwartet = (
        df["Kraft"]
        * df["geschw._m/s"]
    )

    assert np.allclose(
        df["Leistung"],
        erwartet
    )


def test_drehmoment(monkeypatch, kb):
    """Testet die Drehmomentberechnung."""

    monkeypatch.setattr(
        "kraft_Leistungsberechnung.rho",
        lambda hoehe, temp: np.array([1.2, 1.2])
    )

    kb.luftwiderstandskraft()
    kb.rollwiderstandskraft()
    kb.kraft()

    df = kb.drehmoment()

    erwartet = (
        df["Kraft"]
        * kb.rad
    )

    assert np.allclose(
        df["Drehmoment"],
        erwartet
    )


def test_motorstrom(monkeypatch, kb):
    """Testet die Motorstromberechnung."""

    monkeypatch.setattr(
        "kraft_Leistungsberechnung.rho",
        lambda hoehe, temp: np.array([1.2, 1.2])
    )

    kb.luftwiderstandskraft()
    kb.rollwiderstandskraft()
    kb.kraft()
    kb.drehmoment()

    df = kb.motorstrom()

    erwartet = (
        df["Drehmoment"]
        / 1.5
    )

    assert np.allclose(
        df["Motorstrom"],
        erwartet
    )