"""Tests for the RK4 convergence experiment."""

import csv

import pytest

from scripts.convergence_analysis import (
    DURATION_S,
    STEP_SIZES,
    circular_orbit_error,
    main,
)


def test_smaller_steps_reduce_position_error():
    errors = [
        circular_orbit_error(step_s)
        for step_s in STEP_SIZES
    ]

    assert all(error > 0 for error in errors)
    assert all(
        finer < coarser
        for coarser, finer in zip(errors, errors[1:])
    )


def test_error_reduction_is_consistent_with_rk4_order():
    errors = [
        circular_orbit_error(step_s)
        for step_s in STEP_SIZES
    ]

    ratios = [
        coarse / fine
        for coarse, fine in zip(errors, errors[1:])
    ]

    # Empirical bounds for this fixed circular-orbit experiment.
    assert all(14.0 < ratio < 19.0 for ratio in ratios)


def test_convergence_report_and_plot_are_generated(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    main()

    csv_path = tmp_path / "results" / "convergence_report.csv"
    plot_path = (
        tmp_path / "results" / "plots" / "convergence_error.png"
    )

    assert csv_path.is_file()
    assert plot_path.is_file()
    assert plot_path.stat().st_size > 0

    with csv_path.open(
        newline="",
        encoding="utf-8",
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == len(STEP_SIZES)
    assert [
        float(row["step_s"]) for row in rows
    ] == list(STEP_SIZES)

    assert all(
        float(row["duration_s"]) == DURATION_S
        for row in rows
    )

    assert all(
        float(row["final_position_error_m"]) > 0
        for row in rows
    )

    assert rows[0]["error_reduction_ratio"] == ""
    assert all(
        float(row["error_reduction_ratio"]) > 1
        for row in rows[1:]
    )
