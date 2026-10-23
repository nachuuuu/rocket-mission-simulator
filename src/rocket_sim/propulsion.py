"""Ideal rocket propulsion calculations."""

import math


def thrust_newtons(
    mass_flow_rate_kg_s: float,
    exhaust_velocity_m_s: float,
) -> float:
    """Calculate ideal thrust in newtons.

    Args:
        mass_flow_rate_kg_s: Propellant mass flow rate in kg/s.
        exhaust_velocity_m_s: Effective exhaust velocity in m/s.

    Returns:
        Thrust in newtons (N).

    Raises:
        ValueError: If an input is negative or non-finite.
    """
    if not math.isfinite(mass_flow_rate_kg_s) or mass_flow_rate_kg_s < 0:
        raise ValueError("Mass flow rate must be finite and non-negative.")

    if not math.isfinite(exhaust_velocity_m_s) or exhaust_velocity_m_s < 0:
        raise ValueError("Exhaust velocity must be finite and non-negative.")

    return mass_flow_rate_kg_s * exhaust_velocity_m_s