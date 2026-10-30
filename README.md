# Rocket Mission & Orbit Simulator

An educational Python project connecting ideal rocket propulsion calculations with numerical simulation of two-dimensional orbital trajectories around Earth.

**Project status:** M0–M5 implemented. M6 documentation and release preparation in progress.

The project explores the relationship between rocket performance, orbital mechanics, numerical integration, and orbital trajectory analysis. It combines analytical calculations with numerical methods to study idealized spacecraft motion.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Objectives](#project-objectives)
3. [Implemented Milestones](#implemented-milestones)
4. [System Architecture](#system-architecture)
5. [Technology Stack](#technology-stack)
6. [Repository Structure](#repository-structure)
7. [Installation](#installation)
8. [Running the Project](#running-the-project)
9. [Numerical Convergence Analysis](#numerical-convergence-analysis)
10. [Testing and Validation](#testing-and-validation)
11. [Physical Model and Assumptions](#physical-model-and-assumptions)
12. [Known Limitations](#known-limitations)
13. [Development Roadmap](#development-roadmap)
14. [License](#license)

---

## Project Overview

Rocket Mission & Orbit Simulator is a modular Python application designed to explore ideal rocket propulsion and simplified orbital mechanics.

The project is organized around two connected areas:

- **Rocket propulsion:** Ideal thrust, thrust-to-weight ratio, rocket delta-v, and multistage rocket performance.
- **Orbital mechanics:** Analytical orbital calculations, numerical trajectory propagation, visualization, orbital classification, and scenario analysis.

The orbital simulation represents spacecraft motion as a two-dimensional point mass moving under Earth's central inverse-square gravitational field.

The numerical integration layer uses the classical fourth-order Runge–Kutta method (RK4).

The project is intended for educational, computational, and analytical experimentation.

## Project Objectives

- Implement fundamental ideal rocket propulsion equations.
- Calculate ideal multistage rocket performance.
- Implement analytical orbital mechanics reference calculations.
- Simulate two-dimensional spacecraft motion under central gravity.
- Implement numerical integration using RK4.
- Export and visualize spacecraft trajectories.
- Classify orbital initial conditions.
- Evaluate multiple orbital insertion scenarios.
- Investigate numerical integration accuracy through convergence analysis.
- Establish reproducible tests and technical documentation.

---

## Implemented Milestones

### M0 — Environment and Repository

Established the Python project environment and repository structure.

Implemented:
- Python package using a `src/` layout.
- Virtual environment and dependency configuration.
- Git version control.
- Pytest-based testing structure.
- Initial technical documentation.

### M1 — Propulsion and Staging

Implemented ideal rocket propulsion calculations.

The `rocket_sim.propulsion` module provides:

| Function | Description |
|---|---|
| `thrust_newtons()` | Calculates thrust from mass flow rate and effective exhaust velocity |
| `thrust_to_weight_ratio()` | Calculates thrust relative to vehicle weight |
| `ideal_delta_v()` | Calculates ideal rocket delta-v using the Tsiolkovsky equation |

The `rocket_sim.staging` module implements ideal multistage rocket performance calculations.

Stage mass accounting explicitly considers:
- Propellant mass.
- Dry mass.
- Payload mass.
- Discarded stage mass.

These calculations use idealized assumptions and do not represent a complete powered ascent.

### M2 — Analytical Orbital Mechanics

Implemented analytical reference calculations in `rocket_sim.orbit`.

Available functions:

| Function | Description |
|---|---|
| `gravitational_acceleration()` | Gravitational acceleration magnitude at a given radius |
| `circular_orbital_velocity()` | Circular orbital velocity |
| `orbital_period()` | Circular orbital period |

The model uses:

- Earth's gravitational parameter: `3.986004418e14 m³/s²`
- Earth's mean radius: `6,371,000 m`

All calculations use SI units.

### M3 — Orbital Dynamics and Numerical Integration

Implemented two-dimensional spacecraft dynamics under Earth's central gravitational field.

The spacecraft state vector is:

```python
[x_m, y_m, vx_m_s, vy_m_s]
```

Where:

- `x_m`, `y_m`: Position coordinates in metres.
- `vx_m_s`, `vy_m_s`: Velocity components in metres per second.

The `rocket_sim.dynamics` module calculates state derivatives.

The `rocket_sim.integrator` module implements classical fourth-order Runge–Kutta integration.

Available propagation interfaces:

- `rk4_step()`
- `propagate()`
- `propagate_timed()`

The timed propagation interface records simulation timestamps and supports a shortened final integration step when the duration is not an exact multiple of the requested step size.

The project also includes:
- Circular-orbit reference tests.
- Orbital energy conservation tests.
- Angular momentum conservation tests.
- Integration convergence checks.

### M4 — Orbital Classification and Scenario Sweeps

Implemented analytical classification of orbital initial conditions.

The `rocket_sim.classification` module uses:

- Specific orbital energy.
- Specific angular momentum.
- Orbital eccentricity.
- Periapsis radius.
- Configured Earth radius.

Supported classifications:

| Classification | Meaning |
|---|---|
| `earth-intersecting` | The mathematically determined orbit intersects the configured Earth radius |
| `bound` | The initial condition corresponds to a bound orbit that does not intersect Earth |
| `escaping` | The initial condition corresponds to an unbound escaping trajectory |

The `rocket_sim.sweep` module evaluates combinations of orbital insertion speed and flight-path angle.

Default scenario sweep:

| Parameter | Value |
|---|---:|
| Orbital altitude | 400 km |
| Minimum insertion speed | 6,500 m/s |
| Maximum insertion speed | 11,000 m/s |
| Speed increment | 250 m/s |
| Minimum flight-path angle | -30° |
| Maximum flight-path angle | +30° |
| Angle increment | 5° |
| Total scenarios | 247 |

Run the sweep:

```powershell
python scripts/scenario_sweep.py
```

Output:

```text
results/scenario_sweep.csv
```

The classifier evaluates initial orbital conditions analytically. It does not simulate a complete launch or powered flight.

### M5 — Visualization and Numerical Convergence

Implemented trajectory visualization and a reproducible RK4 convergence experiment.

#### Trajectory visualization

The `rocket_sim.visualization` module generates three plots:

1. Orbital trajectory with Earth reference geometry.
2. Altitude versus simulation time.
3. Spacecraft speed versus simulation time.

Generate the plots:

```powershell
python scripts/generate_plots.py
```

Generated files:

```text
results/plots/orbit_trajectory.png
results/plots/altitude_vs_time.png
results/plots/speed_vs_time.png
```

#### Numerical convergence analysis

The `scripts/convergence_analysis.py` script evaluates RK4 numerical accuracy against an analytical circular-orbit reference.

Experiment configuration:

| Parameter | Value |
|---|---:|
| Orbital altitude | 400,000 m |
| Simulation duration | 5,600 s |
| Integration step sizes | 40, 20, 10, 5 s |
| Integration method | Classical RK4 |

The experiment compares final numerical spacecraft positions with the analytical circular-orbit position at the same elapsed time.

Run:

```powershell
python scripts/convergence_analysis.py
```

Generated outputs:

```text
results/convergence_report.csv
results/plots/convergence_error.png
```

Reference experiment results:

| Step size | Final-position error | Error reduction |
|---:|---:|---:|
| 40 s | 5.185726 m | — |
| 20 s | 0.290212 m | 17.87× |
| 10 s | 0.017078 m | 16.99× |
| 5 s | 0.001034 m | 16.51× |

The observed error-reduction ratios are consistent with the expected fourth-order convergence behavior of classical RK4 for this particular experiment.

These results are scenario-specific and should not be interpreted as universal numerical error guarantees.

---

## System Architecture

The project separates physical calculations, numerical integration, trajectory processing, visualization, and analytical classification.

| Component | Responsibility |
|---|---|
| `propulsion.py` | Ideal rocket propulsion calculations |
| `staging.py` | Ideal multistage rocket calculations |
| `orbit.py` | Analytical orbital mechanics and constants |
| `dynamics.py` | Two-dimensional central-gravity equations |
| `integrator.py` | RK4 numerical integration and propagation |
| `trajectory.py` | Trajectory data processing and export |
| `visualization.py` | Orbital trajectory and metric plots |
| `classification.py` | Analytical orbital classification |
| `sweep.py` | Orbital insertion-condition parameter sweeps |

Supporting scripts automate:
- Scenario sweeps.
- Trajectory plot generation.
- Numerical convergence experiments.

The test suite validates the individual components and selected integrated workflows.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Primary programming language |
| NumPy | Numerical computing dependency |
| Matplotlib | Scientific visualization |
| Pytest | Automated testing |
| Git | Version control |
| PowerShell | Windows development environment |

---

## Repository Structure

```text
rocket-mission-simulator/
│
├── docs/
│   ├── architecture.md
│   ├── development.md
│   ├── model-assumptions.md
│   ├── roadmap.md
│   └── validation.md
│
├── examples/
│
├── notebooks/
│
├── results/
│   ├── plots/
│   ├── scenario_sweep.csv
│   └── convergence_report.csv
│
├── scripts/
│   ├── convergence_analysis.py
│   ├── generate_plots.py
│   └── scenario_sweep.py
│
├── src/
│   └── rocket_sim/
│       ├── __init__.py
│       ├── classification.py
│       ├── dynamics.py
│       ├── integrator.py
│       ├── orbit.py
│       ├── propulsion.py
│       ├── staging.py
│       ├── sweep.py
│       ├── trajectory.py
│       └── visualization.py
│
├── tests/
│   ├── test_classification.py
│   ├── test_convergence.py
│   ├── test_dynamics.py
│   ├── test_integrator.py
│   ├── test_orbit.py
│   ├── test_orbit_conservation.py
│   ├── test_propulsion.py
│   ├── test_staging.py
│   ├── test_trajectory.py
│   └── test_visualization.py
│
├── .gitignore
├── pyproject.toml
└── README.md
```

---

## Installation

### Requirements

- Python 3.11 or newer.
- Git.
- Windows, Linux, or macOS.

### Windows PowerShell

Clone the repository:

```powershell
git clone https://github.com/nachuuuu/rocket-mission-simulator.git

Set-Location rocket-mission-simulator
```

Create a virtual environment:

```powershell
py -3.11 -m venv .venv
```

Install the project and development dependencies:

```powershell
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip

& ".\.venv\Scripts\python.exe" -m pip install -e ".[dev]"
```

Activate the environment if desired:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux and macOS

```bash
git clone https://github.com/nachuuuu/rocket-mission-simulator.git

cd rocket-mission-simulator

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

python -m pip install -e ".[dev]"
```

---

## Running the Project

Run all commands from the repository root with the virtual environment activated.

### Run the tests

```powershell
python -m pytest
```

### Generate orbital scenario results

```powershell
python scripts/scenario_sweep.py
```

### Generate trajectory plots

```powershell
python scripts/generate_plots.py
```

### Run numerical convergence analysis

```powershell
python scripts/convergence_analysis.py
```

Generated outputs are written to the `results/` directory.

---

## Numerical Convergence Analysis

The project uses classical fourth-order Runge–Kutta integration.

For a sufficiently smooth problem in the asymptotic convergence regime, RK4's global error is expected to scale approximately as:

\[
E(h) \propto h^4
\]

where:

- \(E(h)\) is the numerical error.
- \(h\) is the integration step size.

When the integration step is halved, the expected error reduction is approximately:

\[
\frac{E(h)}{E(h/2)} \approx 16
\]

The M5 experiment evaluates this behavior using an analytical circular-orbit reference.

The experiment is reproducible through:

```powershell
python scripts/convergence_analysis.py
```

See [Validation and Testing](docs/validation.md) for the validation strategy and measured results.

---

## Testing and Validation

The project uses Pytest for automated testing.

The test suite covers:

- Ideal propulsion calculations.
- Multistage rocket calculations.
- Analytical orbital calculations.
- Central-gravity dynamics.
- RK4 integration.
- Trajectory propagation.
- Orbital energy and angular momentum conservation.
- Trajectory visualization.
- Orbital classification.
- Scenario sweep behavior.
- Numerical convergence.

Run the complete suite:

```powershell
python -m pytest
```

**Latest recorded checkpoint:** 135 tests passed.

Passing tests establish behavior for the covered cases. They do not certify the simulator for real-world aerospace engineering.

See:
- [Validation and Testing](docs/validation.md)
- [Model Assumptions](docs/model-assumptions.md)

---

## Physical Model and Assumptions

The orbital model uses a spherical Earth and central inverse-square gravity.

The configured constants are:

| Constant | Value |
|---|---:|
| Earth mean radius | 6,371,000 m |
| Earth gravitational parameter | 3.986004418 × 10¹⁴ m³/s² |

The initial model assumes:

- Two-dimensional inertial motion.
- Point-mass spacecraft.
- Central inverse-square gravity.
- Vacuum conditions.
- Ideal propulsion calculations.
- No atmospheric drag or powered ascent in orbital propagation.

See [Model Assumptions](docs/model-assumptions.md) for the complete model definition and limitations.

---

## Known Limitations

This project is an educational simulator, not a high-fidelity mission-analysis system.

The current implementation does not model:

- Atmospheric density and drag.
- Powered ascent or finite-duration burns.
- Guidance, navigation, and control.
- Earth oblateness and higher-order gravity harmonics.
- Third-body gravitational perturbations.
- Spacecraft attitude and rotational dynamics.
- Structural constraints or launch-vehicle engineering.
- Real-world launch windows or operational constraints.

Analytical orbital classifications are not predictions of real mission feasibility.

Numerical convergence results apply to the tested configuration and do not establish a universal error bound.

The simulator must not be used for real-world launch decisions or flight-dynamics certification.

---

## Development Roadmap

| Milestone | Description | Status |
|---|---|---|
| M0 | Environment and repository | Complete |
| M1 | Propulsion and staging | Complete |
| M2 | Analytical orbital mechanics | Complete |
| M3 | Dynamics and numerical integration | Complete |
| M4 | Orbital classification and scenario sweeps | Complete |
| M5 | Visualization and numerical convergence | Complete |
| M6 | Documentation and release preparation | In progress |

The roadmap is maintained in [docs/roadmap.md](docs/roadmap.md).

---

## License

No license has currently been added to this repository.

Unless and until a license is included, reuse, modification, and redistribution are not granted by the repository owner.

---

**Repository:** [github.com/nachuuuu/rocket-mission-simulator](https://github.com/nachuuuu/rocket-mission-simulator)

**Project:** Rocket Mission & Orbit Simulator

**Development language:** Python

**Current milestone:** M6 — Documentation and Release