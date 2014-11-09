import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import apso

def rastrigin(*args):
    x = args
    n = len(x)
    val = 10*n+sum([pow(xi,2) - 10*np.cos(2*np.pi*xi) for xi in x])
    return -val


class AnimatedScatter(object):
    def __init__(self, numpoints=50):
        self.swarm = apso.Swarm(rastrigin,[(-5.12,5.12),(-5.12,5.12)],numpoints)
        self.swarm.set_control_param(beta = 0.1,alpha_0 = 0.7,gamma = 0.9)
        self.numpoints = numpoints
        self.stream = self.data_stream()
        self.angle = 0

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111,projection = '3d',azim = -45, elev = 70)
        x = np.linspace(-5.12,5.12,100)
        y = np.linspace(-5.12,5.12,100)
        X,Y = np.meshgrid(x,y)
        u = rastrigin(x[:,None],y[None,:])
        wire1 = self.ax.plot_surface(X,Y,u, rstride=1, cstride=1, cmap=cm.coolwarm,linewidth=0.01)
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=10, 
                                           init_func=self.setup_plot, blit=True,frames=200,)
    def setup_plot(self):
        #X = next(self.stream)
        data=np.zeros((len(self.swarm.particles),3))
        for ind,p in enumerate(self.swarm.particles):
            data[ind,:2] = p.position
            data[ind,2] = rastrigin(*p.position)+1
        self.scat = self.ax.scatter(data[:,0],data[:,1], data[:,2] , s=20, animated=True)

        return self.scat,

    def data_stream(self):
        data=np.zeros((len(self.swarm.particles),3))
        while True:
            data=np.zeros((len(self.swarm.particles),3))
            for ind,p in enumerate(self.swarm.particles):
                data[ind,:2] = p.position
                data[ind,2] = rastrigin(*p.position)+1
            self.swarm.iterate(1)
            yield data

    def update(self, i):
        data = next(self.stream)

        self.scat._offsets3d = ( data[:,0] , data[:,1] , data[:,2] )

        plt.draw()
        return self.scat,

    def show(self):
        plt.show()

if __name__ == '__main__':
    a = AnimatedScatter()
    a.show()
