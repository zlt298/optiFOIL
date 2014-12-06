import apso
from airfoil_generator import generate_airfoil
from xfoil_pipeline import *

import os
import numpy as np

# Airfoil is defined by
#  LEU = Leading edge up        LED = Leading edge down      
#  C20 = Camber at 20%          T20 = Thickness at 20%
#  C40 = Camber at 40%          T40 = Thickness at 40%
#  C60 = Camber at 60%          T60 = Thickness at 60%
#  C80 = Camber at 80%          T80 = Thickness at 80%

#         [  LEU     LED      C20     C40      C60     C80       T20     T40     T60     T80  ]
gen_max = [ 0.100,  0.100,   0.100,  0.100,   0.100,  0.100,    0.100,  0.100,  0.100,  0.100 ]
gen_min = [ 0.035,  0.035,   0.000,  0.000,   0.000,  0.000,    0.065,  0.040,  0.015,  0.015 ]

alpha_sequence = (1 , 4, 1) #Use integers, (Start, End, Step) 

Re    = 150000
Ncrit = 5

niterations = 30 - 1 #first iteration is run at instantiation
nparticles = 10

def log_eval(name, average_results = False, CL_reward = 30, CM_penalty = 10):
    """
    Evaluates the XFOIL logfile with the filename *name*.log
    Airfoil is evaluated at 4 angles, with a scoring multiplier for Coefficient of lift
    and a scoring penalty for adverse moment that are chosen depending on the Reynolds domain
    The function can be set to evaluate for maximum Cl/Cd or maximum average Cl/Cd for the alpha range
    """
    f = open(r"..\airfoils\%s.log"%name, 'r')
    lines = f.readlines()
    LDmax,LatLDmax,CM,count = 0,0,0,0
    for i in range(12,len(lines)):
        LD = 0
        words = [float(x) for x in string.split(lines[i])]
        if words[0] in [float(x) for x in range(alpha_sequence[0],alpha_sequence[0]+1,alpha_sequence[0])]:
            LD = words[1]/words[2]
            count += 1
            if words[4]<CM:
                CM = words[4]      
        if LD > LDmax:
            LDmax = LD
            LatLDmax = words[1]
    LDmax = LDmax if count == 4 else 0
    score = LDmax+(CM*CM_penalty)+LatLDmax*CL_reward
    print 'Airfoil  Number: '+str(name)
    print '          Score: %5.3f\n        Max L/D: %5.3f\nLift at Max L/D: %5.4f'%(score,LDmax,LatLDmax),'\n'
    return score

def eval_function(*args):
    """The evaluation function to be passed to the apso evaluator"""
    LEU,LED,C20,C40,C60,C80,T20,T40,T60,T80 = args
    gen = [LEU,LED,C20,C40,C60,C80,T20,T40,T60,T80]
    name = '%06d' %len([ f for f in os.listdir(r"..\airfoils") if f.endswith(".dat") ])
    generate_airfoil(gen,name)
    xf = XFPype(name,Ncrit,Re,set_alpha = alpha_sequence, mthread = True)
    return log_eval(name)

if __name__ == '__main__':
    # remove all files from last run
    #Do not Edit==============================================================
    filelist = [ f for f in os.listdir(r"..\airfoils") if f.endswith(".dat") ]
    for f in filelist:
        os.remove(os.path.abspath(r"..\airfoils\%s"%f))  
    filelist = [ f for f in os.listdir(r"..\airfoils") if f.endswith(".log") ]
    for f in filelist:
        os.remove(os.path.abspath(r"..\airfoils\%s"%f))
    #Do not Edit==============================================================
    
    s = apso.Swarm(eval_function,zip(gen_min,gen_max),nparticles,log_results = True)
    s.set_control_param(alpha_0 = 0.05,gamma = 0.9)
    s.iterate(niterations)
    #Return the best of the population
    eval_function(*s.global_best)
    name = '%06d' %(len([ f for f in os.listdir(r"..\airfoils") if f.endswith(".dat") ])-1)

    from trial_analysis import *
    del(s)
    convergence_history()
    full_analysis()
    airfoil_properties(chord = 5.5)

    ##s = apso.Swarm(eval_function,zip(gen_min,gen_max),0)
    ##s.seed_from_log('0004',5000)
