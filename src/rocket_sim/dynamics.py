"""Two-dimensional point-mass dynamics under Earth's central gravity."""

import math
from collections.abc import Sequence

from rocket_sim.orbit import EARTH_MU


STATE_SIZE = 4


def state_derivative(state: Sequence[float]) -> tuple[float, float, float, float]:
    """Return the derivative of a 2D orbital state.

    State convention: [x_m, y_m, vx_m_s, vy_m_s] in an inertial plane
    whose origin is Earth's centre. Position is in metres and velocity is
    in metres per second. The returned derivative is
    [vx_m_s, vy_m_s, ax_m_s2, ay_m_s2].

    The model includes only central inverse-square gravity; it excludes
    thrust, atmospheric drag, oblateness, and third-body effects.

    Raises:
        ValueError: If the state does not contain four finite values or if
            the position is at Earth's centre, where this model is singular.
        TypeError: If the state cannot be treated as a sequence of numbers.
    """
    try:
        values = tuple(float(value) for value in state)
    except (TypeError, ValueError) as exc:
        raise TypeError("State must be a sequence of four numeric values.") from exc

    if len(values) != STATE_SIZE:
        raise ValueError("State must contain exactly four values: [x, y, vx, vy].")

    if not all(math.isfinite(value) for value in values):
        raise ValueError("State values must all be finite.")

    x_m, y_m, vx_m_s, vy_m_s = values
    radius_m = math.hypot(x_m, y_m)
    if radius_m <= 0:
        raise ValueError("Position radius must be greater than zero.")

    acceleration_scale = -EARTH_MU / (radius_m**3)
    ax_m_s2 = acceleration_scale * x_m
    ay_m_s2 = acceleration_scale * y_m

    return (vx_m_s, vy_m_s, ax_m_s2, ay_m_s2)
