# Rocket Mission & Orbit Simulator

An educational Python project connecting ideal rocket-propulsion calculations with simplified two-dimensional orbital trajectories around Earth.

**Status:** Early development. The repository currently contains basic analytical orbital-mechanics functions and their tests. Propulsion calculations, numerical trajectory integration, scenario classification, and plotting are planned milestones—not yet implemented.

## Project goals

- Calculate ideal propulsion quantities, including thrust, thrust-to-weight ratio, ideal delta-v, and ideal staging performance.
- Provide analytical orbital reference calculations for Earth's central-gravity model.
- Integrate simplified two-dimensional point-mass trajectories.
- Explore insertion-speed and flight-path-angle scenarios.
- Assess numerical integration accuracy through step-size convergence tests.
- Document assumptions, validation methods, and limitations.

## Current capabilities

The `rocket_sim.orbit` module currently provides:

- `gravitational_acceleration(radius_m)`: magnitude of acceleration under the inverse-square central-gravity model.
- `circular_orbital_velocity(radius_m)`: circular-orbit speed.
- `orbital_period(radius_m)`: circular-orbit period.

All three functions accept a geocentric radius in metres and reject non-finite or non-positive radii with `ValueError`. The current tests include reference checks at 400 km altitude, monotonicity checks, and invalid-input cases.

## Model scope

The initial model uses a spherical Earth, a central inverse-square gravity field, and ideal propulsion equations. Orbital trajectories are intended to be two-dimensional point-mass motion. The model does not represent all physical or engineering effects of a real launch.

See [Model Assumptions](docs/model-assumptions.md) for constants, units, assumptions, and limitations.

## Requirements

- Python 3.11 or newer
- NumPy
- Matplotlib
- pytest for development and tests

## Setup on Windows PowerShell

From the project directory:

```powershell
cd D:\rocket-mission-simulator
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

If the virtual environment already exists, do not recreate it; install or update dependencies with:

```powershell
& "D:\rocket-mission-simulator\.venv\Scripts\python.exe" -m pip install -e "D:\rocket-mission-simulator[dev]"
```

## Run tests

```powershell
& "D:\rocket-mission-simulator\.venv\Scripts\python.exe" -m pytest
```

To run the current orbital calculations from PowerShell:

```powershell
& "D:\rocket-mission-simulator\.venv\Scripts\python.exe" -c "from rocket_sim.orbit import EARTH_RADIUS, circular_orbital_velocity, orbital_period; r = EARTH_RADIUS + 400_000; print(f'Circular speed: {circular_orbital_velocity(r):.1f} m/s'); print(f'Period: {orbital_period(r) / 60:.2f} minutes')"
```

Expected values are approximately 7,673 m/s and 92.4 minutes at 400 km altitude.

## Repository layout

```text
rocket-mission-simulator/
├── docs/
│   ├── model-assumptions.md
│   ├── architecture.md
│   ├── roadmap.md
│   ├── validation.md
│   └── development.md
├── src/
│   └── rocket_sim/
│       ├── __init__.py
│       └── orbit.py
├── tests/
│   └── test_orbit.py
├── .gitignore
└── pyproject.toml
```

The layout above describes the current files plus the documentation being added. New implementation modules will be introduced milestone by milestone.

## Development roadmap

1. **M0 — Environment and repository:** packaging, tests, repository setup, and model assumptions. Baseline established.
2. **M1 — Propulsion:** thrust, thrust-to-weight ratio, Tsiolkovsky ideal rocket equation, ideal staging, and tests.
3. **M2 — Orbital equations:** analytical gravity and circular-orbit calculations. Baseline implemented and tested.
4. **M3 — Dynamics and integration:** central-gravity state derivatives, numerical trajectory integration, and circular-orbit validation.
5. **M4 — Scenario sweeps:** vary insertion speed and flight-path angle; classify outcomes such as bound, escaping, and Earth-intersecting.
6. **M5 — Plots and convergence:** labelled plots, multiple integration step sizes, and a convergence report.
7. **M6 — Documentation and release:** examples, full test suite, final review, and release checkpoint.

See [Roadmap](docs/roadmap.md) for scope and completion criteria.

## Safety and intended use

This is an educational numerical simulator, not a flight-dynamics certification package, launch-vehicle design tool, or launch-planning system. Results depend on the stated assumptions and must not be used for real-world mission decisions.

## License

No license has been added yet. Unless and until a license is included, reuse and redistribution are not granted by this repository.
