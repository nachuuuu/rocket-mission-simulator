"""Tests for ideal multistage rocket calculations."""

import math

import pytest

from rocket_sim.staging import RocketStage, ideal_staged_delta_v


def test_single_stage_matches_tsiolkovsky_equation():
    stage = RocketStage(
        dry_mass_kg=100,
        propellant_mass_kg=900,
        exhaust_velocity_m_s=3000,
    )

    result = ideal_staged_delta_v([stage], payload_mass_kg=100)

    expected = 3000 * math.log(1100 / 200)
    assert result == pytest.approx(expected)


def test_two_stage_delta_v_accounts_for_discarded_dry_mass():
    stages = [
        RocketStage(100, 900, 3000),
        RocketStage(50, 200, 3500),
    ]

    result = ideal_staged_delta_v(stages, payload_mass_kg=100)

    first_stage_delta_v = 3000 * math.log(1350 / 450)
    second_stage_delta_v = 3500 * math.log(350 / 150)

    assert result == pytest.approx(
        first_stage_delta_v + second_stage_delta_v
    )


def test_zero_payload_is_allowed():
    stage = RocketStage(100, 900, 3000)

    result = ideal_staged_delta_v([stage], payload_mass_kg=0)

    assert result == pytest.approx(3000 * math.log(1000 / 100))


def test_empty_stage_list_is_rejected():
    with pytest.raises(ValueError, match="At least one"):
        ideal_staged_delta_v([], payload_mass_kg=100)


@pytest.mark.parametrize("payload", [-1, float("inf"), float("nan")])
def test_invalid_payload_mass_is_rejected(payload):
    stage = RocketStage(100, 900, 3000)

    with pytest.raises(ValueError, match="Payload mass"):
        ideal_staged_delta_v([stage], payload_mass_kg=payload)


@pytest.mark.parametrize(
    ("dry_mass", "propellant_mass", "exhaust_velocity"),
    [
        (0, 900, 3000),
        (-1, 900, 3000),
        (100, 0, 3000),
        (100, -1, 3000),
        (100, 900, 0),
        (100, 900, -1),
        (float("inf"), 900, 3000),
        (100, float("nan"), 3000),
        (100, 900, float("inf")),
    ],
)
def test_invalid_stage_parameters_are_rejected(
    dry_mass, propellant_mass, exhaust_velocity
):
    with pytest.raises(ValueError):
        RocketStage(
            dry_mass_kg=dry_mass,
            propellant_mass_kg=propellant_mass,
            exhaust_velocity_m_s=exhaust_velocity,
        )


def test_non_stage_item_is_rejected():
    with pytest.raises(TypeError, match="RocketStage"):
        ideal_staged_delta_v([object()], payload_mass_kg=100)
