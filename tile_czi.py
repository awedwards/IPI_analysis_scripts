#!/usr/bin/env python
# coding: utf-8

from aicspylibczi import CziFile
import numpy as np
from numpy import random as rd
import tifffile as tf
from pathlib import Path

from matplotlib import pyplot as plt

import sys, os
import re

#rootdir = "/media/austin/DrosophilaMelanogaster/IPI/8plex/Brightfield/"
#files = Path(rootdir).glob("*czi")
#files = ["CRC 72 BF.czi"]

files = sys.argv[1:]

#channels = ['DAPI','FoxP3','CD4','CD45','CD8']
channels = ['DAPI','HLADR','CD8','CD163','CD4','XCR1','CD3','PDL1','PanCK']
#channels = ['DAPI','HLADR','CD8','CD163','CD4','XCR1','CD3','PDL1','EPCAM'] # only for CRC

if sys.argv[-1] == 'bf':
    is_bf = True
    files = files[:-1]
else:
    is_bf = False

if is_bf:
    channels=['Brightfield']
    
tile_size = 2048

for f in files:
    
    f = Path(f)
    czi = CziFile(f)
    im_shape = czi.get_dims_shape()
    
    if not is_bf:
        
        nchannels = im_shape[0]['C'][1]
        assert(len(channels)==nchannels)
    elif is_bf:
        
        nchannels = 1
    
    name = re.match("IPI[A-Z]*[0-9]*",f.stem)[0]
    expdir = Path(os.path.curdir, name)

    try:
        Path.mkdir(expdir)
    except FileExistsError: pass

    print("Reading " + f.name)

    for c in np.arange(nchannels):
        
        fov = 0
        print("Reading " + channels[c] + " channel")    
        im = czi.read_mosaic(C=c)
        
        if is_bf:
            _,w,h,rgb = im.shape
        else:
            _,w,h = im.shape

        rows = list(np.arange(0,w,tile_size))
        cols = list(np.arange(0,h,tile_size))
        

        for x in rows:

            if w-x < tile_size:
                x_end = w
            else:
                x_end = x+tile_size

            for y in cols:
                
                
                # create empty tile, useful for padding out incomplete tiles at the edges with zeros

                if is_bf:
                    tile = np.zeros((tile_size, tile_size, 3))
                else:
                    tile = np.zeros((tile_size, tile_size))

                if h-y < tile_size:
                    y_end = h
                else:
                    y_end = y+tile_size
                    
                if is_bf:
                    tile[0:x_end-x, 0:y_end-y,:] = im[0, x:x_end, y:y_end,:]
                else:
                    tile[0:x_end-x, 0:y_end-y] = im[0, x:x_end, y:y_end]


                savedir = Path(expdir, 'fov' + str(fov))

                try:
                    Path.mkdir(savedir)
                except FileExistsError:
                    pass
                
                tf.imsave(str(Path(savedir, channels[c] + ".tiff")), tile)

                if c==0:
                    with open(Path(expdir, "tile_metadata.txt"), "a") as f:
                        f.write(",".join(["fov" + str(fov), str(x), str(x_end), str(y), str(y_end)]) + "\n")

                fov += 1
