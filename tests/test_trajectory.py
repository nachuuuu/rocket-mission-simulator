
import csv
import math

import pytest

from rocket_sim.integrator import propagate_timed
from rocket_sim.orbit import EARTH_RADIUS, circular_orbital_velocity
from rocket_sim.trajectory import (
    CSV_COLUMNS,
    export_trajectory_csv,
    trajectory_rows,
)


def make_trajectory(duration_s=20, step_s=10):
    radius_m = EARTH_RADIUS + 400_000
    speed_m_s = circular_orbital_velocity(radius_m)
    initial = (radius_m, 0.0, 0.0, speed_m_s)

    return propagate_timed(initial, duration_s, step_s)


def test_timed_propagation_includes_initial_and_final_timestamps():
    trajectory = make_trajectory()

    assert [time for time, _ in trajectory] == [0.0, 10.0, 20.0]


def test_timed_propagation_handles_partial_final_step():
    trajectory = make_trajectory(duration_s=25, step_s=10)

    assert [time for time, _ in trajectory] == [0.0, 10.0, 20.0, 25.0]


def test_zero_duration_has_one_timed_state():
    trajectory = make_trajectory(duration_s=0)

    assert len(trajectory) == 1
    assert trajectory[0][0] == 0.0


def test_trajectory_rows_calculate_radius_altitude_and_speed():
    radius_m = EARTH_RADIUS + 400_000
    speed_m_s = circular_orbital_velocity(radius_m)
    trajectory = ((0.0, (radius_m, 0.0, 0.0, speed_m_s)),)

    row = trajectory_rows(trajectory)[0]

    assert row["radius_m"] == pytest.approx(radius_m)
    assert row["altitude_m"] == pytest.approx(400_000)
    assert row["speed_m_s"] == pytest.approx(speed_m_s)


def test_csv_export_has_expected_columns_and_rows(tmp_path):
    trajectory = make_trajectory()
    output_path = tmp_path / "results" / "orbit.csv"

    returned_path = export_trajectory_csv(trajectory, output_path)

    assert returned_path == output_path
    assert output_path.exists()

    with output_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    assert tuple(reader.fieldnames) == CSV_COLUMNS
    assert len(rows) == len(trajectory)
    assert float(rows[0]["time_s"]) == 0.0
    assert float(rows[-1]["time_s"]) == 20.0


def test_csv_export_contains_finite_numeric_values(tmp_path):
    output_path = tmp_path / "orbit.csv"

    export_trajectory_csv(make_trajectory(), output_path)

    with output_path.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    for row in rows:
        assert all(math.isfinite(float(value)) for value in row.values())


@pytest.mark.parametrize(
    "trajectory",
    [
        (),
        ((-1.0, (7_000_000, 0, 0, 7_500)),),
        ((0.0, (7_000_000, 0, 0, 7_500)),
         (0.0, (7_000_000, 0, 0, 7_500))),
        ((0.0, (0, 0, 0, 0)),),
        ((0.0, (math.nan, 0, 0, 7_500)),),
        ((math.inf, (7_000_000, 0, 0, 7_500)),),
    ],
)
def test_trajectory_rows_reject_invalid_data(trajectory):
    with pytest.raises(ValueError):
        trajectory_rows(trajectory)


def test_export_rejects_a_directory_as_output_path(tmp_path):
    with pytest.raises(ValueError):
        export_trajectory_csv(make_trajectory(), tmp_path)


def test_trajectory_rows_reject_non_numeric_state():
    with pytest.raises(TypeError):
        trajectory_rows(((0.0, ("invalid", 0, 0, 0)),))
