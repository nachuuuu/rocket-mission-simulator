# Software Architecture

## Design principle

Keep the first version small, testable, and organized around physical responsibilities. Analytical calculations, propulsion calculations, numerical dynamics, scenario orchestration, and plotting should remain separable. Planned modules must not be treated as implemented until they exist and have tests.

## Current implementation

### `rocket_sim.orbit`

File: `src/rocket_sim/orbit.py`

Responsibilities:
- Store the initial Earth gravitational parameter and mean radius constants.
- Compute central-gravity acceleration magnitude from geocentric radius.
- Compute circular-orbit speed.
- Compute circular-orbit period.
- Reject non-finite or non-positive radii.

The current acceleration function returns a **magnitude**, not a vector. Directional acceleration belongs in the planned dynamics layer.

### Tests

File: `tests/test_orbit.py`

Responsibilities:
- Compare reference values at 400 km altitude.
- Check expected monotonic relationships with radius.
- Verify invalid inputs are rejected.

## Planned module boundaries

These are proposed responsibilities following the roadmap; modules may be introduced when their milestone begins.

| Module | Responsibility | Milestone |
|---|---|---|
| `propulsion.py` | Thrust, TWR, ideal delta-v, ideal staging | M1 |
| `orbit.py` | Analytical orbital calculations and constants | M2 baseline |
| `dynamics.py` | Two-dimensional state derivatives under central gravity | M3 |
| `integration.py` | Numerical integration and solver settings | M3 |
| `scenarios.py` | Initial conditions, parameter sweeps, trajectory outcomes | M4 |
| `plotting.py` | Labelled trajectory and convergence figures | M5 |

## Data and units

Use SI units internally:
- Position and radius: metres.
- Time: seconds.
- Mass: kilograms.
- Force: newtons.
- Velocity: metres per second.
- Acceleration: metres per second squared.
- Gravitational parameter: cubic metres per second squared.

For two-dimensional trajectories, choose and document a single state-vector convention before implementing the dynamics layer. A suitable convention is `[x_m, y_m, vx_m_s, vy_m_s]`, with the origin at Earth's centre and the initial position and velocity expressed in the same inertial plane.

## Dependency direction

The intended dependency structure is:

1. Constants and analytical orbital equations form the low-level reference layer.
2. Propulsion formulas provide independent ideal performance calculations.
3. Dynamics use the orbital constants but should not depend on plotting.
4. Integration advances the state using dynamics.
5. Scenario code constructs inputs and classifies results.
6. Plotting and reporting consume simulation outputs.

Tests should validate each layer without requiring plots or a complete end-to-end simulation.

## Error handling

Public numerical functions should:
- Define units and input meaning in docstrings.
- Reject invalid domains explicitly.
- Avoid silently clipping physically invalid values.
- Use tolerances in floating-point assertions where appropriate.

## Reproducibility

Record initial conditions, numerical method, time step or tolerances, physical constants, and relevant classification settings with scenario results. Avoid presenting output as physically authoritative when the model omits important real-world effects.
