import math

import pytest

from rocket_sim.propulsion import (
    STANDARD_GRAVITY_M_S2,
    thrust_newtons,
    thrust_to_weight_ratio,
)

def test_thrust_calculation():
    assert thrust_newtons(2.0, 3000.0) == 6000.0


def test_zero_mass_flow_produces_zero_thrust():
    assert thrust_newtons(0.0, 3000.0) == 0.0


def test_zero_exhaust_velocity_produces_zero_thrust():
    assert thrust_newtons(2.0, 0.0) == 0.0


@pytest.mark.parametrize(
    "mass_flow_rate, exhaust_velocity",
    [
        (-1.0, 3000.0),
        (1.0, -3000.0),
    ],
)
def test_negative_inputs_raise_value_error(mass_flow_rate, exhaust_velocity):
    with pytest.raises(ValueError):
        thrust_newtons(mass_flow_rate, exhaust_velocity)


@pytest.mark.parametrize(
    "mass_flow_rate, exhaust_velocity",
    [
        (math.nan, 3000.0),
        (math.inf, 3000.0),
        (-math.inf, 3000.0),
        (1.0, math.nan),
        (1.0, math.inf),
        (1.0, -math.inf),
    ],
)
def test_nonfinite_inputs_raise_value_error(mass_flow_rate, exhaust_velocity):
    with pytest.raises(ValueError):
        thrust_newtons(mass_flow_rate, exhaust_velocity)

def test_twr_calculation():
    assert thrust_to_weight_ratio(19_613.3, 1000.0) == pytest.approx(2.0, abs=1e-4)


def test_twr_zero_thrust():
    assert thrust_to_weight_ratio(0.0, 1000.0) == 0.0


def test_twr_equals_one():
    thrust = 1000.0 * STANDARD_GRAVITY_M_S2
    assert thrust_to_weight_ratio(thrust, 1000.0) == pytest.approx(1.0)


def test_twr_custom_gravity():
    assert thrust_to_weight_ratio(2000.0, 100.0, gravity_m_s2=10.0) == pytest.approx(2.0)


@pytest.mark.parametrize(
    "thrust, mass, gravity",
    [
        (-1.0, 100.0, STANDARD_GRAVITY_M_S2),
        (100.0, 0.0, STANDARD_GRAVITY_M_S2),
        (100.0, -1.0, STANDARD_GRAVITY_M_S2),
        (100.0, 100.0, 0.0),
        (math.nan, 100.0, STANDARD_GRAVITY_M_S2),
        (math.inf, 100.0, STANDARD_GRAVITY_M_S2),
        (100.0, math.nan, STANDARD_GRAVITY_M_S2),
        (100.0, 100.0, math.inf),
    ],
)
def test_twr_invalid_inputs_raise_value_error(thrust, mass, gravity):
    with pytest.raises(ValueError):
        thrust_to_weight_ratio(thrust, mass, gravity)