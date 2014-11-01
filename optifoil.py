import random
from math import *
from airfoil import *

#from xfoil_dat import *
from xfoil import *
from xfoil import xf as Xfoil

import pso
import sys
import os

# remove all files from last run
filelist = [ f for f in os.listdir(".") if f.endswith(".dat") ]
for f in filelist:
    os.remove(f)  
filelist = [ f for f in os.listdir(".") if f.endswith(".log") ]
for f in filelist:
    os.remove(f)


# Airfoil is defined by
#  LEU = Leading edge up            LED = Leading edge down      
#  C20 = Camber at 20%              T20 = Thickness at 20%
#  C40 = Camber at 40%              T40 = Thickness at 40%
#  C60 = Camber at 60%              T60 = Thickness at 60%
#  C80 = Camber at 80%              T80 = Thickness at 80%

#            LEU     LED      C20    C40     C60    C80      T20    T40    T60    T80
genmaxs = [  0.100,  0.100,   0.10,  0.10,   0.10,  0.10,    0.10,  0.10,  0.10,  0.10 ]
genmins = [  0.035,  0.035,   0.00,  0.00,   0.00,  0.00,    0.065,  0.04,  0.015,  0.015 ]


foilnum = 0

def get_name():
    return '%06d' %foilnum

def eval_func(LEU,LED,C20,C40,C60,C80,T20,T40,T60,T80):
    gen = [LEU,LED,C20,C40,C60,C80,T20,T40,T60,T80]
    name = '%06d' %len([ f for f in os.listdir(".") if f.endswith(".dat") ])
    print '\n' + name + ':'
    make_foil(gen,name)
    Xfoil(name,Ncrit,Re)
    
    #return getLDmax(name,10)
    #return getLDmaxPenalty(name)
    #return getLDavg(name)
    #return getLDavgPenalty(name,10)
    return getLscoredLDmax(name,10,25)

def save_best(st):
    make_foil(s.global_best,st)
    Xfoil(st,Ncrit,Re)
    print getLDmax(st,20)


niterations = 25 - 1 #first iteration is run at instantiation
nparticles = 5000
Re = 100000
Ncrit = 9.0

s = pso.swarm(eval_func,zip(genmins,genmaxs),nparticles)
s.iterate(niterations)

make_foil(s.global_best,'result')
Xfoil('result',Ncrit,Re)
print getLDavgPenalty('result',30)
print s.global_best
