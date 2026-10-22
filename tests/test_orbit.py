
import math
import pytest

from rocket_sim.orbit import (
    EARTH_RADIUS,
    circular_orbital_velocity,
    gravitational_acceleration,
    orbital_period,
)


def test_gravity_at_400_km_altitude():
    radius = EARTH_RADIUS + 400_000
    assert gravitational_acceleration(radius) == pytest.approx(8.6943, abs=0.001)


def test_circular_velocity_at_400_km_altitude():
    radius = EARTH_RADIUS + 400_000
    assert circular_orbital_velocity(radius) == pytest.approx(7672.6, abs=1.0)


def test_orbital_period_at_400_km_altitude():
    radius = EARTH_RADIUS + 400_000
    period_minutes = orbital_period(radius) / 60
    assert period_minutes == pytest.approx(92.41, abs=0.05)


def test_higher_orbit_has_lower_gravity():
    low = EARTH_RADIUS + 200_000
    high = EARTH_RADIUS + 400_000
    assert gravitational_acceleration(high) < gravitational_acceleration(low)


def test_higher_orbit_has_lower_circular_velocity():
    low = EARTH_RADIUS + 200_000
    high = EARTH_RADIUS + 400_000
    assert circular_orbital_velocity(high) < circular_orbital_velocity(low)


def test_higher_orbit_has_longer_period():
    low = EARTH_RADIUS + 200_000
    high = EARTH_RADIUS + 400_000
    assert orbital_period(high) > orbital_period(low)


@pytest.mark.parametrize("radius", [0, -1, -1000])
def test_nonpositive_radius_raises_value_error(radius):
    with pytest.raises(ValueError):
        gravitational_acceleration(radius)


@pytest.mark.parametrize("radius", [math.nan, math.inf, -math.inf])
def test_nonfinite_radius_raises_value_error(radius):
    with pytest.raises(ValueError):
        circular_orbital_velocity(radius)
