#!/opt/anaconda3/bin/python

import os
import numpy
import glob
import  random 

ME_DIR = os.path.dirname(os.path.realpath(__file__))
BGN_DIR = os.path.join(ME_DIR, 'bgn')

ALTER_RATE = 0.6
RANDOM_GAIN = 0.2
BGN_GAIN = 0.2

def _getBgn(globstring):
    flist = glob.glob(globstring)
    i = random.randint(0, len(flist) - 1)
    f = flist[i]
    _, data = readWav(f)
    return data

def _uniformAlter(data):
    if random.random() < ALTER_RATE:
        noise = numpy.random.random(data.shape)
        noise = numpy.array(noise, dtype=numpy.float32)
        noise = noise - 0.5
        alpha = random.random() * RANDOM_GAIN
        data  = data + alpha * noise
    return data

def _sytheticAlter(data):
    if random.random() < ALTER_RATE:
        noise = _getBgn(os.path.join(BGN_DIR, '*.wav'))
        alpha = random.random() * BGN_GAIN
        if len(noise) < len(data):
            start = random.randint(0, len(data) - len(noise))
            data = (1 - alpha) * data[start:start + len(noise)] + alpha * noise
        else:
            start = random.randint(0, len(noise) - len(data))
            data = (1- alpha) * data + alpha * noise[start:start + len(data)]
    return data

def bgnAlter(data):
    data = _uniformAlter(data)
    #data = _sytheticAlter(data)
    return data

if __name__ == '__main__':
    spl, wav = readWav('./test.wav')
    wav = bgnAlter(wav)
    numpyToWav(wav, './noise.wav')
