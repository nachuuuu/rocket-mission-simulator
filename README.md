# Rocket Mission & Orbit Simulator

An educational Python project connecting ideal rocket-propulsion calculations with simplified two-dimensional orbital trajectories around Earth.

**Current status:** M0–M4 implementation is present. The project includes ideal propulsion and staging calculations, analytical orbital references, two-dimensional central-gravity dynamics, numerical integration, trajectory visualization, and analytical initial-condition classification with parameter sweeps. M5 convergence analysis and M6 release review remain on the roadmap.

## Project goals

- Calculate ideal propulsion quantities: thrust, thrust-to-weight ratio, ideal delta-v, and ideal staging performance.
- Provide analytical orbital reference calculations for Earth's central-gravity model.
- Integrate simplified two-dimensional point-mass trajectories.
- Explore insertion-speed and flight-path-angle scenarios.
- Classify initial orbital conditions as Earth-intersecting, bound, or escaping.
- Assess numerical integration accuracy through step-size convergence tests.
- Document assumptions, validation methods, and limitations.

## Current capabilities

### Propulsion and staging — M1

The `rocket_sim.propulsion` module provides:

- `thrust_newtons(mass_flow_rate_kg_s, exhaust_velocity_m_s)`
- `thrust_to_weight_ratio(thrust_n, mass_kg, gravity_m_s2=9.80665)`
- `ideal_delta_v(exhaust_velocity_m_s, initial_mass_kg, final_mass_kg)`

The `rocket_sim.staging` module provides ideal staged delta-v calculations using explicit stage and payload mass accounting.

These are ideal calculations. They exclude gravity losses, atmospheric drag, steering losses, and real engine constraints.

### Orbital references — M2

The `rocket_sim.orbit` module provides:

- `gravitational_acceleration(radius_m)`
- `circular_orbital_velocity(radius_m)`
- `orbital_period(radius_m)`

The model uses SI units, geocentric radius in metres, and Earth's configured gravitational parameter and mean radius.

### Dynamics and integration — M3

The dynamics layer represents two-dimensional point-mass motion under Earth's central inverse-square gravity. The state convention is:

`[x_m, y_m, vx_m_s, vy_m_s]`

The state derivative returns position rates and acceleration components. Numerical integration and trajectory propagation are implemented separately from the physical equations, and the project includes tests for dynamics, integration, trajectories, and orbital conservation.

### Scenario classification and sweeps — M4

The `rocket_sim.classification` module classifies an initial state using specific orbital energy, angular momentum, eccentricity, periapsis, and the configured Earth radius.

The supported labels are:

- `earth-intersecting`
- `bound`
- `escaping`

The `rocket_sim.sweep` module evaluates combinations of insertion speed and flight-path angle. The script `scripts/scenario_sweep.py` writes results to `results/scenario_sweep.csv`.

The included sweep evaluates 247 combinations at an altitude of 400 km, with speeds from 6,500 to 11,000 m/s in 250 m/s increments and flight-path angles from −30° to +30° in 5° increments.

The classifier is an analytical initial-condition assessment under a point-mass Earth and vacuum model. It is not a powered-flight simulation or a mission-feasibility assessment.

### Visualization

The visualization module generates trajectory plots. The existing plot-generation workflow is separate from the analytical scenario sweep.

### Remaining milestones

- **M5 — Plots and convergence:** compare multiple integration step sizes and document numerical convergence.
- **M6 — Documentation and release:** complete setup instructions, review assumptions, run the full test suite, inspect the final Git diff, and create a release checkpoint.

## Model scope and limitations

The initial model uses a spherical Earth, a central inverse-square gravity field, ideal propulsion equations, and two-dimensional point-mass trajectories.

It does not model atmospheric drag, powered ascent, guidance and control, Earth oblateness, or multi-body perturbations. Analytical classifications and numerical results must not be treated as flight-dynamics certification or used for real-world launch decisions.

See [Model Assumptions](docs/model-assumptions.md), [Software Architecture](docs/architecture.md), [Validation Strategy](docs/validation.md), and [Development Roadmap](docs/roadmap.md).

## Requirements

- Python 3.11 or newer
- NumPy
- Matplotlib
- pytest for development and tests

## Setup on Windows PowerShell

From the project directory:

```powershell
Set-Location "D:\rocket-mission-simulator"
py -3.11 -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -e ".[dev]"
```

If the virtual environment already exists, do not recreate it; install or update dependencies with the final command above.

## Run tests

```powershell
& ".\.venv\Scripts\python.exe" -m pytest
```

## Generate the scenario sweep

```powershell
& ".\.venv\Scripts\python.exe" scripts\scenario_sweep.py
```

The CSV output is written to `results\scenario_sweep.csv`.

## Repository layout

```text
rocket-mission-simulator/
├── docs/
├── results/
├── scripts/
├── src/rocket_sim/
├── tests/
├── .gitignore
└── pyproject.toml
```

## Safety and intended use

This is an educational numerical simulator, not a flight-dynamics certification package, launch-vehicle design tool, or launch-planning system. Results depend on the stated assumptions and must not be used for real-world mission decisions.

## License

No license has been added yet. Unless and until a license is included, reuse and redistribution are not granted by this repository.
