Welcome to optiFOIL!
By: Jeffrey Nelson

	Sections:
	Intro
	1.Aerodynamics Fundamentals
	2.optiFOIL Controls
	3.Interpreting Results
	4.Technical Details

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
At the bottom of Optifoil.py is a section of code for running a post optimization airfoil
analysis. This functionality can also be accessed from trial_analysis.py. After the import,
the first line "del(s)" is to close the swarm and thus save the latest changes to the swarm
log file. "convergence_history()" will save a png file showing the convergence of score
over the latest optimization run (based on the .log file). "full_analysis()" will plot all
of the relevant airfoil polars from the most successful airfoil and save the data as a .csv
png's of the plots will be saved to the src folder as well. Finally, "airfoil_properties()"
takes the airfoil's chord-length as an input, and outputs a .png file with the airfoil
geometry, area, perimeter, and maximumthickness value. 


===========================================================================================
	4.Technical Details
===========================================================================================
apso.py - Fully functional and commented, with test cases
    A module that allows for generalized optimization of bound-constrained problems using 
the APSO method. The module also has the additional capability to create logfiles to store 
the genes of each generation, and new swarms can use these genes as seed values. A neat 
visualization of the APSO method in progress can be seen by running the 
apso_visualization.py module. (This can be quite taxing on the graphics card)
   
The algorithm is modified from the matlab code found in:
    Xin-She Yang, "Nature-Inspired Metaheuristic Algorithms", Second Edition, Luniver Press
, (2010). www.luniver.com

requires: numpy
-------------------------------------------------------------------------------------------
xfoil_pipeline.py - Functional, Commented
   This module contains the XFPype object which will run the XFOIL commands necessary to 
load an airfoil from a .dat file, set the environmental conditions as desired, and generate
airfoil polar log files which are vital in the wing design process. This is not a 
generalized XFOIL pipeline as it is only one way communication (receiving messages while 
running a subprocess is horrifically slow) specific to airfoil polar generation.

Code for the xfoil pipeline was modified from:
    https://hakantiftikci.wordpress.com/2010/12/21/using-xfoil-and-automating-via-python-subprocess-module/
   
A major challenge was minimizing the runtime of this airfoil polar calculation. Ideally I 
would like to suppress the graphical interface from appearing at all when I run the XFOIL 
commands, but since I cannot figure out how to do that through the subprocess module, I 
looked to other methods and found that I could cut calculation time nearly in half through 
multi-threading. I divide the calculations that I want to do into smaller sections, then 
open a xfoil subprocess to work on each subsection.

requires: subprocess, threading, xfoil.exe (already in the \bin directory)
-------------------------------------------------------------------------------------------
airfoil_generator.py - Fully functional and commented, with test cases
    This module uses a Bezier curve parameterization[1] to generate an airfoil coordinate 
file (.dat) in an format that can be read by XFOIL. The airfoil is defined by 2 bezier 
curve's for the upper and lower surface which are in turn defined by 10 different control 
points which constitute the gene for one airfoil.

Bezier Curve implementation from stackoverflow, user reptilicus:
    http://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy?rq=1
 [1]: http://pubs.sciepub.com/ajme/2/4/1/

requires: numpy, scipy
-------------------------------------------------------------------------------------------
optiFOIL.py - Functional with comments,
    This module ties together all of the pieces above to run airfoil optimization trials. 
Most of the work that is left to do is in cleaning up the evaluation function and boundary 
conditions which are both found in this module. At V1.1, running this file will begin a 
small optimization trial of population size 5 iterated over 30 cycles for a Reynolds number
of 150000, and an Ncrit value of 5 (should take <1 minute; it will rapidly open and close 
windows which can be a strain on the eyes).

requires: All of the above
-------------------------------------------------------------------------------------------
trial_analysis.py - Functional with comments,
    This module is for analyzing the results of an optimization run. It will generate 7 
plots and output some .csv data. The first plot is the convergence history of the 
optimization run. The next is the geometry of the airfoil. Finally, the last 5 are airfoil
polar graphs: alpha vs Cl/Cd, alpha vs Cl, alpha vs Cd, alpha vs Cm, Cd vs Cl. The csv file
will output the data used to generate the airfoil polars.

requires: All of the above + matplotlib
