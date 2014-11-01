from BezierN import BezierN
from xfoil_dat import *

def make_foil(gen,name):
    #define x
    upx = [0, 0, 0.2, 0.4, 0.6, 0.8, 1.0]
    downx = upx

    #declare Y
    upy       = [0]*7
    downy     = [0]*7
    
    # Leading edge
    upy   [1] = gen[0]
    downy [1] = - gen[1]
    # camber + thickness
    upy   [2] = gen[2] + gen[6]
    upy   [3] = gen[3] + gen[7]
    upy   [4] = gen[4] + gen[8]
    upy   [5] = gen[5] + gen[9]
    
    downy [2] = gen[2] - gen[6]
    downy [3] = gen[3] - gen[7]
    downy [4] = gen[4] - gen[8]
    downy [5] = gen[5] - gen[9]
    
    #generate foil
    n=60;
    MyBezier = BezierN(7)
    pupx  = MyBezier.interpolate(upx   ,n)
    pupy  = MyBezier.interpolate(upy   ,n)
    pdownx= MyBezier.interpolate(downx ,n)
    pdowny= MyBezier.interpolate(downy ,n)

    # save foil
    foilfile = open(name+".dat",'w')
    foilfile.write(name+"\n")
    for i in range (n,0,-1):
         foilfile.write(  " %1.6f    %1.6f\n" %(pupx[i],pupy[i]))
    for i in range (0,n+1):
         foilfile.write(  " %1.6f    %1.6f\n" %(pdownx[i],pdowny[i]))
    foilfile.close()
