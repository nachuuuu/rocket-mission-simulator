
"""Plot spacecraft trajectories and orbital metrics."""

from pathlib import Path
from collections.abc import Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from rocket_sim.integrator import TimedState
from rocket_sim.trajectory import trajectory_rows


EARTH_RADIUS_M = 6_371_000.0
METRES_PER_KILOMETRE = 1_000.0


def create_trajectory_plots(
    trajectory: Sequence[TimedState],
    output_dir: str | Path = "results",
) -> tuple[Path, Path, Path]:
    """Generate orbit, altitude-time, and speed-time PNG plots."""
    rows = trajectory_rows(trajectory)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    times_s = [row["time_s"] for row in rows]
    x_km = [row["x_m"] / METRES_PER_KILOMETRE for row in rows]
    y_km = [row["y_m"] / METRES_PER_KILOMETRE for row in rows]
    altitudes_km = [
        row["altitude_m"] / METRES_PER_KILOMETRE for row in rows
    ]
    speeds_km_s = [
        row["speed_m_s"] / METRES_PER_KILOMETRE for row in rows
    ]

    orbit_file = output_path / "orbit_trajectory.png"
    altitude_file = output_path / "altitude_vs_time.png"
    speed_file = output_path / "speed_vs_time.png"

    # Plot 1: Orbital path and Earth.
    figure, axis = plt.subplots(figsize=(8, 8))

    earth_radius_km = EARTH_RADIUS_M / METRES_PER_KILOMETRE
    earth = Circle(
        (0.0, 0.0),
        earth_radius_km,
        color="steelblue",
        alpha=0.65,
        label="Earth",
    )
    axis.add_patch(earth)
    axis.plot(x_km, y_km, label="Spacecraft trajectory", linewidth=1.8)
    axis.scatter(x_km[0], y_km[0], marker="o", label="Start", zorder=3)
    axis.scatter(x_km[-1], y_km[-1], marker="x", label="End", zorder=3)

    extent_km = max(
        earth_radius_km * 1.1,
        max(abs(value) for value in x_km) * 1.1,
        max(abs(value) for value in y_km) * 1.1,
    )
    axis.set_xlim(-extent_km, extent_km)
    axis.set_ylim(-extent_km, extent_km)
    axis.set_aspect("equal", adjustable="box")
    axis.set_title("Spacecraft Orbit")
    axis.set_xlabel("X position (km)")
    axis.set_ylabel("Y position (km)")
    axis.grid(True, alpha=0.3)
    axis.legend()
    figure.tight_layout()
    figure.savefig(orbit_file, dpi=160)
    plt.close(figure)

    # Plot 2: Altitude over simulation time.
    figure, axis = plt.subplots(figsize=(10, 5))
    axis.plot(times_s, altitudes_km, linewidth=1.8)
    axis.set_title("Altitude vs. Time")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Altitude above Earth (km)")
    axis.grid(True, alpha=0.3)
    figure.tight_layout()
    figure.savefig(altitude_file, dpi=160)
    plt.close(figure)

    # Plot 3: Speed over simulation time.
    figure, axis = plt.subplots(figsize=(10, 5))
    axis.plot(times_s, speeds_km_s, linewidth=1.8)
    axis.set_title("Spacecraft Speed vs. Time")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Speed (km/s)")
    axis.grid(True, alpha=0.3)
    figure.tight_layout()
    figure.savefig(speed_file, dpi=160)
    plt.close(figure)

    return orbit_file, altitude_file, speed_file
