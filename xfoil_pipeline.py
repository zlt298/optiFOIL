import subprocess as sp
import os
import sys
import string
#import time





class XFPype(object):
    """
    XFoil Pipeline Object
    Provides functions for running XFOIL commands through python
    """
    
    xfoilpath = r'C:\Users\Jeff\Desktop\ME 481\Optifoil\XFOIL6.99\xfoil.exe'
    alpha = 'aseq 0.9 1.0 0.1\ninit\naseq 1.9 2.0 0.1\ninit\naseq 2.9 3.0 0.1\ninit\naseq 3.9 4.0 0.1'
    
    def __init__(self):
        self.process = sp.Popen(xfoilpath ,stdin=sp.PIPE,stderr=sp.PIPE,stdout=sp.PIPE)

    def cmd(self,s):
        
        
def XFPy(name, Ncrit, Re):
    def Cmd(cmd):
        ps.stdin.write(cmd+'\n')
    ps = sp.Popen(xfoilpath ,stdin=sp.PIPE,stderr=sp.PIPE,stdout=sp.PIPE)
    Cmd('load '+name+'.dat')
    Cmd('OPER')
    Cmd('Vpar') #change boundary layer options
    Cmd('N '+str(Ncrit)) #plot amplification parameter
    Cmd(' ')
    Cmd('visc '+str(Re))
    Cmd('PACC')
    Cmd(name+'.log')  # output file
    Cmd(' ')          # no dump file
    Cmd(alpha)
    Cmd(' ')
    out, err = ps.communicate('quit\n')
    #if 'Convergence' in out: print out
    #print out
    #Cmd('quit')  # exit
    ps.stderr.close()
    ps.stdin.close()
    ps.stdout.close()
    ps.wait()
