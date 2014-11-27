Sorta kinda in progress

Welcome to optiFOIL!
By: Jeffrey Nelson

	Sections:
	Intro
	1.Aerodynamics Fundamentals
	2.optiFOIL Controls
	3.Parameter Fine Tuning
	4.Interpreting Results

Optifoil is a 2D airfoil geometry optimization solution which utilizes the 
Accelerated Particle Swarm Optimization method to iteratively select an airfoil
geometry which is optimum under the specified conditions. As it is a computational 
fluid dynamics solution, optiFOIL will not guarentee ideal results, so be sure to 
proceed to experimental validation as soon as possible.

	1.Aerodynamics Fundamentals

The primary equation which will inform the global design specification is the lift eq:

Lift = 1/2 * rho * V^2 * wetted area * 3D Coefficient of Lift

XFOIL will provide The 2D coefficient of lift (Cl) and the 2D coefficient of drag (Cd)
which can be used to determine the 3d Coefficients (CL and CD). The evaluation
function of optiFOIL (which can be modified) is primarily concerned with maximizing
Cl/Cd for a certain range of angles (default is [1,2,3,4]degrees). XFOIL also requires
two fluid dynamics properties as inputs: Reynolds number and Ncrit.

Reynolds Number Re = density * velocity * characteristic length / viscosity
-Characteristic length for the wing is the chord length
-velocity must be solved for iteratively using the thrust curve and drag calculations

Ncrit is an integer parameter that represents the quality of the boundary layer
-A high number (6-11) is better for controled environments (Clean wind tunnel, good flow straightening)
-A low number is for high turbulence free streams
-For the RC plane scale, 4 - 6 is probably ideal

	2.optiFOIL Controls
Blah blah blah

	3.Parameter Fine Tuning
Blah blah

	4.Interpreting Results
Blah