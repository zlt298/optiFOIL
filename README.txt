Welcome to optiFOIL!
By: Jeffrey Nelson

	Sections:
	Intro
	1.Aerodynamics Fundamentals
	2.optiFOIL Controls
	3.Interpreting Results

Optifoil is a 2D airfoil geometry optimization solution which utilizes the 
Accelerated Particle Swarm Optimization method to iteratively select an airfoil
geometry which is optimum under the specified conditions. As it is a computational 
fluid dynamics solution, optiFOIL will not guarentee ideal results, so be sure to 
proceed to experimental validation as soon as possible.


===========================================================================================
	1.Aerodynamics Fundamentals
===========================================================================================
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
-A high number (6-11) is better for controled environments
(Clean wind tunnel, good flow straightening)
-A low number is for high turbulence free streams
-For the RC plane scale, 4 - 6 is probably ideal


===========================================================================================
	2.optiFOIL Controls
===========================================================================================
optiFOIL's functionality can be accessed from within optiFOIL.py
Going from top to bottom, the parameters/functions that can be edited are:
	gen_max
	gen_min
	alpha_sequence
	Re
	Ncrit
	ninterations
	nparticles
	log_eval
	eval_function
	*various swarm control parameters*
-------------------------------------------------------------------------------------------
gen_max and gen_min are the parameter upper and lower bounds, respectively. There are 10
input parameters defining the geometry of the wing:LEU,LED,C20,C40,C60,C80,T20,T40,T60,T80.
LEU and LED define the leading edge curvature for the upper and lower airfoil surfaces; the
lower the value, the sharper the leading edge. (Too small a value will cause weird 
divergences) The C values represent upwards camber, and T values represent thickness from 
this camber line. Avoid large or negative cambers, and maintain a minimum thickness for 
realistic results.
-------------------------------------------------------------------------------------------
alpha_sequence is the sequence of angle's of attack the airfoil will be evaluated at. I 
have had good results by doing a rough search at (1,7,2) and then narrowing down based on 
the discovered best.
-------------------------------------------------------------------------------------------
Re is the Reynolds number under which you are optimizing. It might be comfirmation bias, 
but I have had better convergence with 50k multiples.
-------------------------------------------------------------------------------------------
Ncrit as mentioned above
-------------------------------------------------------------------------------------------
niterations and nparticles determine the size of the search you wish to conduct. nparticles
determines the number of random seed airfoils you wish to populate your solution space 
with, while niterations is the number of iterations for these particles to evaluate over.
I suggest using a small population size to determine the number of iterations it takes to 
reach an acceptable level of convergence, then moving to a full scale run. If no swarm 
parameters are changed, convergence is reached in 25 iterations.
-------------------------------------------------------------------------------------------
The log_eval function will take the XFOIL output polars and evaluate them to determine the
hueristic score by which the optimization will take place. Basically, alter this function
to optimize for different airfoil properties. The way the function is currently set up, it
will find the maximum Cl/Cd within the specified alpha_sequence and then apply two score 
modifiers to weight for Cl at max Cl/Cd and penalize large moment coefficients. The 
proportional weights of the Cl bonus and Cm penalty need to be adjusted based on the 
desired airfoil properties, and the Reynolds number where the evaluation takes place. A Cl
bonus of 30 at Re = 150000 will result in appriximately a 1 to 2 score weight between Cl 
and Cl/Cd, while a Cm penalty of 10 at the same Reynolds will result in a 1 to 30-40 score
weight between Cm and Cl/Cd. If you are unsure which to use, simply set both bonuses to 0
and optimize for Cl/Cd.
-------------------------------------------------------------------------------------------
The eval_function function should only be edited to turn multithreading on or off. The 
option is found on the second to last line: 
xf = XFPype(name,Ncrit,Re,set_alpha = alpha_sequence, mthread = True)
if mthread is set to True, a copy of XFOIL will be opened for each alpha in alpha_sequence
and the results will be evaluated simultaneously. Obviously Turn this off if your computer
does not allow multi-threading. Generally speaking, faster computers will benefit more from
multithreading.
-------------------------------------------------------------------------------------------
At the bottom of the optiFOIL.py page is the accelerated particle swarm optimization 
implementation. The first line: 
s = apso.Swarm(eval_function,zip(gen_min,gen_max),nparticles,log_results = True), can be 
edited to set log_results True or False depending on whether or not you wish to keep a log
of gene's and their scores. s.set_control_param(alpha_0 = 0.05,gamma = 0.9) will allow you
to set control parameters of your swarm according to the documentation found in apso.py
-------------------------------------------------------------------------------------------
After running through niterations*nparticles evaluations, optiFOIL will generate a final 
log file for the global best of your population. In the airfoils folder, the largest number
will be the result of your optimization run.


===========================================================================================
	3.Interpreting Results
===========================================================================================
Coming Soon
