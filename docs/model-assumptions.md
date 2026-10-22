

\# Rocket Mission and Orbit Simulator — Model Assumptions



\## Purpose

An educational simulator connecting ideal rocket propulsion calculations

to simplified two-dimensional orbital trajectories.



\## Units

\- Distance: metres (m)

\- Time: seconds (s)

\- Mass: kilograms (kg)

\- Force: newtons (N)

\- Velocity: metres per second (m/s)

\- Acceleration: metres per second squared (m/s^2)

\- Gravitational parameter: cubic metres per square second (m^3/s^2)



\## Earth Model

\- Mean Earth radius: 6,371,000 m

\- Gravitational parameter: 3.986004418e14 m^3/s^2

\- Earth is initially modelled as spherical.

\- Gravity follows the central inverse-square law.



\## Propulsion Model

\- Initial propulsion calculations use ideal equations.

\- Delta-v uses the Tsiolkovsky rocket equation.

\- Atmospheric drag, gravity losses, and finite-burn trajectory effects

&#x20; are not included in ideal delta-v calculations.

\- Staging assumptions must explicitly account for discarded dry mass

&#x20; and the mass carried by each stage.



\## Orbital Model

\- The initial orbital model is two-dimensional.

\- The initial trajectory model uses point-mass motion under central gravity.

\- Circular-orbit formulas are analytical reference cases.

\- Numerical integration accuracy must be evaluated separately.



\## Limitations

This is an educational numerical model, not a launch-planning tool.

Real launch vehicles require additional physical effects, engineering

constraints, and independent validation.



