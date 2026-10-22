# Validation Strategy

## Purpose

Validation checks whether the code follows the documented mathematical model and whether numerical results behave as expected. Passing tests does not establish that the simplified model is suitable for real launch or mission planning.

## Validation layers

### 1. Input and unit validation

For every public function:
- Document the units of every argument and return value.
- Test invalid values and domain boundaries.
- Reject non-finite inputs when they would make the result meaningless.
- Avoid mixing altitude above Earth's surface with geocentric radius from Earth's centre.

### 2. Analytical orbital references

The existing orbital tests use an altitude of 400 km, convert it to geocentric radius by adding the configured mean Earth radius, and compare:
- Gravity magnitude against approximately 8.6943 m/s².
- Circular speed against approximately 7,672.6 m/s.
- Circular period against approximately 92.41 minutes.

The test suite also checks that higher circular radii have lower gravity and circular speed, but longer orbital periods.

### 3. Propulsion references (planned in M1)

Test thrust, thrust-to-weight ratio, ideal rocket-equation delta-v, and stage mass accounting against hand-calculated or independently derived reference values. Include invalid and boundary inputs, including non-positive masses and inconsistent stage masses.

### 4. Dynamics and integration (planned in M3)

Use a circular-orbit initial condition as a reference:
- Set the speed from the analytical circular-orbit formula.
- Verify gravity is directed toward the origin.
- Check that radius and speed remain close to their expected behavior over a suitable integration interval.
- Report numerical drift and ensure the tolerance reflects the selected numerical method and step size.

Do not select tolerances merely to make a test pass; explain the expected numerical error.

### 5. Outcome classification (planned in M4)

Construct representative Earth-intersecting, bound, and escaping cases. Define classification criteria and tolerances before running broad sweeps. Include cases close to boundaries and make any ambiguity explicit.

### 6. Convergence study (planned in M5)

Run the same reference scenario using at least three time-step sizes. Compare a clearly defined metric, such as final-state error against a reference solution or drift in a conserved quantity. Record the step sizes and observed differences. Smaller steps are not automatically proof of correctness, so compare against analytical or otherwise justified references.

## Test execution

On the established Windows environment:

```powershell
& "D:\rocket-mission-simulator\.venv\Scripts\python.exe" -m pytest
```

## Reporting results

A validation report should state:
- Code revision or commit.
- Python and dependency versions where relevant.
- Physical constants and initial conditions.
- Numerical method and settings.
- Tests run and their outcomes.
- Metrics, tolerances, and known limitations.

Never describe a test as passing unless it was actually run and its result observed.
