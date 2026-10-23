import math

import pytest

from rocket_sim.propulsion import thrust_newtons


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