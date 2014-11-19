import apso
from airfoil_generator import generate_airfoil
from xfoil_pipeline import *

import os
import numpy as np

# Airfoil is defined by
#  LEU = Leading edge up            LED = Leading edge down      
#  C20 = Camber at 20%              T20 = Thickness at 20%
#  C40 = Camber at 40%              T40 = Thickness at 40%
#  C60 = Camber at 60%              T60 = Thickness at 60%
#  C80 = Camber at 80%              T80 = Thickness at 80%

#            LEU     LED      C20    C40     C60    C80      T20    T40    T60    T80
gen_max = [  0.100,  0.100,   0.10,  0.10,   0.10,  0.10,    0.10,  0.10,  0.10,  0.10 ]
gen_min = [  0.035,  0.035,   0.00,  0.00,   0.00,  0.00,    0.065,  0.04,  0.015,  0.015 ]

def eval_function(*args):
    f = open(r"..\airfoils\%s.log"%name, 'r')
    lines = f.readlines()
    LatLDmax = 0
    LDmax,LD,count = 0,0,0
    Cm = 0
    for i in range(12,len(lines)):
        words = string.split(lines[i])
        LD = 0
        if float(words[0]) in [1.0,2.0,3.0,4.0]:
            LD = float(words[1])/float(words[2])
            count += 1
            if float(words[4])<Cm:
                Cm = float(words[4])      
        if LD > LDmax:
            LDmax = LD
            LatLDmax = float(words[1])
            
    LDmax = LDmax if count == 4 else 0
    
    return LDmax+(Cm*10)+LatLDmax*30

