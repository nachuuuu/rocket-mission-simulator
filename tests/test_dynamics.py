import math

import pytest

from rocket_sim.dynamics import state_derivative
from rocket_sim.orbit import (
    EARTH_RADIUS,
    circular_orbital_velocity,
    gravitational_acceleration,
)


EARTH_MU_LOCAL = 3.986004418e14


def test_state_derivative_returns_velocity_and_acceleration():
    result = state_derivative((7_000_000, 0, 0, 7_500))
    assert result[:2] == (0.0, 7_500.0)
    assert result[2] == pytest.approx(-EARTH_MU_LOCAL / 7_000_000**2)
    assert result[3] == 0.0


def test_gravity_acceleration_points_towards_earth_centre_in_all_quadrants():
    for x_m, y_m in ((7e6, 0), (0, 7e6), (-7e6, 0), (0, -7e6), (3e6, 4e6)):
        dx, dy, ax, ay = state_derivative((x_m, y_m, 1, 2))
        assert ax * x_m + ay * y_m < 0
        assert dx == 1
        assert dy == 2


def test_circular_orbit_state_has_tangential_velocity_and_radial_gravity():
    radius_m = EARTH_RADIUS + 400_000
    speed_m_s = circular_orbital_velocity(radius_m)
    dx, dy, ax, ay = state_derivative((radius_m, 0, 0, speed_m_s))

    assert dx == 0
    assert dy == pytest.approx(speed_m_s)
    assert ax == pytest.approx(-gravitational_acceleration(radius_m))
    assert ay == pytest.approx(0)


@pytest.mark.parametrize(
    "state",
    [
        (1, 2, 3),
        (1, 2, 3, 4, 5),
        (0, 0, 0, 0),
        (math.nan, 1, 2, 3),
        (1, math.inf, 2, 3),
        (1, 2, -math.inf, 3),
    ],
)
def test_invalid_state_raises_value_error(state):
    with pytest.raises(ValueError):
        state_derivative(state)


def test_non_numeric_state_raises_type_error():
    with pytest.raises(TypeError):
        state_derivative((1, 2, "not-a-number", 4))
