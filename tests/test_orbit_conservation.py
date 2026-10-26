
"""Numerical conservation tests for orbital propagation."""

import math

from rocket_sim.integrator import propagate
from rocket_sim.orbit import EARTH_RADIUS, circular_orbital_velocity


def circular_orbit_setup():
    """Return a circular orbit state and its derived gravitational parameter."""
    radius_m = EARTH_RADIUS + 400_000
    speed_m_s = circular_orbital_velocity(radius_m)
    mu_m3_s2 = speed_m_s**2 * radius_m

    initial_state = (radius_m, 0.0, 0.0, speed_m_s)
    return radius_m, speed_m_s, mu_m3_s2, initial_state


def specific_orbital_energy(state, mu_m3_s2):
    """Calculate specific mechanical energy in J/kg."""
    x, y, vx, vy = state
    radius_m = math.hypot(x, y)
    speed_squared = vx**2 + vy**2

    return 0.5 * speed_squared - mu_m3_s2 / radius_m


def specific_angular_momentum(state):
    """Calculate the signed z-component of specific angular momentum."""
    x, y, vx, vy = state
    return x * vy - y * vx


def test_orbital_energy_is_conserved_during_propagation():
    _, _, mu_m3_s2, initial = circular_orbit_setup()

    trajectory = propagate(
        initial,
        duration_s=16_000,
        step_s=10,
    )

    initial_energy = specific_orbital_energy(initial, mu_m3_s2)

    maximum_relative_drift = max(
        abs(specific_orbital_energy(state, mu_m3_s2) - initial_energy)
        / abs(initial_energy)
        for state in trajectory
    )

    assert maximum_relative_drift < 1e-6


def test_angular_momentum_is_conserved_during_propagation():
    _, _, _, initial = circular_orbit_setup()

    trajectory = propagate(
        initial,
        duration_s=16_000,
        step_s=10,
    )

    initial_momentum = specific_angular_momentum(initial)

    maximum_relative_drift = max(
        abs(specific_angular_momentum(state) - initial_momentum)
        / abs(initial_momentum)
        for state in trajectory
    )

    assert maximum_relative_drift < 1e-6


def test_smaller_time_step_improves_circular_orbit_position_accuracy():
    radius_m, speed_m_s, _, initial = circular_orbit_setup()
    duration_s = 5_600

    coarse_final = propagate(
        initial,
        duration_s=duration_s,
        step_s=40,
    )[-1]

    fine_final = propagate(
        initial,
        duration_s=duration_s,
        step_s=20,
    )[-1]

    angular_rate_rad_s = speed_m_s / radius_m
    angle_rad = angular_rate_rad_s * duration_s

    exact_x = radius_m * math.cos(angle_rad)
    exact_y = radius_m * math.sin(angle_rad)

    coarse_error_m = math.hypot(
        coarse_final[0] - exact_x,
        coarse_final[1] - exact_y,
    )

    fine_error_m = math.hypot(
        fine_final[0] - exact_x,
        fine_final[1] - exact_y,
    )

    assert coarse_error_m > 0
    assert fine_error_m < coarse_error_m
