
"""Basic orbital mechanics calculations."""

import math

EARTH_MU = 3.986004418e14  # Earth's gravitational parameter, m^3/s^2
EARTH_RADIUS = 6_371_000.0  # Mean Earth radius, metres


def gravitational_acceleration(radius_m: float) -> float:
    """Return gravitational acceleration magnitude in m/s^2."""
    _validate_radius(radius_m)
    return EARTH_MU / radius_m**2


def circular_orbital_velocity(radius_m: float) -> float:
    """Return circular orbital speed in m/s."""
    _validate_radius(radius_m)
    return math.sqrt(EARTH_MU / radius_m)


def orbital_period(radius_m: float) -> float:
    """Return circular orbital period in seconds."""
    _validate_radius(radius_m)
    return 2 * math.pi * math.sqrt(radius_m**3 / EARTH_MU)


def _validate_radius(radius_m: float) -> None:
    if not math.isfinite(radius_m) or radius_m <= 0:
        raise ValueError("Radius must be finite and greater than zero.")
