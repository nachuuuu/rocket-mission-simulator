"""Run a reproducible RK4 circular-orbit convergence experiment."""

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from rocket_sim.integrator import propagate_timed
from rocket_sim.orbit import (
    EARTH_MU,
    EARTH_RADIUS,
    circular_orbital_velocity,
    orbital_period,
)

ALTITUDE_M = 400_000.0
DURATION_S = 5_600.0
STEP_SIZES = (40.0, 20.0, 10.0, 5.0)


def circular_orbit_error(step_s: float) -> float:
    """Return final-position error in metres for one RK4 step size."""
    radius_m = EARTH_RADIUS + ALTITUDE_M
    speed_m_s = circular_orbital_velocity(radius_m)

    initial_state = (radius_m, 0.0, 0.0, speed_m_s)
    trajectory = propagate_timed(
        initial_state,
        duration_s=DURATION_S,
        step_s=step_s,
    )
    final_state = trajectory[-1][1]

    angle_rad = speed_m_s / radius_m * DURATION_S
    exact_x_m = radius_m * math.cos(angle_rad)
    exact_y_m = radius_m * math.sin(angle_rad)

    return math.hypot(
        final_state[0] - exact_x_m,
        final_state[1] - exact_y_m,
    )


def main() -> None:
    """Write convergence metrics to CSV and a log-log PNG plot."""
    output_dir = Path("results")
    plot_dir = output_dir / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    previous_error = None

    for step_s in STEP_SIZES:
        error_m = circular_orbit_error(step_s)
        ratio = (
            previous_error / error_m
            if previous_error is not None and error_m > 0
            else None
        )
        rows.append(
            {
                "step_s": step_s,
                "duration_s": DURATION_S,
                "final_position_error_m": error_m,
                "error_reduction_ratio": ratio,
            }
        )
        previous_error = error_m

    csv_path = output_dir / "convergence_report.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    plot_path = plot_dir / "convergence_error.png"
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.loglog(
        [row["step_s"] for row in rows],
        [row["final_position_error_m"] for row in rows],
        marker="o",
        label="RK4 final-position error",
    )
    axis.set_title("RK4 Circular-Orbit Convergence")
    axis.set_xlabel("Integration step size (s)")
    axis.set_ylabel("Final-position error (m)")
    axis.grid(True, which="both", alpha=0.3)
    axis.legend()
    figure.tight_layout()
    figure.savefig(plot_path, dpi=160)
    plt.close(figure)

    print(f"Orbital period: {orbital_period(EARTH_RADIUS + ALTITUDE_M):.3f} s")
    print(f"Duration: {DURATION_S:.1f} s")
    print(f"CSV report: {csv_path.resolve()}")
    print(f"Convergence plot: {plot_path.resolve()}")
    print()
    print("Step (s) | Final position error (m) | Error reduction ratio")
    for row in rows:
        ratio = row["error_reduction_ratio"]
        ratio_text = f"{ratio:.4f}" if ratio is not None else "-"
        print(
            f'{row["step_s"]:8.1f} | '
            f'{row["final_position_error_m"]:24.12g} | {ratio_text}'
        )


if __name__ == "__main__":
    main()
