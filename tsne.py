#!/bin/env python
import os
import time
import argparse
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.manifold import TSNE
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if __name__=='__main__':
    #tsne prepare
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', '-d', type=str, default='rdata.npy',
                        help='raw data')
    parser.add_argument('--feature', '-f', type=str, default='result/feature.npy',
                        help='deep feature')
    parser.add_argument('--output', '-o', type=str, default='output.npy',
                        help='output of t-SNE')
    parser.add_argument('--seed', '-s', type=int, default=0,
                        help='random seed')
    args = parser.parse_args()

    starttime=time.time()

    data_d = np.load(args.feature, mmap_mode='r')
    data_d = data_d.reshape((-1, data_d.shape[0]))
    scaler_d = StandardScaler().fit(data_d)
    data_d = scaler_d.transform(data_d)
    data_d = data_d.reshape((data_d.shape[-1],-1))

    data_r = np.load(args.data, mmap_mode='r')
    data_r = data_r.reshape((data_r.shape[0],-1))
    print('shape of feature: ' + str(data_d.shape))
    print('shape of data: ' + str(data_r.shape))

    data_t = np.memmap('input.dat', dtype='float32', mode='w+', shape=(data_d.shape[0], data_r.shape[1]+data_d.shape[1]))
    data_t = np.hstack((data_r, data_d))
    print('shape of t-SNE input: ' + str(data_t.shape))
    np.save("input.npy", data_t)
    os.remove("input.dat")

    endtime=time.time()
    print('time spent for t-SNE_prepare: ', endtime-starttime)
    print('t-SNE running')
    
    #tsne running
    starttime=time.time()

    np.random.seed(args.seed)
    data_t = np.load(args.input, mmap_mode='r')
    tsne=TSNE(n_components=2)
    X=tsne.fit_transform(data_t)
    np.save(args.output, X) # output of t-sne

    plt.figure()
    plt.scatter(X[:, 0], X[:, 1])
    plt.title('t-SNE')
    plt.xlabel('RC1')
    plt.ylabel('RC2')
    plt.savefig("tsne.png") # save figure

    endtime=time.time()
    print('time:',endtime-starttime)
