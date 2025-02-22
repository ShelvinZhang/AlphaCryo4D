#!/bin/env python

import os
import argparse
import time
import mrcfile as mf
import numpy as np
from sklearn.preprocessing import StandardScaler


if __name__ == '__main__':
    starttime = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', '-f', type=str, default='./maps/',
                        help='folder of maps')
    args = parser.parse_args()
    path = args.folder # the folder of maps

    pwd = os.getcwd()
    print(pwd)
    
    try:
        os.remove(pwd + '/data.log')
    except:
        pass

    try:
        os.remove(pwd + '/num.txt')
    except:
        pass
    
    files = list(filter(lambda f: os.path.splitext(f)[1] == '.mrc', os.listdir(path)))
    os.chdir(path)
    with mf.open(files[0], mode='r') as mrc:
        n = mrc.data.shape[0] # box size of maps
    fp = np.memmap(pwd + '/rdata.dat', dtype='float32', mode='w+', shape=(len(files), n**3))
    fp3d = np.memmap(pwd + '/rdata_3d.dat', dtype='float32', mode='w+', shape=(len(files), n, n, n))

    for n,file in enumerate(files):
        if os.path.isfile(file):
            print(n,file)
            mrc = mf.mrcfile.MrcFile(file,mode='r')
            nmrc = mrc.data
            nmrc3d = nmrc.copy()
            nmrc3d -= nmrc3d.mean()
            nmrc3d /= nmrc3d.std()
            nmrc3d = (nmrc3d-nmrc3d.min())/(nmrc3d.max()-nmrc3d.min())
            fp3d[n] = nmrc3d
            nmrc=np.reshape(nmrc,(-1,1))
            scaler = StandardScaler().fit(nmrc) # normalization
            nmrc_norm = np.ravel(scaler.transform(nmrc))
            fp[n] = nmrc_norm
            with open(pwd + '/data.log', mode='a+') as f:
                f.write('%d %s\n' % (n+1, file))
            with open(pwd + '/num.txt', mode='a+') as num:
                total = 0
                with open(pwd + '/stars/' + file.strip('.mrc') + '.star') as star:
                    for line in star.readlines():
                        if "mrcs" in line:
                            total = total + 1
                num.write('%d\n' % total )

    os.chdir(pwd)
    np.save('data_dl.npy', fp3d) # output npy file
    np.save('rdata.npy', fp)
    os.remove('rdata.dat')
    os.remove('rdata_3d.dat')
    
    endtime=time.time()
    print('time spent:', endtime-starttime)
