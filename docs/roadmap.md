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

#### M4 — Scenario sweeps and classification

**Purpose:** Explore how initial conditions affect idealized orbital outcomes.

**Status:** Implemented; 22 dedicated classification and sweep tests pass.

Implemented work:
- Sweep insertion speeds and flight-path angles at a configurable altitude.
- Classify initial states as `earth-intersecting`, `bound`, or `escaping`.
- Use specific orbital energy, angular momentum, eccentricity, periapsis, and the configured Earth radius.
- Validate sweep inputs and the energy-classification tolerance.
- Export reproducible scenario results to `results/scenario_sweep.csv` using `scripts/scenario_sweep.py`.

Default sweep settings:
- Altitude: 400,000 m.
- Insertion speed: 6,500–11,000 m/s in 250 m/s increments.
- Flight-path angle: −30° to +30° in 5° increments.
- Total scenarios: 247.

Acceptance criteria:
- Classification rules and numerical tolerances are explicit.
- Tests cover representative outcomes and invalid inputs.
- Generated results record the initial conditions and classification metrics.
- The classification is documented as an analytical initial-condition assessment, not a prediction of real mission feasibility.

**Limitations:** The classifier assumes a point-mass Earth and vacuum. It does not model atmospheric drag, powered flight, guidance, or real launch constraints. Negative periapsis altitude indicates a mathematically Earth-intersecting orbit, not a physically realizable below-surface trajectory.

## M5 — Plots and convergence

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
