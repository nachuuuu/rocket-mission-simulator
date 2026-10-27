# Architecture

## Project overview

Rocket Mission & Orbit Simulator is a Python project for exploring idealized rocket performance and orbital mechanics. The codebase separates propulsion calculations, orbital state calculations, numerical integration, trajectory visualization, orbital classification, and scenario sweeps.

The simulator is intended for educational and analytical use. Its idealized results are not a substitute for mission-grade flight dynamics or launch-vehicle engineering.

## Repository structure

```text
rocket-mission-simulator/
├── data/                       # Input datasets and supporting data
├── docs/
│   ├── architecture.md         # System design
│   ├── model-assumptions.md    # Physical assumptions and limitations
│   ├── roadmap.md              # Milestones and implementation status
│   └── validation.md           # Testing and validation strategy
├── results/
│   └── scenario_sweep.csv      # Generated orbital scenario results
├── scripts/
│   ├── build_targets.py        # Dataset target generation utility
│   └── scenario_sweep.py      # Orbital scenario sweep utility
├── src/
│   └── rocket_sim/
│       ├── classification.py  # Analytical orbital classification
│       ├── orbit.py           # Orbital constants and calculations
│       ├── propulsion.py      # Ideal rocket performance calculations
│       ├── sweep.py           # Insertion-condition parameter sweeps
│       └── visualization.py   # Orbital trajectory visualizations
└── tests/
    ├── test_classification.py
    ├── test_orbit.py
    ├── test_propulsion.py
    ├── test_sweep.py
    └── test_visualization.py
```

The exact contents of `data/` and `results/` can vary as the project evolves. Generated files should be reproducible from their corresponding scripts wherever practical.

## Main components

### Propulsion

`propulsion.py` contains ideal rocket performance calculations, including the Tsiolkovsky rocket equation and ideal delta-v calculations. These calculations use simplified assumptions and do not model a complete powered flight.

### Orbital mechanics

`orbit.py` contains orbital constants and core calculations used by the simulator. The orbital model uses a two-dimensional state representation:

`[x_m, y_m, vx_m_s, vy_m_s]`

Position is measured in metres and velocity in metres per second.

### Visualization

`visualization.py` provides plots for inspecting orbital trajectories. Visualization supports analysis of simulated results; it does not increase the physical fidelity of the underlying model.

### Orbital classification

`classification.py` classifies an initial orbital state into one of three categories:

- `earth-intersecting`
- `bound`
- `escaping`

The analytical classification uses specific orbital energy, angular momentum, eccentricity, periapsis, and the configured Earth radius. It assumes a point-mass Earth and vacuum.

### Scenario sweeps

`sweep.py` evaluates combinations of insertion speed and flight-path angle at a specified altitude. Each result includes the initial conditions and orbital classification metrics.

`scripts/scenario_sweep.py` runs the default sweep and writes the results to `results/scenario_sweep.csv`.

The default sweep evaluates 19 insertion speeds and 13 flight-path angles, for a total of 247 scenarios.

## Data flow

1. Define physical constants and an initial orbital state.
2. Calculate propulsion or orbital quantities using the relevant module.
3. Integrate or inspect orbital motion using the available simulation functionality.
4. Visualize trajectories where applicable.
5. Classify initial conditions and evaluate parameter combinations.
6. Export generated scenario results for inspection and further analysis.

Not every workflow requires every component.

## Validation

Each major module has corresponding tests under `tests/`. Tests check numerical behavior, representative physical cases, input validation, and output structure.

Run the complete suite from the repository root:

```powershell
python -m pytest
```

Run the scenario sweep with:

```powershell
python scripts/scenario_sweep.py
```

## Current limitations

- The orbital model is simplified and does not constitute a high-fidelity mission simulator.
- The analytical classifier assumes a point-mass Earth and vacuum.
- The classifier evaluates initial conditions; it does not simulate atmospheric entry, powered flight, or guidance.
- Ideal propulsion calculations do not account for all real engine, vehicle, and operational losses.
- Scenario-sweep classifications do not establish real-world launch feasibility.

See `model-assumptions.md` for the physical assumptions and `roadmap.md` for planned improvements.
