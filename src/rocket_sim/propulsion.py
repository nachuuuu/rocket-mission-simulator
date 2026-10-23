
"""Rocket propulsion calculations."""

import math


STANDARD_GRAVITY_M_S2 = 9.80665


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


def thrust_to_weight_ratio(
    thrust_n: float,
    mass_kg: float,
    gravity_m_s2: float = STANDARD_GRAVITY_M_S2,
) -> float:
    """Calculate thrust-to-weight ratio (dimensionless).

    Args:
        thrust_n: Engine thrust in newtons.
        mass_kg: Total vehicle mass in kilograms.
        gravity_m_s2: Local gravitational acceleration in m/s^2.

    Returns:
        Thrust divided by vehicle weight.

    Raises:
        ValueError: If inputs are non-finite, thrust is negative,
            or mass or gravity is not positive.
    """
    if not math.isfinite(thrust_n) or thrust_n < 0:
        raise ValueError("Thrust must be finite and non-negative.")

    if not math.isfinite(mass_kg) or mass_kg <= 0:
        raise ValueError("Mass must be finite and greater than zero.")

    if not math.isfinite(gravity_m_s2) or gravity_m_s2 <= 0:
        raise ValueError("Gravity must be finite and greater than zero.")

    return thrust_n / (mass_kg * gravity_m_s2)


def ideal_delta_v(
    exhaust_velocity_m_s: float,
    initial_mass_kg: float,
    final_mass_kg: float,
) -> float:
    """Calculate ideal delta-v using the Tsiolkovsky rocket equation.

    Args:
        exhaust_velocity_m_s: Effective exhaust velocity in m/s.
        initial_mass_kg: Vehicle mass before propellant is consumed, in kg.
        final_mass_kg: Vehicle mass after propellant is consumed, in kg.

    Returns:
        Ideal change in velocity in m/s.

    Raises:
        ValueError: If inputs are non-finite, masses are not positive,
            exhaust velocity is negative, or final mass exceeds initial mass.
    """
    if not math.isfinite(exhaust_velocity_m_s) or exhaust_velocity_m_s < 0:
        raise ValueError("Exhaust velocity must be finite and non-negative.")

    if not math.isfinite(initial_mass_kg) or initial_mass_kg <= 0:
        raise ValueError("Initial mass must be finite and greater than zero.")

    if not math.isfinite(final_mass_kg) or final_mass_kg <= 0:
        raise ValueError("Final mass must be finite and greater than zero.")

    if final_mass_kg > initial_mass_kg:
        raise ValueError("Final mass cannot exceed initial mass.")

    return exhaust_velocity_m_s * math.log(initial_mass_kg / final_mass_kg)
