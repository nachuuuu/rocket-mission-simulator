
"""Generate an orbital insertion scenario sweep as a CSV file."""

import csv
from pathlib import Path

from rocket_sim.sweep import sweep_insertion_conditions


def main() -> None:
    output_path = Path("results") / "scenario_sweep.csv"

    # 19 speeds: 6,500 to 11,000 m/s in 250 m/s increments.
    speeds_m_s = range(6_500, 11_001, 250)

    # 13 angles: -30 to +30 degrees in 5-degree increments.
    angles_deg = range(-30, 31, 5)

    results = sweep_insertion_conditions(
        speeds_m_s,
        angles_deg,
        altitude_m=400_000.0,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = list(results[0].keys())

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(results)

    counts: dict[str, int] = {}

    for result in results:
        label = str(result["classification"])
        counts[label] = counts.get(label, 0) + 1

    print(f"Scenarios evaluated: {len(results)}")
    print(f"CSV saved to: {output_path.resolve()}")
    print("Classification counts:")

    for label, count in sorted(counts.items()):
        print(f"  {label}: {count}")


if __name__ == "__main__":
    main()
