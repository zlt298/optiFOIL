import subprocess as sp
import os
import shutil
import sys
import string
import time

xfoilpath = r'C:\Users\Jeff\Desktop\ME 481\Optifoil\XFOIL6.99\xfoil.exe'

def Xfoil(name, Ncrit, Re , alpha_r = 'aseq 0.0 8.0 2.0'):
    def Cmd(cmd):
        ps.stdin.write(cmd+'\n')

    try:
        os.remove(name+'.log')
    except :
        pass

    ps = sp.Popen(xfoilpath ,stdin=sp.PIPE,stderr=sp.PIPE,stdout=sp.PIPE)
    ps.stderr.close()
    # comand part
    Cmd('load '+name+'.dat')
    Cmd('OPER')
    Cmd('Vpar') #change boundary layer options
    Cmd('N '+str(Ncrit)) #plot amplification parameter
    Cmd(' ')
    Cmd('visc '+str(Re))
    Cmd('PACC')
    Cmd(name+'.log')  # output file
    Cmd(' ')          # no dump file
    Cmd(alpha_r)
    #time.sleep(0.5)
    Cmd(' ')     # escape OPER
    Cmd('quit')  # exit
    #print ps.stdout.read()# console ouput for debug
    ps.stdout.close()
    ps.stdin.close()
    ps.wait()
    
    #while (ps.returncode() == None):
        #time.sleep(1)
    #ps.kill()

def getLDcap():
    return 160

def getLDmax(name):
    filename = name+".log"
    f = open(filename, 'r')
    flines = f.readlines()
    LDmax = 0
    for i in range(12,len(flines)):
        #print flines[i]
        words = string.split(flines[i]) 
        LD = float(words[1])/float(words[2])

        if LD > getLDcap():
            break
        
        if(LD>LDmax):
            LDmax = LD
    #print LDmax
    return LDmax

def getLDmaxPenalty(name,penalty):
    filename = name+".log"
    f = open(filename, 'r')
    flines = f.readlines()
    LDmax = 0
    m = 0
    for i in range(12,len(flines)):
        #print flines[i]
        words = string.split(flines[i]) 
        LD = float(words[1])/float(words[2])

        if LD > getLDcap():
            break
        
        if(LD>LDmax):
            LDmax = LD
            m = float(words[4])
    print LDmax , LDmax + (m * penalty)
    return LDmax + (m * penalty)

def getLDavg(name):
    filename = name+".log"
    f = open(filename, 'r')
    flines = f.readlines()
    LDsum,count = 0,0
    for i in range(12,len(flines)):
        #print flines[i]
        words = string.split(flines[i]) 
        LD = float(words[1])/float(words[2])

        if LD > getLDcap():
            break
        
        LDsum = LDsum + LD
        count += 1
    return LDmax /float(count)

def eval_results(Ncrit,Re,alpha_r = 'aseq 0.0 8.0 0.5',penalty = 140):
    filelist = [ f.split('.')[0] for f in os.listdir(".") if f.endswith(".dat") ]
    filelist = filelist[::-1]
    for i in filelist:
        print '\n'+i
        Xfoil(i,Ncrit,Re,alpha_r)
        if getLDmaxPenalty(i,penalty) > 85.3:
            break

def convergence_history():
    from pylab import plot as plt, show
    filelist = [ f.split('.')[0] for f in os.listdir(".") if f.endswith(".log") ][:-1]
    dat = []
    for i in filelist:
        #print '\n'+i
        m = getLDmax(i)
        if m != 0:
            dat.append(m)
    plt(dat)
    show()
