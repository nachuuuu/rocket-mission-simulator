
"""Generate demonstration orbit plots for the simulator."""

import math
from pathlib import Path

from rocket_sim.integrator import propagate_timed
from rocket_sim.visualization import create_trajectory_plots


def main() -> None:
    earth_radius_m = 6_371_000.0
    gravitational_parameter = 3.986004418e14
    orbital_altitude_m = 400_000.0
    orbital_radius_m = earth_radius_m + orbital_altitude_m

    circular_speed_m_s = math.sqrt(
        gravitational_parameter / orbital_radius_m
    )

    initial_state = (
        orbital_radius_m,
        0.0,
        0.0,
        circular_speed_m_s,
    )

    # Simulate 90 minutes using 10-second integration steps.
    trajectory = propagate_timed(
        initial_state=initial_state,
        duration_s=5_400.0,
        step_s=10.0,
    )

    output_dir = Path("results") / "plots"
    output_files = create_trajectory_plots(
        trajectory,
        output_dir=output_dir,
    )

    print(f"Simulation states: {len(trajectory)}")
    print(f"Simulation duration: {trajectory[-1][0]:.1f} seconds")
    print(f"Plots saved to: {output_dir.resolve()}")

    for path in output_files:
        print(f"Created: {path} ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
