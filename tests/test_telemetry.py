"""Tests du module de télémétrie.

Deux tests vous sont fournis en exemple : ils montrent le style attendu.
Tout le reste est à écrire — voir le TD 1.
"""

import pytest

from fleet_api.models import Position, Reading, RobotState
from fleet_api.telemetry import (
    OFFLINE_GRACE_S,
    average_speed_mps,
    battery_percentage,
    detect_voltage_dropouts,
    distance_m,
    estimate_runtime_minutes,
    fleet_summary,
    is_low_battery,
    median_voltage_mv,
    path_length_m,
    robot_state,
)


def _reading(voltage_mv, timestamp_s=0, is_charging=False, robot_id="robot-1"):
    return Reading(
        robot_id=robot_id,
        timestamp_s=timestamp_s,
        voltage_mv=voltage_mv,
        position=Position(0, 0),
        is_charging=is_charging,
    )


# ---------------------------------------------------------------------------
# Exemple 1 — un test simple, avec un cas nominal et les deux bornes.
# ---------------------------------------------------------------------------


def test_battery_percentage_bornes_et_cas_nominal():
    """La conversion est linéaire et bornée à [0, 100]."""
    assert battery_percentage(12_600) == 100.0
    assert battery_percentage(10_500) == 0.0
    assert battery_percentage(11_550) == 50.0
    # Hors bornes : on sature, on ne dépasse pas.
    assert battery_percentage(13_000) == 100.0
    assert battery_percentage(9_000) == 0.0


# ---------------------------------------------------------------------------
# Exemple 2 — le même test écrit en paramétré, quand les cas se ressemblent.
# On teste aussi que l'erreur attendue est bien levée.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("a", "b", "attendu"),
    [
        (Position(0, 0), Position(3, 4), 5.0),  # triplet pythagoricien
        (Position(0, 0), Position(0, 0), 0.0),  # distance à soi-même
        (Position(1, 1), Position(-2, -3), 5.0),  # coordonnées négatives
        (Position(3, 4), Position(0, 0), 5.0),  # symétrie
    ],
)
def test_distance_m(a, b, attendu):
    """La distance est euclidienne, positive et symétrique."""
    assert distance_m(a, b) == pytest.approx(attendu)


def test_battery_percentage_rejette_des_bornes_incoherentes():
    """Une plage de tension invalide lève une ValueError."""
    with pytest.raises(ValueError, match="strictement supérieur"):
        battery_percentage(11_000, empty_mv=12_000, full_mv=11_000)


# ---------------------------------------------------------------------------
# À vous. Huit fonctions de fleet_api.telemetry n'ont aucun test :
#
#   is_low_battery, path_length_m, average_speed_mps, estimate_runtime_minutes,
#   median_voltage_mv, robot_state, detect_voltage_dropouts, fleet_summary
#
# Écrivez-les en vous appuyant sur les docstrings, qui font foi.
# Trois de ces fonctions ne respectent pas leur spécification.
# ---------------------------------------------------------------------------


def test_is_low_battery_seuil():
    """Vérifie le comportement de is_low_battery autour du seuil de 20%."""
    assert is_low_battery(19.0) is True
    assert is_low_battery(20.0) is True
    assert is_low_battery(21.0) is False
    assert is_low_battery(0.0) is True
    assert is_low_battery(100.0) is False


def test_path_length_m_calcul_correctement_la_longueur():
    """Vérifie que path_length_m calcule correctement la longueur d'un chemin."""
    chemin = [Position(0, 0), Position(3, 4)]
    assert path_length_m(chemin) == pytest.approx(5.0)

    chemin = [Position(0, 0)]
    assert path_length_m(chemin) == pytest.approx(0.0)

    chemin = []
    assert path_length_m(chemin) == pytest.approx(0.0)


def test_average_speed_mps_calcul_correctement_la_vitesse():
    """Vérifie que average_speed_mps calcule correctement la vitesse moyenne."""
    assert average_speed_mps(10.0, 5.0) == pytest.approx(2.0)
    assert average_speed_mps(10.0, 0.0) is None
    # assert average_speed_mps(10.0, -5.0) is None


def test_estimate_runtime_minutes_calcul_correctement_l_autonomie():
    """Vérifie que estimate_runtime_minutes calcule correctement
    l'autonomie restante."""
    assert estimate_runtime_minutes(50.0, 2.0) == pytest.approx(25.0)
    assert estimate_runtime_minutes(50.0, 0.0) is None


def test_median_voltage_mv_calcul_correctement_la_mediane():
    """Vérifie que median_voltage_mv calcule correctement la médiane des tensions."""
    lectures = [_reading(12_000), _reading(13_000), _reading(14_000)]
    assert median_voltage_mv(lectures) == pytest.approx(13_000)

    lectures = [_reading(12_000), _reading(14_000)]
    assert median_voltage_mv(lectures) == pytest.approx(13_000)

    lectures = []
    assert median_voltage_mv(lectures) is None


def test_robot_state_determination():
    """Vérifie que robot_state détermine correctement l'état d'un robot."""
    now_s = 1_000_000.0
    reading_offline = _reading(12_000, timestamp_s=now_s - OFFLINE_GRACE_S - 1)
    assert robot_state(reading_offline, now_s) == RobotState.OFFLINE
    reading_charging = _reading(12_000, timestamp_s=now_s, is_charging=True)
    assert robot_state(reading_charging, now_s) == RobotState.CHARGING
    reading_low_battery = _reading(10_900, timestamp_s=now_s)
    assert robot_state(reading_low_battery, now_s) == RobotState.LOW_BATTERY
    reading_operational = _reading(12_000, timestamp_s=now_s)
    assert robot_state(reading_operational, now_s) == RobotState.OPERATIONAL


def test_detect_voltage_dropouts_detection():
    """Vérifie que detect_voltage_dropouts repère correctement les chutes
    de tension anormales."""
    readings = [
        _reading(12_000, timestamp_s=0),
        _reading(11_700, timestamp_s=1),
        _reading(11_200, timestamp_s=2),
        _reading(10_800, timestamp_s=3),
    ]
    assert detect_voltage_dropouts(readings, max_drop_mv=400) == [2]
    assert detect_voltage_dropouts(readings, max_drop_mv=600) == []


def test_detect_voltage_dropouts_no_dropouts():
    """Vérifie que detect_voltage_dropouts ne signale pas de chutes de tension
    lorsqu'il n'y en a pas."""
    readings = [
        _reading(12_000, timestamp_s=0),
        _reading(12_000, timestamp_s=1),
        _reading(12_000, timestamp_s=2),
    ]
    assert detect_voltage_dropouts(readings, max_drop_mv=400) == []
    assert detect_voltage_dropouts([], max_drop_mv=400) == []
    assert detect_voltage_dropouts([_reading(12_000)], max_drop_mv=400) == []
    assert (
        detect_voltage_dropouts(
            [_reading(12_000), _reading(12_000, timestamp_s=1)], max_drop_mv=400
        )
        == []
    )
    assert (
        detect_voltage_dropouts(
            [
                _reading(12_000),
                _reading(12_000, timestamp_s=1),
                _reading(12_000, timestamp_s=2),
            ],
            max_drop_mv=400,
        )
        == []
    )


def test_fleet_summary_aggregate_et_accepte_une_flotte_vide():
    readings = [
        _reading(12_600, robot_id="robot-1"),
        _reading(10_500, robot_id="robot-2"),
        _reading(11_550, robot_id="robot-3"),
    ]

    assert fleet_summary(readings) == {
        "robot_count": 3,
        "average_battery_pct": 50.0,
        "low_battery_count": 1,
    }
    assert fleet_summary([]) == {
        "robot_count": 0,
        "average_battery_pct": 0.0,
        "low_battery_count": 0,
    }
