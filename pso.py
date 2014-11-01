#Jeff's Implementation of a generalized Particle Swarm Optimization algorithm
"""
A particle swarm optimization module.
"""

import numpy as np
from numpy.random import randn, rand

#---------------------------------------------------------------------------------------------------
#particle class=====================================================================================
#---------------------------------------------------------------------------------------------------
class particle():
    """
    Instance of a particle
    stores position, evaluates and takes a step
    """
    def __init__(self, eval_function, bounds):
        self.eval_function = eval_function
        self.bounds = bounds
        self.nparam = len(self.bounds)
        self.lb = np.array([i[0] for i in self.bounds])
        self.ub = np.array([i[1] for i in self.bounds])
        self.r = self.ub - self.lb
        temp = (rand(1,self.nparam))[0]
        self.position = self.lb + np.multiply(temp,self.r)
        self.fix_bound()

        self.prevposition = self.position
        self.eval = 0

    def fix_bound(self):
        for ind in range(self.nparam):
            if self.position[ind] > self.ub[ind]:
                self.position[ind] = self.ub[ind]
            if self.position[ind] < self.lb[ind]:
                self.position[ind] = self.lb[ind]
            
    def eval_pos(self):
        #print 'position: ' + str(self.position)
        #print 'eval: ' + str(self.eval_function(*self.position))
        self.eval = self.eval_function(*self.position)
        np.append(self.position,self.eval)
        return np.append(self.position,self.eval)
    
    def step(self,global_best,control_param):
        self.prevposition = self.position
        alpha,beta = control_param
        epsilon = randn(1,self.nparam)[0]

        self.position = (1-beta)*self.prevposition + beta*global_best + alpha * epsilon
        self.fix_bound()

    def update_bounds(self,bounds):
        self.bounds = bounds

    def update_eval(self,eval_function):
        self.eval_function = eval_function
        
#---------------------------------------------------------------------------------------------------
#swarm class========================================================================================
#---------------------------------------------------------------------------------------------------
class swarm():
    """
    Create and Iterate a particle swarm
    x_1 = (1-Beta)*x_0 + Beta * global_best + alpha * epsilon

    Instantiation:
    eval_function - Evaluation function that returns a hueristic score when evaluated for parameters
    bounds - a list of tuple boundaries for each input parameter of the evaluation function [(lb1,ub1),(lb2,ub2),...]
    particle_count - number of particles to instantiate with

    Functions:
    set_control_param - alter the default control parameters to change convergence behavior
    __init__ - initialize the swarm
    iterate(N) - take N time steps
    get_best - return the position of the current global best
    converge(epsilon) - iterate until all (x_t+1 - x_t) < epsilon where x is normalized to the solution space
    """        
    def __init__(self, eval_function, bounds, particle_count):
        """
        Initialize a particle swarm
        """
        self.eval_function = eval_function
        self.bounds = bounds
        self.particle_count = particle_count
        
        #default control parameters (can be changed with set_control_param())
        self.beta = 0.5
        self.gamma = 0.7
        self.alpha_0 = 1
        
        self.t = 0
        self.particles = [particle(eval_function,bounds) for i in range(self.particle_count)]
        self.global_best = self.get_best()
    

    def set_control_param(bounds,alpha_0 = 1,beta = 0.5, gamma = 0.7):
        """
        beta = deterministic behavior coefficient (1-0)
        alpha = Stochastic behavior coefficients vector(1-0)
        gamma = Stochastic decay coefficient

        alpha = alpha_0*gamma^t  (t is iteration)
        """
        self.beta = beta
        self.gamma = gamma
        self.alpha_0 = alpha_0

    def get_best(self):
        pos = []
        for i in self.particles:
            pos.append(i.eval_pos())
        return np.array(max(pos,key = lambda x: x[-1])[:-1])

    def iterate(self,n):
        for _ in range(n):
            for p in self.particles:
                p.step(self.global_best,(self.alpha_0 * pow(self.gamma,self.t),self.beta))
            self.t = self.t + 1
            self.global_best = self.get_best()

    def update_bounds(self,bounds):
        self.bounds = bounds
        for p in self.particles:
            p.update_bounds(self.bounds)

    def update_eval(self,eval_function):
        self.eval_function = eval_function
        for p in self.particles:
            p.update_eval(self.eval_function)
        
#---------------------------------------------------------------------------------------------------
#test functions=====================================================================================
#---------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    #1-d case
    test_function = lambda x: -2*x*x + 5*x - 4 #solution at x = 1.25
    s = swarm(test_function,[(-100,100)],20)
    s.iterate(1000)
    print s.get_best()
    
    #2-d case
    test_function = lambda x,y: -((x*x/16.0)+(y*y/25.0)) + 10 + 0.25*x+.08*y  #solution at x = 2,y=1
    s = swarm(test_function,[(-800,500),(-500,1000)],50)
    s.iterate(50)
    print s.get_best()

    #multimodal Test Case: Rastrigin's Function (n parameters)
        #http://en.wikipedia.org/wiki/Rastrigin_function
    from math import cos,pi
    def rastrigin(*args):
        x = args
        n = len(x)
        val = 10*n+sum([pow(xi,2) - 10*cos(2*pi*xi) for xi in x])
        return -val
    test_function = rastrigin  #solution at f(0,...0) = 0
    s = swarm(test_function,[(-5.12,5.12)],1000)#,(-5.12,5.12),(-5.12,5.12),(-5.12,5.12)],10000)
    s.iterate(2000)
    print s.get_best()
