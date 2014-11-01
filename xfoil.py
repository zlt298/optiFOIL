import subprocess as sp
import os
import shutil
import sys
import string
import time

xfoilpath = r'C:\Users\Jeff\Desktop\ME 481\Optifoil\XFOIL6.99\xfoil.exe'
##Re = 2e5
##Ncrit = 9
##name = '000001'
alpha = 'aseq 0.9 1.0 0.1\ninit\naseq 1.9 2.0 0.1\ninit\naseq 2.9 3.0 0.1\ninit\naseq 3.9 4.0 0.1'

def xf(name, Ncrit, Re):
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


def getLDcap():
    return 160

def getLscoredLDmax(name,penalty,score):
    filename = name+".log"
    f = open(filename, 'r')
    flines = f.readlines()
    LatLDmax = 0
    LDmax,LD,count = 0,0,0
    Cm = 0
    for i in range(12,len(flines)):
        words = string.split(flines[i])
        LD = 0
        if float(words[0]) in [1.0,2.0,3.0,4.0]:
            LD = float(words[1])/float(words[2])
            count += 1
            if float(words[4])<Cm:
                Cm = float(words[4])
            if LD > getLDcap():
                break        
        if LD > LDmax:
            LDmax = LD
            LatLDmax = float(words[1])
            
    LDmax = LDmax if count == 4 else 0
    
    #print LDmax,LatLDmax,Cm
    return LDmax+(Cm*penalty)+LatLDmax*score

def getLDmax(name,penalty):
    filename = name+".log"
    f = open(filename, 'r')
    flines = f.readlines()
    LDmax,LD,count = 0,0,0
    Cm = 0
    for i in range(12,len(flines)):
        words = string.split(flines[i])
        LD = 0
        if float(words[0]) in [6.0,7.0,8.0]:
            LD = float(words[1])/float(words[2])
            count += 1
            if float(words[4])<Cm: Cm = float(words[4])
            if LD > getLDcap():
                break        
        if LD > LDmax: LDmax = LD
    LDavg = LDmax if count == 3 else 0
    #print LDavg,LDavg+(Cm*penalty)
    return LDavg+(Cm*penalty)

def getLDavgPenalty(name,penalty):
    filename = name+".log"
    f = open(filename, 'r')
    flines = f.readlines()
    LDsum,count = 0,0
    Cm = 0
    for i in range(12,len(flines)):
        words = string.split(flines[i])
        LD = 0
        if float(words[0]) in [6.0,7.0,8.0]:
            LD = float(words[1])/float(words[2])
            count += 1
            if float(words[4])<Cm: Cm = float(words[4])
            if LD > getLDcap():
                break        
        LDsum = LDsum + LD
    LDavg = LDsum /float(count) if count == 3 else 0
    #print LDavg,LDavg+(Cm*penalty)
    return LDavg+(Cm*penalty)

def getLDavg(name):
    filename = name+".log"
    f = open(filename, 'r')
    flines = f.readlines()
    LDsum,count = 0,0
    for i in range(12,len(flines)):
        #print flines[i]
        words = string.split(flines[i])
        LD = 0
        if float(words[0]) in [6.0,7.0,8.0]:
            LD = float(words[1])/float(words[2])
            count += 1
            if LD > getLDcap():
                break        
        LDsum = LDsum + LD
    LDavg = LDsum /float(count) if count == 3 else 0
    #print LDavg
    return LDavg

def eval_results(penalty = 10):
    filelist = [ f.split('.')[0] for f in os.listdir(".") if f.endswith(".dat") ]
    filelist = filelist[::-1]
    vmax = (0,0)
    for i in filelist:
        #v = getLDavgPenalty(i,penalty)
        v = getLscoredLDmax(i,10,25)

        #if v > 70:
            #print (i,v)
        
        if v > vmax[1]:
            vmax = (i,v)
    print vmax

def plot_latest():
    from pylab import plot as plt, show
    pass

def convergence_history():
    from pylab import plot as plt, show
    filelist = [ f.split('.')[0] for f in os.listdir(".") if f.endswith(".log") ][:-1]
    dat = []
    overall = [None,0]
    for i in filelist:
        #print '\n'+i
        #m = getLDmax(i,0)
        #if m>45:overall = [i,m]
        #m = getLDavg(i)
        m = getLscoredLDmax(i,0,0)
        #m = getLDavgPenalty(i,10)
        #if m > 0 and m<75:
        dat.append(m)
    #print overall
    plt(dat)
    show()
