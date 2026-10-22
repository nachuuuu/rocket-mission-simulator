# Development Roadmap

This roadmap preserves the planned scope and order of work. A feature is not considered complete merely because it is described here; completion requires implementation, tests, and review.

## M0 — Environment and repository

**Purpose:** Establish a reproducible Python project and a clean Git baseline.

Scope:
- Python environment and dependency configuration.
- `src/` package layout and `tests/` directory.
- Git exclusions for environments, caches, and build outputs.
- Initial assumptions and repository checkpoint.

**Status:** Baseline established. The repository is version-controlled and has a remote checkpoint.

## M1 — Propulsion

**Purpose:** Implement ideal propulsion calculations independently of trajectory integration.

Planned functions:
- Thrust from mass flow rate and effective exhaust velocity, with clearly documented assumptions.
- Thrust-to-weight ratio using thrust and vehicle weight at a specified gravitational acceleration.
- Ideal rocket delta-v using the Tsiolkovsky equation.
- Ideal staging calculations with explicit accounting for propellant mass, dry mass, payload, and discarded stages.

Acceptance criteria:
- SI units are used and documented.
- Invalid masses, flow rates, exhaust velocities, and other physical inputs are handled explicitly.
- Edge cases have tests.
- Formula tests use independently calculated reference values.
- Staging conventions and the mass included at each stage boundary are documented.

## M2 — Orbital equations

**Purpose:** Establish analytical reference calculations.

Implemented baseline:
- Central-gravity acceleration magnitude.
- Circular-orbit velocity.
- Circular-orbit period.
- Earth gravitational parameter and mean radius constants.
- Validation for finite, positive radius inputs.

Acceptance criteria:
- Analytical formulas are covered by tests.
- Units and geocentric radius conventions are explicit.
- Invalid input behavior is tested.

**Status:** Core functions and tests are present in `src/rocket_sim/orbit.py` and `tests/test_orbit.py`.

## M3 — Dynamics and integration

**Purpose:** Simulate two-dimensional point-mass motion under Earth's central gravity.

Planned work:
- Define state-vector order, coordinate convention, and SI units.
- Implement state derivatives for position and velocity.
- Integrate the equations with a documented numerical method.
- Add a circular-orbit test case and diagnostics for its invariants.

Acceptance criteria:
- State and derivative dimensions are validated.
- Gravity points toward Earth's centre.
- A circular-orbit scenario behaves consistently with the analytical reference.
- Numerical errors and integration settings are reported rather than hidden.

## M4 — Scenario sweeps and classification

**Purpose:** Explore how initial conditions affect a simplified trajectory.

Planned work:
- Sweep insertion speed and flight-path angle.
- Detect Earth intersection using the configured Earth radius.
- Classify trajectories as Earth-intersecting, bound, or escaping, with classification rules defined in documentation.
- Record assumptions and simulation settings with the outputs.

Acceptance criteria:
- Classification boundaries and numerical tolerances are explicit.
- Tests cover representative outcomes and boundary cases.
- The classification does not imply real-world mission feasibility.

## M5 — Plots and convergence

**Purpose:** Make simulation results inspectable and numerically defensible.

Planned work:
- Label trajectory plots with units and reference geometry.
- Compare at least three integration step sizes.
- Summarize how trajectory outputs change as the step size is reduced.
- Document limitations of the chosen integration method.

Acceptance criteria:
- Plots have titles, axis labels, units, and legends where needed.
- Output is reproducible from documented settings.
- A convergence report identifies metrics and step sizes.
- Conclusions are limited to what the numerical comparison supports.

## M6 — Documentation and release

**Purpose:** Review the complete educational model and publish a coherent release checkpoint.

Planned work:
- Complete setup instructions and worked examples.
- Review assumptions and limitations against the code.
- Run the full test suite.
- Inspect Git status and diff, then commit the release state.
- Document known limitations and future work.

Acceptance criteria:
- A clean setup can install the project and run tests.
- Documentation matches implemented behavior.
- All tests pass, or any known failures are explicitly recorded.
- No generated results, virtual environments, secrets, or unrelated files are committed.

## Explicitly deferred

The initial scope excludes a graphical user interface, atmospheric drag, powered ascent, guidance and control, Earth oblateness, and multi-body perturbations. These should only be considered after the simplified vacuum model is validated and the core milestones are complete.
