
# Architecture

## 1. Project overview

Rocket Mission & Orbit Simulator is an educational Python application for exploring idealized rocket propulsion, staging, orbital mechanics, and numerical trajectory propagation.

The project is organized into independent modules. Each module handles a specific responsibility, allowing physical calculations, numerical methods, analysis workflows, and visualization to be tested separately.

The implemented system includes:

- Ideal rocket propulsion and delta-v calculations.
- Multistage rocket performance calculations.
- Analytical orbital mechanics and reference calculations.
- Two-dimensional orbital dynamics under central gravity.
- Numerical orbit propagation using the fourth-order Runge-Kutta method (RK4).
- Timed propagation and trajectory CSV export.
- Orbital trajectory visualization.
- Analytical orbital classification.
- Insertion-condition scenario sweeps.
- Numerical convergence analysis.

The simulator is intended for educational and analytical use. It is not a mission-grade flight dynamics system or a launch-vehicle design tool.

## 2. Repository structure

```text
rocket-mission-simulator/
├── docs/
│   ├── architecture.md
│   ├── development.md
│   ├── model-assumptions.md
│   ├── roadmap.md
│   └── validation.md
├── examples/
├── notebooks/
├── results/
│   └── plots/
├── scripts/
│   ├── convergence_analysis.py
│   ├── generate_plots.py
│   └── scenario_sweep.py
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
├── .gitignore
├── pyproject.toml
└── README.md
```

Generated result files are stored under `results/`. These include scenario sweep data, convergence reports, and visualization outputs. Their exact presence depends on which analysis scripts have been executed.

## 3. System architecture

The application follows a modular architecture:

1. Physical constants and analytical calculations provide the reference values.
2. Propulsion and staging modules calculate idealized rocket performance.
3. Orbital dynamics defines the equations of motion.
4. The numerical integrator propagates the orbital state over time.
5. Trajectory utilities manage timed propagation and data export.
6. Classification and sweep modules evaluate orbital insertion conditions.
7. Visualization and convergence analysis provide tools for inspecting and validating results.

The modules can be used independently or combined into larger analysis workflows.

## 4. Core components

### 4.1 Propulsion — `propulsion.py`

Implements ideal rocket performance calculations, including:

- Tsiolkovsky rocket equation.
- Ideal delta-v calculations.
- Relationships between mass ratio, exhaust velocity, and achievable velocity change.

The module focuses on idealized propulsion calculations rather than complete powered-flight simulation.

### 4.2 Staging — `staging.py`

Implements multistage rocket performance calculations.

The staging model accounts for stage mass contributions, including propellant mass, structural or dry mass, and mass carried by preceding stages.

It supports analysis of how staging affects the ideal velocity capability of a launch vehicle.

### 4.3 Orbital mechanics — `orbit.py`

Contains orbital constants and analytical orbital calculations.

The module provides reference calculations used by the numerical simulation and orbital analysis components.

The simulator uses SI units:

- Position: metres.
- Velocity: metres per second.
- Time: seconds.
- Gravitational parameter: cubic metres per square second.

### 4.4 Orbital dynamics — `dynamics.py`

Defines the equations of motion for a two-dimensional spacecraft state under central gravitational acceleration.

The state vector is represented as:

`[x, y, vx, vy]`

where:

- `x`, `y` represent position coordinates in metres.
- `vx`, `vy` represent velocity components in metres per second.

The current dynamics model uses point-mass central gravity.

### 4.5 Numerical integration — `integrator.py`

Implements numerical propagation of the orbital state using the classical fourth-order Runge-Kutta method (RK4).

The integrator advances the state by evaluating the equations of motion at intermediate points within each time step.

The module supports orbital propagation and is designed to work with the state derivatives defined in `dynamics.py`.

### 4.6 Trajectory management — `trajectory.py`

Provides timed propagation and trajectory data handling.

Its responsibilities include:

- Propagating an initial state over a specified duration.
- Managing propagation time steps.
- Exporting trajectory data to CSV for further inspection and analysis.

### 4.7 Visualization — `visualization.py`

Generates plots for inspecting simulated orbital motion.

The project includes visualization workflows for:

- Orbital trajectories.
- Altitude against time.
- Speed against time.
- Numerical convergence error.

Visualization is used to interpret simulation output. It does not increase the physical fidelity of the underlying model.

### 4.8 Orbital classification — `classification.py`

Classifies an initial orbital state into one of three categories:

- `bound`
- `earth-intersecting`
- `escaping`

The analytical classification uses orbital quantities such as:

- Specific orbital energy.
- Angular momentum.
- Eccentricity.
- Periapsis.
- Configured Earth radius.

The classifier assumes a point-mass Earth and vacuum conditions. It evaluates idealized orbital conditions rather than determining whether a real mission is operationally feasible.

### 4.9 Scenario sweeps — `sweep.py`

Evaluates combinations of orbital insertion conditions at a specified altitude.

The sweep workflow varies insertion speed and flight-path angle, calculates the associated orbital characteristics, and records classification results.

The default scenario sweep evaluates:

- 19 insertion speeds.
- 13 flight-path angles.
- 247 total scenarios.

`scripts/scenario_sweep.py` executes the workflow and writes the generated results to `results/scenario_sweep.csv`.

### 4.10 Numerical convergence analysis

`scripts/convergence_analysis.py` evaluates the numerical accuracy of RK4 propagation by comparing simulated orbital positions against an analytical circular-orbit reference.

The experiment evaluates multiple integration time steps and measures final-position error.

The analysis is used to investigate the expected fourth-order convergence behavior of RK4 for the selected test case.

Generated outputs include:

- `results/convergence_report.csv`
- `results/plots/convergence_error.png`

The results apply to the documented experiment and do not establish a universal error bound for every trajectory or integration configuration.

## 5. Data flow

A typical orbital simulation workflow follows these steps:

1. Define the physical constants and initial orbital state.
2. Calculate analytical orbital reference quantities where required.
3. Pass the initial state to the orbital dynamics model.
4. Integrate the equations of motion using RK4.
5. Perform timed propagation and collect trajectory states.
6. Export trajectory data when required.
7. Generate plots for trajectory, altitude, or speed analysis.
8. Apply analytical classification to evaluate orbital insertion conditions.

A separate parameter-sweep workflow evaluates multiple insertion conditions and exports their classification results.

The convergence workflow compares numerical propagation against an analytical reference using different integration time steps.

Not every workflow requires every module.

## 6. Scripts and analysis workflows

The `scripts/` directory contains executable analysis workflows:

| Script | Responsibility |
|---|---|
| `generate_plots.py` | Generates orbital visualization outputs. |
| `scenario_sweep.py` | Evaluates insertion-condition scenarios and exports results. |
| `convergence_analysis.py` | Measures RK4 numerical convergence against an analytical reference. |

These scripts use functionality implemented in the `rocket_sim` package.

## 7. Testing and validation architecture

The `tests/` directory contains module-level and system-level tests.

The test suite covers:

- Propulsion calculations.
- Multistage performance calculations.
- Orbital reference calculations.
- Central-gravity state derivatives.
- RK4 integration.
- Orbital conservation behavior.
- Trajectory propagation and export.
- Visualization outputs.
- Orbital classification.
- Numerical convergence.

Run the complete test suite from the repository root:

```powershell
python -m pytest
```

Run individual analysis workflows:

```powershell
python scripts/scenario_sweep.py
python scripts/generate_plots.py
python scripts/convergence_analysis.py
```

## 8. Dependencies and environment

The project requires Python 3.11 or later.

Runtime dependencies:

- NumPy
- Matplotlib

Development dependency:

- Pytest

The package configuration and dependency definitions are maintained in `pyproject.toml`.

## 9. Current limitations

The current architecture implements an educational orbital mechanics and rocket performance model. It does not include:

- Atmospheric drag.
- Powered ascent or finite-burn trajectory simulation.
- Guidance and control systems.
- Earth oblateness.
- Third-body gravitational perturbations.
- Detailed engine performance and operational losses.
- Structural, thermal, or aerodynamic vehicle analysis.
- High-fidelity launch or mission constraints.

The orbital classifier uses analytical initial-condition classification. The numerical propagator uses a simplified two-dimensional central-gravity model.

Scenario sweep results and convergence measurements should therefore be interpreted within the assumptions of the implemented models.

For further details, see:

- `model-assumptions.md` — physical assumptions and model limitations.
- `development.md` — development environment and workflow.
- `validation.md` — testing and numerical validation.
- `roadmap.md` — implementation milestones and future work.
