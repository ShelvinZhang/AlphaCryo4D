#!/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy import interpolate
from scipy import integrate

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--landscape', '-l', type=str, default='output.npy',
                        help='free energy landscape mapping by t-sne')
    parser.add_argument('--number', '-n', type=str, default='num.txt',
                        help='particle number file')
    parser.add_argument('--xrange', '-x', type=float, default=[-30,30],
                        help='maximum value of the reaction coordinate of free energy landscape')
    parser.add_argument('--yrange', '-y', type=float, default=[-45,20],
                        help='maximum value of the reaction coordinate of free energy landscape')
    parser.add_argument('--interpolate', '-I', type=str, default='linear',
                        help='interplotion method used in free energy landscape plotting, linear or cubic')
    args = parser.parse_args()

    # initialize
    lx=args.xrange
    ly=args.yrange
    grid_x, grid_y = np.mgrid[lx[0]:lx[1]:1000j, ly[0]:ly[1]:1000j]   # about from (-80,-80) to (80,80)
    print("range of free energy landscape: (" + str(lx) + str(ly) + ")")
    
    #free energy landscape
    k=1
    T=1
    x1 = np.load(args.landscape)
    z = np.loadtxt(args.number)

    sum_z = np.sum(z)
    z = z/sum_z
    g = -k*T*np.log(z)
    x2 = x1[0:,:]   # start from volume 0 to end
    if args.interpolate=='linear':
        Hfunc = interpolate.LinearNDInterpolator(x2, g)
    elif args.interpolate=='cubic':
        Hfunc = interpolate.CloughTocher2DInterpolator(x2, g)

    grid_z = Hfunc(grid_x, grid_y)
    
    # results
    plt.figure(figsize=(5,5))
    plt.imshow(grid_z.T,extent=[lx[0],lx[1],ly[0],ly[1]],origin="lower",cmap=plt.cm.Spectral_r)
    plt.colorbar()

    plt.scatter(x2[:,0],x2[:,1],c='g',s=0.1)
    #plt.scatter(x2[:,0],x2[:,1],c='g',s=z*100)
    for i in np.arange(x2.shape[0]):
        plt.annotate(i+1,(x2[i,0],x2[i,1]),fontsize=1)

    plt.savefig('el.pdf',format='pdf')
    plt.show()
