# Validation and Testing

## Purpose

This document describes how the Rocket Mission & Orbit Simulator is tested and how numerical results should be interpreted.

Tests establish that implemented functions behave as expected for selected cases. Passing tests does not prove that the simplified physical model is suitable for real-world mission design.

## Test framework

The project uses `pytest`.

Run the complete test suite from the repository root:

```powershell
python -m pytest
```

Run an individual module's tests with:

```powershell
python -m pytest tests/test_propulsion.py
python -m pytest tests/test_orbit.py
python -m pytest tests/test_visualization.py
python -m pytest tests/test_classification.py
python -m pytest tests/test_sweep.py
```

A test file should exist before running its corresponding command.

## Validation layers

### 1. Propulsion calculations — implemented

Tests cover ideal rocket performance calculations and their expected numerical behavior, including delta-v calculations and input handling.

These tests validate the implemented mathematical model, not the performance of a real engine or launch vehicle.

### 2. Orbital calculations — implemented

Orbital calculations are tested using representative states and expected mathematical behavior. Constants and units must remain consistent across calculations.

### 3. Numerical integration and visualization — implemented

Tests cover implemented trajectory integration and visualization functionality. Numerical output should be inspected for sensible behavior, and plotting code should be tested without requiring manual interaction where possible.

### 4. Initial-condition classification — implemented

Classification tests cover representative orbital outcomes:

- Bound orbit.
- Earth-intersecting trajectory.
- Escaping trajectory.
- Unbound inbound trajectory that intersects Earth.
- Invalid states and invalid numerical tolerances.

The classifier uses specific orbital energy, angular momentum, eccentricity, periapsis, and the configured Earth radius.

Near-zero specific energy is treated as parabolic or unbound according to the configured energy tolerance. Classification depends on the stated analytical model and should not be interpreted as a complete propagation result.

### 5. Scenario sweeps — implemented

Sweep tests cover the generation of speed and flight-path-angle combinations, expected output structure, and invalid inputs.

The default sweep uses:

- Altitude: 400,000 m.
- Insertion speed: 6,500–11,000 m/s in 250 m/s increments.
- Flight-path angle: −30° to +30° in 5° increments.
- Total: 247 scenarios.

Run the sweep with:

```powershell
python scripts/scenario_sweep.py
```

The script generates `results/scenario_sweep.csv`. The output should contain the initial conditions and classification metrics for each evaluated scenario.

### 6. Numerical convergence — planned

Future convergence work should compare numerical solutions at different integration step sizes or tolerances, where applicable. Acceptance criteria should be defined for the quantities being compared.

## Interpreting results

- A passing test suite confirms behavior only for the cases covered by the tests.
- Numerical outputs depend on the model assumptions, units, and numerical methods.
- An `earth-intersecting` classification indicates a mathematically Earth-intersecting trajectory under the analytical model.
- A negative periapsis altitude is a mathematical indicator of Earth intersection, not a physically realizable below-surface orbit.
- An `escaping` classification does not imply that a real spacecraft can complete a mission or achieve a particular operational objective.
- The current model does not represent all real-world atmospheric, propulsion, guidance, structural, or launch constraints.

## Validation policy

When adding a feature:

1. Add tests for representative valid inputs.
2. Add tests for invalid inputs and boundary conditions where applicable.
3. Run the relevant test module.
4. Run the complete test suite.
5. Document any new assumptions, tolerances, or limitations.
6. Review generated outputs for consistency with the model's intended behavior.
