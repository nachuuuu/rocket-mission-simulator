

\# Rocket Mission and Orbit Simulator — Model Assumptions



\## 1. Purpose and scope



This document describes the physical and numerical assumptions used by Rocket Mission and Orbit Simulator.



The project is an educational simulator connecting ideal rocket propulsion calculations with simplified two-dimensional orbital mechanics.



The models are intended to explore fundamental relationships in propulsion, staging, orbital motion, and numerical integration. They are not intended for operational launch planning, flight certification, or mission-critical engineering.



\## 2. Units and conventions



The simulator uses the International System of Units (SI).



| Quantity | Unit |

|---|---|

| Distance and position | metres (m) |

| Time | seconds (s) |

| Mass | kilograms (kg) |

| Force | newtons (N) |

| Velocity | metres per second (m/s) |

| Acceleration | metres per second squared (m/s²) |

| Gravitational parameter | cubic metres per square second (m³/s²) |

| Specific orbital energy | joules per kilogram (J/kg) |

| Angular momentum per unit mass | m²/s |



The two-dimensional orbital state is represented as:



`\[x, y, vx, vy]`



where `x` and `y` are position coordinates, and `vx` and `vy` are velocity components.



\## 3. Earth and gravitational model



The simulator uses the following Earth reference parameters:



| Parameter | Value |

|---|---:|

| Mean Earth radius | 6,371,000 m |

| Gravitational parameter (μ) | 3.986004418 × 10¹⁴ m³/s² |



The current orbital model assumes:



\- Earth is spherical.

\- Earth is represented as a point-mass gravitational source.

\- Gravitational acceleration follows the central inverse-square law.

\- The gravitational parameter is constant.

\- The orbital simulation operates in a two-dimensional plane.



The gravitational acceleration is directed toward Earth's centre and depends on the spacecraft's distance from that centre.



The model does not currently account for variations in Earth's gravitational field caused by its oblateness or non-spherical mass distribution.



\## 4. Propulsion model



\### 4.1 Ideal rocket equation



The propulsion module uses the Tsiolkovsky rocket equation to calculate ideal velocity change:



\\\[

\\Delta v = v\_e \\ln\\left(\\frac{m\_0}{m\_f}\\right)

\\]



where:



\- `Δv` is ideal velocity change.

\- `ve` is effective exhaust velocity.

\- `m0` is initial vehicle mass.

\- `mf` is final vehicle mass.



The calculation assumes idealized rocket propulsion and does not represent a complete powered-flight trajectory.



\### 4.2 Propulsion limitations



The ideal delta-v calculation does not include:



\- Atmospheric drag.

\- Gravity losses during powered ascent.

\- Steering and guidance losses.

\- Finite-burn trajectory effects.

\- Engine startup and shutdown transients.

\- Real-world engine performance variations.



Consequently, ideal delta-v should not be interpreted as the actual velocity gain of a launch vehicle during a real mission.



\## 5. Staging model



The staging module evaluates idealized multistage rocket performance.



The calculation accounts for the mass contributions of individual stages, including:



\- Propellant mass.

\- Structural or dry mass.

\- Mass carried by a stage during its operation.

\- Mass discarded when a stage is separated.



The model is intended to demonstrate how staging changes the effective mass ratio and ideal velocity capability of a launch vehicle.



It does not simulate the detailed mechanical or dynamic behaviour of stage separation.



\## 6. Orbital mechanics model



\### 6.1 Two-dimensional motion



The orbital simulation represents spacecraft motion in a two-dimensional Cartesian plane.



The state consists of position and velocity components:



`\[x, y, vx, vy]`



The model assumes that the spacecraft can be represented as a point mass.



\### 6.2 Central gravitational motion



The orbital dynamics module models motion under Earth's central gravitational acceleration.



The current model does not include:



\- Atmospheric drag.

\- Earth oblateness and higher-order gravity harmonics.

\- Third-body gravitational perturbations.

\- Solar radiation pressure.

\- Propulsive forces during orbital propagation.



\### 6.3 Analytical reference cases



Circular-orbit calculations provide analytical reference cases for checking numerical propagation.



These reference calculations are also used in numerical convergence analysis.



Analytical reference values and numerically propagated trajectories serve different purposes: the former provide comparison values, while the latter approximate the evolution of the orbital state over time.



\## 7. Numerical integration assumptions



\### 7.1 Runge-Kutta integration



The numerical integrator uses the classical fourth-order Runge-Kutta method (RK4).



RK4 estimates the state at the next time step using four evaluations of the state derivative.



The method has a theoretical local truncation error of order \\(O(h^5)\\) and global error of order \\(O(h^4)\\) under suitable smoothness and stability conditions, where `h` is the integration time step.



These theoretical properties do not guarantee a particular accuracy for every simulation.



\### 7.2 Time-step dependence



Numerical accuracy depends on the selected integration time step and the behaviour of the simulated trajectory.



Smaller time steps generally improve accuracy for a sufficiently well-behaved problem, at the cost of additional computation.



The convergence analysis compares numerical propagation against an analytical circular-orbit reference using multiple time steps.



The observed convergence results apply to the specific experiment documented in `validation.md`.



\### 7.3 Numerical limitations



The simulator does not currently provide:



\- Adaptive time-step integration.

\- Automatic error-controlled integration.

\- A universal numerical error bound.

\- Mission-specific numerical accuracy certification.



Numerical results should be interpreted alongside the integration settings and validation evidence.



\## 8. Orbital classification assumptions



The classification module evaluates initial orbital conditions using analytical orbital quantities.



The supported categories are:



\- `bound`

\- `earth-intersecting`

\- `escaping`



Classification uses quantities such as specific orbital energy, angular momentum, eccentricity, and periapsis relative to the configured Earth radius.



The classifier assumes:



\- Point-mass central gravity.

\- A spherical Earth reference radius.

\- Vacuum conditions.

\- Idealized two-body orbital motion.



An `earth-intersecting` result indicates that the calculated orbit intersects the reference Earth radius under the analytical model. It does not simulate atmospheric entry, surface impact dynamics, or vehicle survivability.



An `escaping` result describes the analytical orbital-energy classification. It does not establish that a spacecraft can achieve a real mission objective.



\## 9. Scenario sweep assumptions



The scenario sweep evaluates combinations of insertion speed and flight-path angle at a specified altitude.



Each scenario is evaluated using the implemented orbital calculations and classification logic.



The default sweep contains:



\- 19 insertion speeds.

\- 13 flight-path angles.

\- 247 total scenarios.



The results are dependent on the selected input ranges, reference Earth parameters, and analytical classification assumptions.



The sweep is a parameter-analysis tool, not a launch-window optimizer or operational mission-feasibility assessment.



\## 10. Validation and interpretation



The project uses automated tests and numerical experiments to check implementation behaviour.



Validation includes:



\- Unit tests for propulsion and staging calculations.

\- Tests for orbital reference calculations and dynamics.

\- Tests for numerical integration.

\- Orbital conservation checks.

\- Tests for trajectory propagation and export.

\- Tests for orbital classification.

\- Numerical convergence analysis against an analytical circular-orbit reference.



A passing test suite demonstrates that the tested cases satisfy their expected behaviour. It does not establish that the simulator reproduces every physical effect of a real launch or orbital mission.



See `validation.md` for the validation procedures and numerical results.



\## 11. Overall limitations



The current simulator is an educational numerical model.



It does not currently represent a complete launch vehicle, powered ascent, atmospheric flight, or high-fidelity spacecraft mission.



Real-world aerospace applications require additional physical models, engineering constraints, uncertainty analysis, and independent verification and validation.



Results should therefore be interpreted within the assumptions and limitations documented above.



