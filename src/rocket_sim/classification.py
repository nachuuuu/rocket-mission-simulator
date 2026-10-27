							
"""Analytical classification of two-dimensional orbital initial conditions."""

import math
from collections.abc import Sequence

from rocket_sim.orbit import EARTH_MU, EARTH_RADIUS

EARTH_INTERSECTING = "earth-intersecting"
BOUND = "bound"
ESCAPING = "escaping"


def classify_initial_state(
    state: Sequence[float],
    energy_tolerance_j_kg: float = 1e-6,
) -> dict[str, float | str | bool]:
    """Classify an orbital state using specific energy and periapsis.

    State convention: [x_m, y_m, vx_m_s, vy_m_s].

    This analytical classifier assumes a point-mass Earth and vacuum.
    """
    try:
        values = tuple(float(value) for value in state)
        tolerance = float(energy_tolerance_j_kg)
    except (TypeError, ValueError) as exc:
        raise TypeError("State and tolerance must be numeric.") from exc

    if len(values) != 4:
        raise ValueError("State must contain exactly four values.")

    if not all(math.isfinite(value) for value in values):
        raise ValueError("State values must all be finite.")

    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("Energy tolerance must be finite and non-negative.")

    x_m, y_m, vx_m_s, vy_m_s = values
    radius_m = math.hypot(x_m, y_m)

    if radius_m <= 0:
        raise ValueError("Position radius must be greater than zero.")

    speed_squared = vx_m_s**2 + vy_m_s**2
    radial_velocity_m_s = (
        x_m * vx_m_s + y_m * vy_m_s
    ) / radius_m

    energy = speed_squared / 2.0 - EARTH_MU / radius_m
    angular_momentum = x_m * vy_m_s - y_m * vx_m_s
    h_squared = angular_momentum**2

    eccentricity_squared = (
        1.0 + 2.0 * energy * h_squared / EARTH_MU**2
    )
    eccentricity = math.sqrt(max(0.0, eccentricity_squared))

    periapsis_m = h_squared / (
        EARTH_MU * (1.0 + eccentricity)
    )

    if radius_m <= EARTH_RADIUS:
        classification = EARTH_INTERSECTING
    elif energy < -tolerance:
        classification = (
            EARTH_INTERSECTING
            if periapsis_m <= EARTH_RADIUS
            else BOUND
        )
    elif energy > tolerance:
        classification = (
            EARTH_INTERSECTING
            if periapsis_m <= EARTH_RADIUS
            and radial_velocity_m_s < 0
            else ESCAPING
        )
    else:
        # Treat near-zero energy as parabolic/unbound.
        classification = (
            EARTH_INTERSECTING
            if periapsis_m <= EARTH_RADIUS
            and radial_velocity_m_s < 0
            else ESCAPING
        )

    return {
        "classification": classification,
        "radius_m": radius_m,
        "speed_m_s": math.sqrt(speed_squared),
        "radial_velocity_m_s": radial_velocity_m_s,
        "specific_energy_j_kg": energy,
        "angular_momentum_m2_s": angular_momentum,
        "eccentricity": eccentricity,
        "periapsis_m": periapsis_m,
        "periapsis_altitude_m": periapsis_m - EARTH_RADIUS,
        "earth_intersecting": classification == EARTH_INTERSECTING,
    }
