import math

import pytest

from rocket_sim.dynamics import state_derivative
from rocket_sim.integrator import propagate, rk4_step
from rocket_sim.orbit import EARTH_RADIUS, circular_orbital_velocity


def test_rk4_step_returns_four_finite_state_values():
    state = (7_000_000, 0, 0, 7_500)

    result = rk4_step(state, 1.0)

    assert len(result) == 4
    assert all(math.isfinite(value) for value in result)
    assert result != state


def test_rk4_step_matches_initial_derivative_for_small_step():
    state = (7_000_000, 0, 0, 7_500)
    dt_s = 0.001

    result = rk4_step(state, dt_s)
    derivative = state_derivative(state)

    for actual, initial, rate in zip(result, state, derivative):
        assert actual == pytest.approx(initial + rate * dt_s, abs=1e-5)


def test_propagation_includes_initial_and_final_states():
    initial = (7_000_000, 0, 0, 7_500)

    trajectory = propagate(initial, duration_s=10, step_s=1)

    assert len(trajectory) == 11
    assert trajectory[0] == initial
    assert all(len(state) == 4 for state in trajectory)


def test_zero_duration_returns_only_initial_state():
    initial = (7_000_000, 0, 0, 7_500)

    assert propagate(initial, 0, 1) == (initial,)


def test_propagation_handles_a_partial_final_step():
    initial = (7_000_000, 0, 0, 7_500)

    trajectory = propagate(initial, duration_s=2.5, step_s=1)

    assert len(trajectory) == 4


def test_circular_orbit_returns_near_initial_position_after_one_period():
    radius_m = EARTH_RADIUS + 400_000
    speed_m_s = circular_orbital_velocity(radius_m)
    period_s = 2 * math.pi * radius_m / speed_m_s

    initial = (radius_m, 0, 0, speed_m_s)
    trajectory = propagate(initial, duration_s=period_s, step_s=10)
    final = trajectory[-1]

    position_error_m = math.hypot(
        final[0] - initial[0],
        final[1] - initial[1],
    )

    assert position_error_m < 1_000


@pytest.mark.parametrize("dt_s", [0, -1, math.inf, math.nan])
def test_rk4_rejects_invalid_time_steps(dt_s):
    with pytest.raises(ValueError):
        rk4_step((7_000_000, 0, 0, 7_500), dt_s)


@pytest.mark.parametrize(
    ("duration_s", "step_s"),
    [
        (-1, 1),
        (1, 0),
        (1, -1),
        (math.inf, 1),
        (1, math.nan),
    ],
)
def test_propagate_rejects_invalid_duration_or_step(duration_s, step_s):
    with pytest.raises(ValueError):
        propagate((7_000_000, 0, 0, 7_500), duration_s, step_s)
