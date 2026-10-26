
"""Trajectory analysis and CSV export utilities."""

import csv
import math
from collections.abc import Sequence
from pathlib import Path

from rocket_sim.integrator import TimedState


CSV_COLUMNS = (
    "time_s",
    "x_m",
    "y_m",
    "vx_m_s",
    "vy_m_s",
    "radius_m",
    "altitude_m",
    "speed_m_s",
)


def trajectory_rows(
    trajectory: Sequence[TimedState],
) -> tuple[dict[str, float], ...]:
    """Convert timed orbital states into validated, unit-labelled rows."""
    rows: list[dict[str, float]] = []
    previous_time_s = -1.0

    for time_s, state in trajectory:
        try:
            time_s = float(time_s)
            values = tuple(float(value) for value in state)
        except (TypeError, ValueError) as exc:
            raise TypeError(
                "Trajectory times and state values must be numeric."
            ) from exc

        if not math.isfinite(time_s) or time_s < 0:
            raise ValueError("Trajectory times must be finite and non-negative.")

        if time_s <= previous_time_s:
            raise ValueError("Trajectory times must be strictly increasing.")

        if len(values) != 4:
            raise ValueError("Each state must contain exactly four values.")

        if not all(math.isfinite(value) for value in values):
            raise ValueError("Trajectory state values must all be finite.")

        x_m, y_m, vx_m_s, vy_m_s = values
        radius_m = math.hypot(x_m, y_m)

        if radius_m <= 0:
            raise ValueError("Spacecraft radius must be greater than zero.")

        speed_m_s = math.hypot(vx_m_s, vy_m_s)

        rows.append(
            {
                "time_s": time_s,
                "x_m": x_m,
                "y_m": y_m,
                "vx_m_s": vx_m_s,
                "vy_m_s": vy_m_s,
                "radius_m": radius_m,
                "altitude_m": radius_m - 6_371_000.0,
                "speed_m_s": speed_m_s,
            }
        )

        previous_time_s = time_s

    if not rows:
        raise ValueError("Trajectory must contain at least one state.")

    return tuple(rows)


def export_trajectory_csv(
    trajectory: Sequence[TimedState],
    output_path: str | Path,
) -> Path:
    """Write a timed trajectory to CSV and return the output path."""
    rows = trajectory_rows(trajectory)
    path = Path(output_path)

    if path.exists() and path.is_dir():
        raise ValueError("Output path must identify a file, not a directory.")

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    return path
