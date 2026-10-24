"""Ideal multistage rocket performance calculations."""

from dataclasses import dataclass
import math
from collections.abc import Sequence


@dataclass(frozen=True)
class RocketStage:
    """An ideal rocket stage, with masses expressed in kilograms.

    Stages must be supplied from the bottom stage to the top stage.
    """

    dry_mass_kg: float
    propellant_mass_kg: float
    exhaust_velocity_m_s: float

    def __post_init__(self) -> None:
        """Reject physically invalid stage parameters."""
        values = (
            ("Dry mass", self.dry_mass_kg),
            ("Propellant mass", self.propellant_mass_kg),
            ("Exhaust velocity", self.exhaust_velocity_m_s),
        )

        for name, value in values:
            if not math.isfinite(value) or value <= 0:
                raise ValueError(
                    f"{name} must be finite and greater than zero."
                )


def ideal_staged_delta_v(
    stages: Sequence[RocketStage],
    payload_mass_kg: float,
) -> float:
    """Calculate total ideal delta-v for a multistage rocket.

    Args:
        stages: Rocket stages ordered bottom-to-top.
        payload_mass_kg: Payload mass remaining after all stages are spent,
            in kilograms. Zero is allowed.

    Returns:
        Sum of the ideal velocity increments of all stages, in m/s.

    Assumptions:
        - Each stage burns all its propellant before separation.
        - The spent stage's dry mass is discarded before the next stage burns.
        - Exhaust velocity is constant during each stage's burn.
        - Gravity losses, aerodynamic drag, steering losses, and engine limits
          are ignored.

    Raises:
        ValueError: If the stage list is empty or the payload mass is invalid.
        TypeError: If an item is not a RocketStage.
    """
    if not math.isfinite(payload_mass_kg) or payload_mass_kg < 0:
        raise ValueError("Payload mass must be finite and non-negative.")

    if not stages:
        raise ValueError("At least one rocket stage is required.")

    for stage in stages:
        if not isinstance(stage, RocketStage):
            raise TypeError("Every item must be a RocketStage.")

    delta_v_values = []

    for index, stage in enumerate(stages):
        # At ignition, this stage carries its own mass and every upper stage.
        carried_stages = stages[index:]

        initial_mass_kg = payload_mass_kg + math.fsum(
            item.dry_mass_kg + item.propellant_mass_kg
            for item in carried_stages
        )

        # At burnout, this stage's propellant has been consumed, but its
        # dry structure is still attached until separation.
        final_mass_kg = initial_mass_kg - stage.propellant_mass_kg

        stage_delta_v = stage.exhaust_velocity_m_s * math.log(
            initial_mass_kg / final_mass_kg
        )
        delta_v_values.append(stage_delta_v)

    return math.fsum(delta_v_values)
