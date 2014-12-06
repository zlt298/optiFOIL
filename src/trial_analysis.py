import os,csv
import numpy as np

from optiFOIL import log_eval,alpha_sequence,Re,Ncrit
import apso
from airfoil_generator import generate_airfoil
from xfoil_pipeline import *

class XFPype_indepth(XFPype):
    """Extend XFPype for a more in-depth analysis of a single airfoil,mthread disallowed"""
    def __init__(self, name, Ncrit, Re, set_alpha = (-16,16,0.1)):
        self.set_alpha(*set_alpha)
        procs = []
        threads = []
        for ind,alpha in enumerate(self.alpha_list):
            process = sp.Popen(self.xfoilpath ,stdin=sp.PIPE,stderr=sp.PIPE,stdout=sp.PIPE)
            out = self.run_analysis(process,name,Ncrit,Re,alpha)
            if "VISCAL:  Convergence failed" in out:
                print "Convergence failed on alpha = %s, skipping..."%alpha

    def set_alpha(self,start,stop,step):
        self.alpha_float = np.linspace(start,stop,(stop-start+step)/step)
        self.alpha_list = ['aseq %4.2f %4.2f 0.1'%(x-0.1,x) for x in self.alpha_float]
        self.alpha_count = len(self.alpha_list)
        self.alpha = '\ninit\n'.join(self.alpha_list)
        return None    

    def run_analysis(self,proc,name, Ncrit, Re, alpha):
        proc.stdin.write(r"load ..\airfoils\\"+name+'.dat'  +'\n')
        proc.stdin.write('OPER'                             +'\n')
        proc.stdin.write('Vpar'                             +'\n')
        proc.stdin.write('N %i'%Ncrit                       +'\n')
        proc.stdin.write(' '                                +'\n')
        proc.stdin.write('ITER 70'                          +'\n')
        proc.stdin.write('visc %i'%Re                       +'\n')
        proc.stdin.write('PACC'                             +'\n')
        proc.stdin.write(r"..\airfoils\\"+name+'.log'       +'\n')
        proc.stdin.write(' '                                +'\n')
        proc.stdin.write(alpha                              +'\n')
        proc.stdin.write(' '                                +'\n')
        out, err = proc.communicate('quit\n')
        proc.stderr.close()
        proc.stdin.close()
        proc.stdout.close()
        proc.wait()
        return out

latest_log = 'log%04d.apso' %(len([ f for f in os.listdir(r".") if f.endswith(".apso") ])-1)
latest_airfoil = '%06d' %(len([ f for f in os.listdir(r"..\airfoils") if f.endswith(".dat") ])-1)

import matplotlib as mpl
import matplotlib.pyplot as plt
def convergence_history():
    """Plot the non-zero hueristic scores for the most recent optiFOIL run."""
    log = open(latest_log,'r')
    score = []
    for line in log:
        temp = float(line.split(';')[-1])
        if temp == 0:score.append(-1)
        else: score.append(temp)
    plt.plot(range(len(score)),score,'.b',label = 'Score')
    plt.plot([0,len(score)],[max(score),max(score)],'--r',label ='Maximum')
    plt.legend(loc = 'lower right')
    plt.title('Airfoil Convergence History')
    plt.ylabel('Score')
    plt.xlabel('Evaluation #')
    plt.ylim([0,int(max(score)*1.1)])
    #plt.show()
    plt.savefig('Convergence History')
    return None

def logPlots(name,alphalist):
    f = open(r"..\airfoils\\"+name+'.log', 'r')
    flines = f.readlines()
    data = []
    for i in range(12,len(flines)):
        words = [float(x) for x in string.split(flines[i])]
        a,Cl,Cd,Cdp,Cm = tuple(words[:5])
        if float(a) in alphalist:
            data.append((a,Cl,Cd,Cl/Cd,Cm))
    data = sorted(list(set(data)))
    with open(name+' result.csv', 'w+b') as csvfile:
        cw = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_NONE)
        cw.writerow(('Alpha','Cl','Cd','Cl/Cd','Cm'))
        for line in data:
            cw.writerow([str(x) for x in line])
    return data

def airfoil_properties(chord = 1.):
    """Get parameters of newest airfoil (perimeter, area, maximum thickness)"""
    from airfoil_generator import generate_airfoil
    def polyArea(xx,yy):
        """Loop integral to find Polygon Area, order matters"""
        Itotal = 0
        for ind in range(len(xx)-1):
            Itotal += 0.5*(yy[ind+1]+yy[ind])*(xx[ind+1]-xx[ind])
        Itotal += 0.5*(yy[0]+yy[-1])*(xx[0]-xx[-1])    
        return Itotal
    def polyPeri(xx,yy):
        """Trivial Polygon Perimeter"""
        Ltotal = 0
        for ind in range(len(xx)-1):
            Ltotal += np.sqrt((yy[ind+1]-yy[ind])**2+(xx[ind+1]-xx[ind])**2)
        Ltotal += np.sqrt((yy[0]-yy[-1])**2+(xx[0]-xx[-1])**2) 
        return Ltotal
    gene = [float(i) for i in open(latest_log,'r').readlines()[-1].split(';')[0].split(',')]
    generate_airfoil(gene,latest_airfoil,181) #increase fidelity of airfoil
    with open(r"..\airfoils\%s.dat"%latest_airfoil,'r') as foilfile:
        x,y = [],[]
        for ind,row in enumerate(foilfile):
            if ind!=0:
                x.append(float(row.split('    ')[0]))
                y.append(float(row.split('    ')[1]))
        foilfile.close()
        x,y = [float(i)*chord for i in x][::-1],[float(i)*chord for i in y][::-1]
    peri,area = polyPeri(x,y),polyArea(x,y)
    max_thickness = max([(abs(y[ind]-y[360-ind])) for ind in range(180)])
    plt.figure(figsize=(9,4),dpi=100)
    plt.plot(x,y,'b',[chord*-0.1,chord*1.1],[0,0],'--k')
    plt.axis('equal')
    plt.xlim([chord*-0.1,chord*1.1])
    plt.text(0,chord*-0.2,'Perimeter = %6.5f\nArea = %6.5f\nMax Thickness = %6.5f'%(peri,area,max_thickness))
    plt.savefig('Airfoil Geometry')
    plt.clf()
    return peri,area,max_thickness

def full_analysis():
    xf = XFPype_indepth(latest_airfoil,Ncrit,Re)
    alist = xf.alpha_float    
    data = logPlots(latest_airfoil,alist)
    alpha,cl,cd,ld,cm = zip(*data)
    def plot_polar(xx,yy,title,xax,yax,maxY = False,minY = False):
        plt.plot(xx,yy)
        plt.title(title)
        plt.xlabel(xax)
        plt.ylabel(yax)
        if maxY:
            maxY = max(yy)
            maxX = xx[yy.index(maxY)]
            plt.axhline(maxY,color = 'k',linestyle = '--',label = 'Maximum Cl/Cd = %6.5f'%maxY)
            plt.axvline(maxX,color = 'k',linestyle = '--',label = 'At Alpha = %4.3f'%maxX)
            plt.legend(loc = 'lower center')
            return maxX,maxY
        if minY:
            minY = min(yy)
            minX = xx[yy.index(minY)]
            plt.axvline(minX,color = 'k',linestyle = '--',label = 'Minimum Cd = %6.5f'%minY)
            plt.legend(loc = 'upper center')
            return minY
        return None
        
    alphaAtmax,maxLD = plot_polar(alpha,ld,'Cl over Cd vs Alpha','Alpha [deg]','Cl/Cd',maxY = True)
    plt.savefig('LD vs alpha')
    plt.clf()

    Cdmin = plot_polar(alpha,cd,'Cd vs Alpha','Alpha [deg]','Cd',minY = True)
    plt.savefig('Cd vs alpha')
    plt.clf()

    plot_polar(alpha,cl,'Cl vs Alpha','Alpha [deg]','Cl')
    plt.savefig('Cl vs alpha')
    plt.clf()

    plot_polar(alpha,cm,'Cm vs Alpha','Alpha [deg]','Cm')
    plt.savefig('Cm vs alpha')
    plt.clf()

    plot_polar(cd,cl,'Cl vs Cd','Cd','Cl')
    plt.savefig('Cl vs Cd')
    plt.clf()
    return None



if __name__ == '__main__':
    convergence_history()
    full_analysis()
    airfoil_properties(chord = 5.5)
