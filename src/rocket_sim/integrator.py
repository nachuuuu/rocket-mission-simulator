
"""Numerical integration methods for spacecraft motion."""

import math
from collections.abc import Sequence

from rocket_sim.dynamics import state_derivative

State = tuple[float, float, float, float]
TimedState = tuple[float, State]


def rk4_step(
    state: Sequence[float],
    dt_s: float,
) -> State:
    """Advance a four-component spacecraft state by one RK4 step."""
    try:
        dt_s = float(dt_s)
    except (TypeError, ValueError) as exc:
        raise TypeError("Time step must be numeric.") from exc

    if not math.isfinite(dt_s) or dt_s <= 0:
        raise ValueError("Time step must be finite and greater than zero.")

    initial = tuple(float(value) for value in state)

    if len(initial) != 4:
        raise ValueError("State must contain exactly four values.")

    k1 = state_derivative(initial)

    k2 = state_derivative(
        tuple(y + 0.5 * dt_s * k for y, k in zip(initial, k1))
    )

    k3 = state_derivative(
        tuple(y + 0.5 * dt_s * k for y, k in zip(initial, k2))
    )

    k4 = state_derivative(
        tuple(y + dt_s * k for y, k in zip(initial, k3))
    )

    result = tuple(
        y + (dt_s / 6.0) * (a + 2.0 * b + 2.0 * c + d)
        for y, a, b, c, d in zip(initial, k1, k2, k3, k4)
    )

    if not all(math.isfinite(value) for value in result):
        raise ValueError("Integration produced a non-finite state.")

    return result


def propagate_timed(
    initial_state: Sequence[float],
    duration_s: float,
    step_s: float,
) -> tuple[TimedState, ...]:
    """Propagate a spacecraft and return (time_s, state) at every step.

    The trajectory includes the initial state at t=0 and the final state
    at exactly duration_s. The final integration step is shortened when
    duration_s is not an exact multiple of step_s.

    State convention: [x_m, y_m, vx_m_s, vy_m_s].
    """
    try:
        duration_s = float(duration_s)
        step_s = float(step_s)
    except (TypeError, ValueError) as exc:
        raise TypeError("Duration and time step must be numeric.") from exc

    if not math.isfinite(duration_s) or duration_s < 0:
        raise ValueError("Duration must be finite and non-negative.")

    if not math.isfinite(step_s) or step_s <= 0:
        raise ValueError("Time step must be finite and greater than zero.")

    current = tuple(float(value) for value in initial_state)

    # Validate the initial state using the existing dynamics model.
    state_derivative(current)

    elapsed_s = 0.0
    trajectory: list[TimedState] = [(elapsed_s, current)]

    while elapsed_s < duration_s:
        next_time_s = min(duration_s, elapsed_s + step_s)
        dt_s = next_time_s - elapsed_s

        current = rk4_step(current, dt_s)
        elapsed_s = next_time_s
        trajectory.append((elapsed_s, current))

    return tuple(trajectory)


def propagate(
    initial_state: Sequence[float],
    duration_s: float,
    step_s: float,
) -> tuple[State, ...]:
    """Propagate a spacecraft and return its states without timestamps.

    This preserves the original propagate() API for existing callers.
    Use propagate_timed() when simulation timestamps are required.
    """
    timed_trajectory = propagate_timed(
        initial_state,
        duration_s,
        step_s,
    )

    return tuple(state for _, state in timed_trajectory)
