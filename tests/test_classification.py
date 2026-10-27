
"""Tests for orbital classification and insertion-condition sweeps."""

import math

import pytest

from rocket_sim.classification import (
    BOUND,
    EARTH_INTERSECTING,
    ESCAPING,
    classify_initial_state,
)
from rocket_sim.orbit import EARTH_MU, EARTH_RADIUS, circular_orbital_velocity
from rocket_sim.sweep import sweep_insertion_conditions


def test_circular_orbit_is_bound_and_does_not_intersect_earth():
    radius_m = EARTH_RADIUS + 400_000
    speed_m_s = circular_orbital_velocity(radius_m)

    result = classify_initial_state((radius_m, 0, 0, speed_m_s))

    assert result["classification"] == BOUND
    assert result["earth_intersecting"] is False
    assert result["periapsis_m"] == pytest.approx(radius_m)


def test_low_speed_tangential_insertion_intersects_earth():
    radius_m = EARTH_RADIUS + 400_000

    result = classify_initial_state((radius_m, 0, 0, 100.0))

    assert result["classification"] == EARTH_INTERSECTING
    assert result["periapsis_m"] < EARTH_RADIUS


def test_speed_above_escape_speed_is_classified_as_escaping():
    radius_m = EARTH_RADIUS + 400_000
    escape_speed_m_s = math.sqrt(2 * EARTH_MU / radius_m)

    result = classify_initial_state(
        (radius_m, 0, 0, escape_speed_m_s * 1.1)
    )

    assert result["classification"] == ESCAPING
    assert result["specific_energy_j_kg"] > 0


def test_inbound_unbound_trajectory_can_intersect_earth():
    radius_m = EARTH_RADIUS + 400_000

    # High inward radial speed and low tangential speed.
    result = classify_initial_state((radius_m, 0, -11_000, 1_000))

    assert result["classification"] == EARTH_INTERSECTING
    assert result["specific_energy_j_kg"] > 0
    assert result["radial_velocity_m_s"] < 0
    assert result["periapsis_m"] < EARTH_RADIUS


def test_outbound_unbound_trajectory_is_classified_as_escaping():
    radius_m = EARTH_RADIUS + 400_000

    result = classify_initial_state((radius_m, 0, 1_000, 11_000))

    assert result["classification"] == ESCAPING
    assert result["specific_energy_j_kg"] > 0
    assert result["radial_velocity_m_s"] > 0


def test_state_inside_earth_is_earth_intersecting():
    result = classify_initial_state((EARTH_RADIUS - 1, 0, 0, 1))

    assert result["classification"] == EARTH_INTERSECTING
    assert result["earth_intersecting"] is True


@pytest.mark.parametrize(
    "state",
    [
        (1, 2, 3),
        (0, 0, 0, 0),
        (math.nan, 0, 0, 1),
        (7_000_000, 0, math.inf, 1),
    ],
)
def test_classifier_rejects_invalid_states(state):
    with pytest.raises((TypeError, ValueError)):
        classify_initial_state(state)


def test_classifier_rejects_negative_energy_tolerance():
    with pytest.raises(ValueError):
        classify_initial_state((7_000_000, 0, 0, 7_500), -1)


def test_sweep_evaluates_every_speed_angle_combination():
    results = sweep_insertion_conditions(
        [7_000, 8_000],
        [-10, 0, 10],
    )

    assert len(results) == 6
    assert {row["insertion_speed_m_s"] for row in results} == {
        7_000.0,
        8_000.0,
    }
    assert {row["flight_path_angle_deg"] for row in results} == {
        -10.0,
        0.0,
        10.0,
    }


def test_sweep_records_classification_and_orbit_metrics():
    row = sweep_insertion_conditions([7_700], [0])[0]

    assert row["classification"] == BOUND
    assert row["altitude_m"] == 400_000
    assert row["periapsis_altitude_m"] > 0
    assert "specific_energy_j_kg" in row
    assert "eccentricity" in row


@pytest.mark.parametrize(
    "speeds,angles,altitude",
    [
        ([], [0], 400_000),
        ([7_500], [], 400_000),
        ([0], [0], 400_000),
        ([-1], [0], 400_000),
        ([7_500], [91], 400_000),
        ([7_500], [-91], 400_000),
        ([7_500], [0], -1),
    ],
)
def test_sweep_rejects_invalid_parameters(speeds, angles, altitude):
    with pytest.raises(ValueError):
        sweep_insertion_conditions(
            speeds,
            angles,
            altitude_m=altitude,
        )


def test_sweep_rejects_non_finite_speed():
    with pytest.raises(ValueError):
        sweep_insertion_conditions([math.inf], [0])


def test_sweep_rejects_negative_energy_tolerance():
    with pytest.raises(ValueError):
        sweep_insertion_conditions(
            [7_500],
            [0],
            energy_tolerance_j_kg=-1,
        )
