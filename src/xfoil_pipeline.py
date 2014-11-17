import subprocess as sp
import os,string
from threading import Thread

class XFPype(object):
    """
    XFoil Pipeline Object
    Provides functions for running XFOIL commands through python
    
    
    """
    
    xfoilpath = r'..\bin\xfoil.exe'
    
    def __init__(self, name, Ncrit, Re, set_alpha = (1,4,1), mthread = False):
        """
        name        = name of dat file as string (without the .dat)
        Ncrit       = Parameter that defines the quality of the boundary layer (See Xfoil documentation for details)
        Re          = Reynolds Number
        set_alpha   = Tuple with (start,end,step) alpha range (all as integers)
        mthread     = enable/disable multithreading

        The calculations will be run on initialization, and the output will be spitout to a logfile (name.log)
        """
        self.set_alpha(*set_alpha)

        if mthread: #Multithreading option
            procs = []
            threads = []
            for ind,alpha in enumerate(self.alpha_list):
                procs.append(sp.Popen(self.xfoilpath ,stdin=sp.PIPE,stderr=sp.PIPE,stdout=sp.PIPE))
                def f():
                    self.run_analysis(procs[-1],name,Ncrit,Re,alpha)
                t = Thread(target=f)
                t.daemon = True
                t.start()
                threads.append(t)
            [t.join() for t in threads]
        else:
            process = sp.Popen(self.xfoilpath ,stdin=sp.PIPE,stderr=sp.PIPE,stdout=sp.PIPE)
            self.run_analysis(process,name,Ncrit,Re,self.alpha)

    def set_alpha(self,start,stop,step):
        self.alpha_list = ['aseq %4.2f %4.2f 0.1'%(x-0.1,x) for x in range(start,stop+step,step)]
        self.alpha_count = len(self.alpha_list)
        self.alpha = '\ninit\n'.join(self.alpha_list)
        return None
    
    def run_analysis(self,proc,name, Ncrit, Re, alpha):
        proc.stdin.write(r"load ..\airfoils\\"+name+'.dat'  +'\n')
        proc.stdin.write('OPER'                             +'\n')
        proc.stdin.write('Vpar'                             +'\n')
        proc.stdin.write('N %i'%Ncrit                       +'\n')
        proc.stdin.write(' '                                +'\n')
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

        
if __name__ == '__main__':
    #Test speed difference between single and multithreading
    #delete the log file before each run; comment out and only run one at a time for accurate results.
    #For 8 alpha angles:
        #single thread : 0.617s
        #8 threads     : 0.371s
    xf = XFPype('test',5,150000,mthread = False)
    
    import time
    tic = time.time()
    b = XFPype('test',5,150000,mthread = True)
    toc = time.time()
    print toc-tic
    
##    tic = time.time()
##    a = XFPype('test',5,150000)
##    toc = time.time()
##    print toc-tic
    
    
