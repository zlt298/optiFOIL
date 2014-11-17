import numpy as np
from scipy.misc import comb

"""
Create airfoils according to the following parameterization:
Fit a bezier curve (courtesy of reptilicus
http://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy?rq=1
) to the following:

LEU    C20+T20  C40+T40  C60+T60  C80+T80
0.0      0.2      0.4      0.6      0.8      1.0
LED    C20-T20  C40-T40  C60-T60  C80-T80

Where gene is the list:
  0   1   2   3   4   5   6   7   8   9
[LEU,LED,C20,C40,C60,C80,T20,T40,T60,T80]
"""
def bernstein_poly(i, n, t):
    return comb(n, i) * ( t**(n-i) ) * (1 - t)**i

def bezier_curve(points, points_per_curve = 61):
    nPoints = len(points)
    xPoints = points[:,0]
    yPoints = points[:,1]

    t = np.linspace(0.0, 1.0, points_per_curve)
    polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])
    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals

def generate_airfoil(gene,name, points_per_curve = 61):
    xx = np.zeros((7,))
    xx[1:] = np.linspace(0,1,6)
    y_up = np.array([0.0,
                     gene[0],
                     gene[2] + gene[6],
                     gene[3] + gene[7],
                     gene[4] + gene[8],
                     gene[5] + gene[9],
                     0.0])
    y_dn = np.array([0.0,
                     -gene[1],
                     gene[2] - gene[6],
                     gene[3] - gene[7],
                     gene[4] - gene[8],
                     gene[5] - gene[9],
                     0.0])
    xy_up = np.vstack((xx[:],y_up)).transpose()
    xy_dn = np.vstack((xx[:],y_dn)).transpose()
    xy_up = bezier_curve(xy_up,points_per_curve)
    xy_dn = bezier_curve(xy_dn,points_per_curve)

    with open(r"..\airfoils\%s.dat"%name,'w') as foilfile:
        foilfile.write(name+"\n")
        for i in range (points_per_curve-1):
             foilfile.write(  " %1.6f    %1.6f\n" %(xy_up[0][i],xy_up[1][i]))
        for i in range (points_per_curve-1,-1,-1):
             foilfile.write(  " %1.6f    %1.6f\n" %(xy_dn[0][i],xy_dn[1][i]))
        foilfile.close()


if __name__ == '__main__':
    generate_airfoil([ 0.09976517,
                       0.02443823,
                       0.08003413,
                       0.07513678,
                       0.02698911,
                       0.08670379,
                       0.04765646,
                       0.045,
                       0.01539405,
                       0.015    ], 'test')
