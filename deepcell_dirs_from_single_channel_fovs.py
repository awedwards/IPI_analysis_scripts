#!/usr/bin/env python
# coding: utf-8

import re
from pathlib import Path
import shutil
from os import remove, rmdir
from sys import argv

def isempty(dir_path):
    # Checks a directory to see if it contains any files
    
    path = Path(dir_path)
    has_next = next(path.iterdir(), None)
    if has_next is None:
        return True
    return False

def create_dir(dir_path):
    # Create an empty directory at dir_path if it doesn't yet exist
    try:
        Path.mkdir(dir_path)
    except FileExistsError:
        if not isempty(input_dir):
            raise Exception('Directory ' +dir_path.name + ' is not empty.')


files = argv[1:]
#rootdir = "/media/austin/DrosophilaMelanogaster/IPI/8plex/data/"

exp_dirs = [Path(exp) for exp in files]

for exp in exp_dirs:
    fov_dirs = [fov for fov in Path(exp).iterdir() if fov.is_dir()]

    #Create required directory structure for DeepCell
    input_dir = Path(exp,"input_data")
    create_dir(input_dir)
    single_tiff_dir = Path(input_dir, "single_channel_inputs")
    create_dir(single_tiff_dir)
    mibitiff_dir = Path(input_dir, "mibitiff_inputs")
    create_dir(mibitiff_dir)
    deepcell_input_dir = Path(input_dir,"deepcell_input")
    create_dir(deepcell_input_dir)
    deepcell_output_dir = Path(exp, "deepcell_output")
    create_dir(deepcell_output_dir)

    for f in fov_dirs:

        res = re.match("fov\d+",f.name)[0]
        create_dir(Path(single_tiff_dir,res))

        tiff_dir = Path(single_tiff_dir,res,"TIFs")
        print(tiff_dir)
        create_dir(tiff_dir)

        tiffs = [im_file for im_file in Path(f).iterdir() if (im_file.name.endswith(".tif") or im_file.name.endswith(".tiff"))]

        for tf in tiffs:
            shutil.move(str(tf), str(Path(tiff_dir, tf.name)))

        rmdir(f)
