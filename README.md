# Rocket Mission & Orbit Simulator

An educational Python project connecting ideal rocket-propulsion calculations with simplified two-dimensional orbital trajectories around Earth.

**Status:** M1 ideal propulsion calculations and M2 analytical orbital references are implemented with tests. M3 has started: two-dimensional central-gravity state derivatives are implemented; numerical integration and circular-orbit propagation validation remain to be completed. Scenario classification, sweeps, and plotting are still planned.

## Project goals

- Calculate ideal propulsion quantities: thrust, thrust-to-weight ratio, ideal delta-v, and ideal staging performance.
- Provide analytical orbital reference calculations for Earth's central-gravity model.
- Integrate simplified two-dimensional point-mass trajectories.
- Explore insertion-speed and flight-path-angle scenarios.
- Assess numerical integration accuracy through step-size convergence tests.
- Document assumptions, validation methods, and limitations.

## Current capabilities

### Propulsion — M1

The `rocket_sim.propulsion` module provides:
- `thrust_newtons(mass_flow_rate_kg_s, exhaust_velocity_m_s)`
- `thrust_to_weight_ratio(thrust_n, mass_kg, gravity_m_s2=9.80665)`
- `ideal_delta_v(exhaust_velocity_m_s, initial_mass_kg, final_mass_kg)`

The `rocket_sim.staging` module provides:
- `RocketStage(dry_mass_kg, propellant_mass_kg, exhaust_velocity_m_s)`
- `ideal_staged_delta_v(stages, payload_mass_kg)`

These are ideal calculations. They exclude gravity losses, atmospheric drag, steering losses, and real engine constraints.

### Orbital references — M2

The `rocket_sim.orbit` module provides:
- `gravitational_acceleration(radius_m)`: gravity magnitude under the inverse-square central-gravity model.
- `circular_orbital_velocity(radius_m)`: circular-orbit speed.
- `orbital_period(radius_m)`: circular-orbit period.

Functions use SI units, a geocentric radius in metres, and reject non-finite or non-positive radii.

### Dynamics — M3 in progress

The `rocket_sim.dynamics.state_derivative(state)` function accepts `[x_m, y_m, vx_m_s, vy_m_s]` and returns `[vx_m_s, vy_m_s, ax_m_s2, ay_m_s2]` for central gravity. Numerical integration and full trajectory propagation are the next implementation tasks.

## Model scope

The initial model uses a spherical Earth, a central inverse-square gravity field, ideal propulsion equations, and intended two-dimensional point-mass trajectories. It does not represent all physical or engineering effects of a real launch.

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

To run the current orbital references from PowerShell:

```powershell
& "D:\rocket-mission-simulator\.venv\Scripts\python.exe" -c "from rocket_sim.orbit import EARTH_RADIUS, circular_orbital_velocity, orbital_period; r = EARTH_RADIUS + 400_000; print(f'Circular speed: {circular_orbital_velocity(r):.1f} m/s'); print(f'Period: {orbital_period(r) / 60:.2f} minutes')"
```

Expected values are approximately 7,673 m/s and 92.4 minutes at 400 km altitude.

## Repository layout

```text
rocket-mission-simulator/
├── docs/
├── src/rocket_sim/
│   ├── __init__.py
│   ├── orbit.py
│   ├── propulsion.py
│   ├── staging.py
│   └── dynamics.py
├── tests/
│   ├── test_orbit.py
│   ├── test_propulsion.py
│   ├── test_staging.py
│   └── test_dynamics.py
├── .gitignore
└── pyproject.toml
```

## Development roadmap

1. **M0 — Environment and repository:** established.
2. **M1 — Propulsion:** thrust, thrust-to-weight ratio, Tsiolkovsky ideal rocket equation, ideal staging, and tests implemented.
3. **M2 — Orbital equations:** analytical gravity and circular-orbit calculations implemented and tested.
4. **M3 — Dynamics and integration:** state derivatives implemented; numerical integration and propagated circular-orbit validation remain.
5. **M4 — Scenario sweeps:** vary insertion speed and flight-path angle; classify outcomes as Earth-intersecting, bound, or escaping.
6. **M5 — Plots and convergence:** labelled plots, multiple integration step sizes, and a convergence report.
7. **M6 — Documentation and release:** examples, full test suite, final review, and release checkpoint.

See [Roadmap](docs/roadmap.md) for scope and completion criteria.

## Safety and intended use

This is an educational numerical simulator, not a flight-dynamics certification package, launch-vehicle design tool, or launch-planning system. Results depend on the stated assumptions and must not be used for real-world mission decisions.

## License

No license has been added yet. Unless and until a license is included, reuse and redistribution are not granted by this repository.
