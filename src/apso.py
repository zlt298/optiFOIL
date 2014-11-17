"""
Generalized Accelerated Particle Swarm Optimization Module
-APSO allows for optimization of bound-constrained problems

Code is based off of Xin-She Yang, "Nature-Inspired Metaheuristic Algorithms",
Second Edition, Luniver Press, (2010).   www.luniver.com

Nelson, J. (2014)
jn2345@hawaii.edu
"""
import os,csv
import numpy as np
from numpy.random import randn, rand

#---------------------------------------------------------------------------------------------------
#swarm class========================================================================================
#---------------------------------------------------------------------------------------------------
class Swarm(object):
    """
    Each particle swarm is associated with a single evaluation function, default bounds on all input
    parameters, and an arbitrary number of particles. The step evaluation of the parameter vector is:
    
    x_1 = (1-beta)*x_0 + beta * global_best + alpha * epsilon
    beta is the coefficient of determinant behavior (Particles move towards global best) 0<beta<1
    alpha is the coefficient of stochastic behavior (Particles explore randomly) 0<alpha<1
        alpha = alpha_0 * gamma^t
    
    Instantiation:
    eval_function  - Evaluation function that returns a hueristic score when evaluated for parameters
    bounds         - A list of tuple boundaries (Inclusive) for each input parameter of the evaluation
                     [(lower bound 1,upper bound 1),(lower bound 2,upper bound 2),...]
    particle_count - Number of particles to instantiate with
    seed           - An arbitrary number of lists of initial positions to seed your swarm with
    """        
    def __init__(self, eval_function, bounds, particle_count, seed = None, log_results = False):
        """
        Note that the swarm will be evaluated once upon instantiation, if the evaluation function
        is cpu time intensive, consider instantiating with no initial particles.
        """
        self.eval_function  = eval_function
        self.bounds         = bounds
        self.particle_count = particle_count
        self.logfile        = self.create_logfile() if log_results else False
        
        #default control parameters (can be changed with set_control_param())
        self.beta           = 0.5 #Deterministic Behavior Coefficient
        self.gamma          = 0.7 #Stochistic Behavior Decay Coefficient
        self.alpha_0        = 1.  #Stochistic Behavior Coefficient

        #System Variables
        self.t              = 0   #Iteration Step Count
        self.particles      = [Particle(eval_function,bounds) for i in range(self.particle_count)]
        for vector in seed if seed else []:
            self.particles.append(Particle(eval_function,bounds,vector))
        self.global_best    = self.evaluate_swarm()

    def __del__(self):
        """Cleanup"""
        if self.logfile: self.logfile.close()
    
    def set_control_param(self,alpha_0 = 1,beta = 0.5, gamma = 0.7):
        """Change the control parameters of the swarm"""
        self.beta           = beta
        self.gamma          = gamma
        self.alpha_0        = alpha_0

    def create_logfile(self):
        """
        Create a logfile with the naming scheme 000X.apso; Log inputs will be:
        param1,param2,param3,...;evaluation  <Gene 1>
        param1,param2,param3,...;evaluation  <Gene 2>
        etc...
        """
        try:
            filecount = max([ int(f.split('.')[0]) for f in os.listdir(".") if f.endswith(".apso")])
        except (ValueError):
            filecount = -1
        return open("%04.i.apso"%(filecount+1),'w')

    def seed_from_log(self,log_name,seeds_from_end):
        """
        Seed the current swarm with particles from *log_name*.apso
        Start with the gene at the last line, and count backwards to seeds_from_end
        Reevaluate the swarm after appending
        """
        seedlist = []
        with open('%s.apso'%log_name, 'r') as seed_log:
            for line in seed_log:
                try:
                    seedlist.append([float(x) for x in line.split(";")[0].split(",")])
                except Exception as e:
                    print e
        for vector in seedlist[::-1][:seeds_from_end]:
            self.particles.append(Particle(self.eval_function,self.bounds,vector))
        self.global_best = self.evaluate_swarm()

    def evaluate_swarm(self):
        """
        Iterate through the particles in the swarm and evaluate at each position.
        Write the positions and evaluation results to the log file and
        return the set of parameters with the  highest evaluation function result
        """
        positions = []
        for p in self.particles:
            positions.append(p.eval_pos())
            if self.logfile:
                s = ','.join(str(val) for val in positions[-1][:-1])+ ";" + str(positions[-1][-1])
                self.logfile.write(s+"\n")
        try:
            return np.array(max(positions,key = lambda x: x[-1])[:-1])
        except (ValueError):
            return None

    def iterate(self,n):
        """Iterate the swarm by n steps"""
        for _ in range(n):
            for p in self.particles:
                p.step(self.global_best,(self.alpha_0 * pow(self.gamma,self.t),self.beta))
            self.t = self.t + 1
            self.global_best = self.evaluate_swarm()

    def update_bounds(self,bounds):
        """Update parameter boundaries for all of the particles in the swarm."""
        self.bounds = bounds
        for p in self.particles:
            p.update_bounds(self.bounds)

    def update_eval(self,eval_function):
        """Update the evaluation function for all of the particles in the swarm."""
        self.eval_function = eval_function
        for p in self.particles:
            p.update_eval(self.eval_function)

    def get_best(self):
        """Returns the position and evaluation of the current best position"""
        return self.global_best,self.eval_function(*self.global_best)
            

#---------------------------------------------------------------------------------------------------
#Particle class=====================================================================================
#---------------------------------------------------------------------------------------------------
class Particle(Swarm):
    """
    Each Particle is associated with a single evaluation function, default bounds on all input
    parameters, and an optional fixed position.
    """
    def __init__(self, eval_function, bounds, starting_position = None):
        self.eval_function  = eval_function
        self.bounds         = bounds
        self.nparam         = len(self.bounds)
        self.lb             = np.array([i[0] for i in self.bounds])
        self.ub             = np.array([i[1] for i in self.bounds])
        self.r              = self.ub - self.lb

        if starting_position: #If seeded Particle
            self.position   = np.array(starting_position)
        else:                 #If unseeded Particle
            temp            = (rand(1,self.nparam))[0]
            self.position   = self.lb + np.multiply(temp,self.r)
        self.fix_bound()

        self.prevposition   = self.position
        self.eval           = 0

    def __del__(self): pass #Overwrite parent

    def fix_bound(self):
        """Correct parameters that are above or below their respective boundaries."""
        for ind in range(self.nparam):
            if self.position[ind] > self.ub[ind]:
                self.position[ind] = self.ub[ind]
            if self.position[ind] < self.lb[ind]:
                self.position[ind] = self.lb[ind]

    def eval_pos(self):
        """Run the evaluation function and return the current position and result"""
        self.eval = self.eval_function(*self.position)
        return np.append(self.position,self.eval)
    
    def step(self,global_best,control_param):
        """Take an iterative step"""
        self.prevposition = self.position
        alpha,beta = control_param
        epsilon = randn(1,self.nparam)[0]

        self.position = (1-beta)*self.prevposition + beta*global_best + alpha * epsilon
        self.fix_bound()
    
#---------------------------------------------------------------------------------------------------
#test functions=====================================================================================
#---------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    #1-d case with seed
    test_function = lambda x: -2*x*x + 5*x - 4 #solution at x = 1.25
    s = Swarm(test_function,[(-100,100)],5,seed = [[1],[1.2],[1.5]])
    s.iterate(1000)
    print s.get_best()
    
    #2-d case
    test_function = lambda x,y: -((x*x/16.0)+(y*y/25.0)) + 10 + 0.25*x+.08*y  #solution at x = 2,y=1
    s = Swarm(test_function,[(-800,500),(-500,1000)],50)
    s.iterate(50)
    print s.get_best()

##    #multimodal Test Case: Rastrigin's Function (n parameters)
##        #http://en.wikipedia.org/wiki/Rastrigin_function
##    from math import cos,pi
##    def rastrigin(*args):
##        x = args
##        n = len(x)
##        val = 10*n+sum([pow(xi,2) - 10*cos(2*pi*xi) for xi in x])
##        return -val
##    test_function = rastrigin  #solution at f(0,...0) = 0
##
##    #Log results of one swarm, reload the final 100 gene's in a new swarm and reevaluate
##    s = Swarm(test_function,[(-5.12,5.12),(-5.12,5.12),(-5.12,5.12),(-5.12,5.12)],10000,log_results = True)
##    s.iterate(50)
##    del s
##    s = Swarm(test_function,[(-5.12,5.12),(-5.12,5.12),(-5.12,5.12),(-5.12,5.12)],0)
##    s.set_control_param(alpha_0 = 0.01)
##    s.seed_from_log('0000',100)
##    s.iterate(100)
##    print s.get_best()
