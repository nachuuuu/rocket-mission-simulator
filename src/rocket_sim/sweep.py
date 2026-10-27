
"""Parameter sweeps for orbital insertion scenarios."""

import math
from collections.abc import Iterable

from rocket_sim.classification import classify_initial_state
from rocket_sim.orbit import EARTH_RADIUS


def sweep_insertion_conditions(
    speeds_m_s: Iterable[float],
    flight_path_angles_deg: Iterable[float],
    *,
    altitude_m: float = 400_000.0,
    energy_tolerance_j_kg: float = 1e-6,
) -> tuple[dict[str, float | str | bool], ...]:
    """Classify combinations of insertion speed and flight-path angle.

    Flight-path angle is measured from the local horizontal:
    negative = descending, zero = tangential, positive = ascending.

    The initial position is on the positive x-axis. The initial velocity
    components are derived from the insertion speed and flight-path angle.
    """
    try:
        speeds = tuple(float(value) for value in speeds_m_s)
        angles = tuple(float(value) for value in flight_path_angles_deg)
        altitude = float(altitude_m)
        tolerance = float(energy_tolerance_j_kg)
    except (TypeError, ValueError) as exc:
        raise TypeError("Sweep parameters must be numeric.") from exc

    if not speeds or not angles:
        raise ValueError(
            "Speeds and angles must each contain at least one value."
        )

    if not all(math.isfinite(value) and value > 0 for value in speeds):
        raise ValueError("Speeds must be finite and positive.")

    if not all(
        math.isfinite(value) and -90 <= value <= 90
        for value in angles
    ):
        raise ValueError(
            "Angles must be finite and between -90 and 90 degrees."
        )

    if not math.isfinite(altitude) or altitude < 0:
        raise ValueError("Altitude must be finite and non-negative.")

    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError(
            "Energy tolerance must be finite and non-negative."
        )

    radius_m = EARTH_RADIUS + altitude
    results: list[dict[str, float | str | bool]] = []

    for speed_m_s in speeds:
        for angle_deg in angles:
            angle_rad = math.radians(angle_deg)

            radial_speed_m_s = speed_m_s * math.sin(angle_rad)
            tangential_speed_m_s = speed_m_s * math.cos(angle_rad)

            state = (
                radius_m,
                0.0,
                radial_speed_m_s,
                tangential_speed_m_s,
            )

            classification = classify_initial_state(
                state,
                energy_tolerance_j_kg=tolerance,
            )

            results.append(
                {
                    "altitude_m": altitude,
                    "insertion_speed_m_s": speed_m_s,
                    "flight_path_angle_deg": angle_deg,
                    **classification,
                }
            )

    return tuple(results)
