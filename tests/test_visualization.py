
"""Tests for spacecraft trajectory visualizations."""

import math

import pytest

from rocket_sim.integrator import propagate_timed
from rocket_sim.visualization import create_trajectory_plots


def make_circular_orbit():
    """Create a short, physically plausible circular-orbit trajectory."""
    earth_radius_m = 6_371_000.0
    orbital_radius_m = earth_radius_m + 400_000.0
    gravitational_parameter = 3.986004418e14

    circular_speed_m_s = math.sqrt(
        gravitational_parameter / orbital_radius_m
    )

    initial_state = (
        orbital_radius_m,
        0.0,
        0.0,
        circular_speed_m_s,
    )

    return propagate_timed(
        initial_state=initial_state,
        duration_s=120.0,
        step_s=10.0,
    )


def test_create_trajectory_plots_generates_three_png_files(tmp_path):
    trajectory = make_circular_orbit()

    output_files = create_trajectory_plots(
        trajectory,
        output_dir=tmp_path,
    )

    assert len(output_files) == 3

    expected_names = {
        "orbit_trajectory.png",
        "altitude_vs_time.png",
        "speed_vs_time.png",
    }

    assert {path.name for path in output_files} == expected_names

    for path in output_files:
        assert path.is_file()
        assert path.stat().st_size > 0


def test_create_trajectory_plots_creates_missing_directory(tmp_path):
    output_dir = tmp_path / "new_results" / "plots"

    output_files = create_trajectory_plots(
        make_circular_orbit(),
        output_dir=output_dir,
    )

    assert output_dir.is_dir()
    assert all(path.exists() for path in output_files)


def test_create_trajectory_plots_rejects_empty_trajectory(tmp_path):
    with pytest.raises(ValueError, match="at least one state"):
        create_trajectory_plots([], output_dir=tmp_path)


def test_create_trajectory_plots_rejects_invalid_state(tmp_path):
    trajectory = (
        (0.0, (7_000_000.0, 0.0, 0.0, 7_500.0)),
        (1.0, (float("nan"), 0.0, 0.0, 7_500.0)),
    )

    with pytest.raises(ValueError, match="finite"):
        create_trajectory_plots(trajectory, output_dir=tmp_path)
