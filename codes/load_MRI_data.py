#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import os
import argparse
from skimage.io import imsave
import nibabel as nib

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_name", type=str, default='2', help="input directory nii datat to be extracted from")
    parser.add_argument("--datafolder", type=str, default='../data/sampleMRIdata', help="path to the dir_name")
    parser.add_argument("--modality", type=str, default='T2', help="which MRI modality to read?")
    parser.add_argument("--variant", type=int, default=1, help="variant:   1 - png,  2 - numpy")
    parser.add_argument("--dir_nameoutput", type=str, default='../data/mri_exported', help="output directory nii datat to be saved to")
    opt = parser.parse_args()
    #print(opt)
    variant = opt.variant
    dir_nameoutput = opt.dir_nameoutput 
    dir_name = opt.dir_name
    datafolder = opt.datafolder
    modality = opt.modality
    dir_sep = '/'

    # find th correct directory to read based on the given MRI modality
    lisOfDirs = os.listdir(datafolder + dir_sep + dir_name)
    for m in range(0, len(lisOfDirs)):
        if lisOfDirs[m].find(modality)!=-1:
            targetModality = lisOfDirs[m]
    
    #make the output location
    if not os.path.isdir(dir_nameoutput):
        os.mkdir(dir_nameoutput)
    if not os.path.isdir(dir_nameoutput + dir_sep + dir_name): 
        os.mkdir(dir_nameoutput + dir_sep + dir_name)
    if not os.path.isdir(dir_nameoutput + dir_sep + dir_name + dir_sep + targetModality):
        os.mkdir(dir_nameoutput + dir_sep + dir_name + dir_sep + targetModality)
    
            
    # load data
    filename = datafolder + dir_sep + dir_name + dir_sep +  targetModality  + dir_sep +  targetModality + '.nii'
    img = nib.load(filename)
    data_volume = img.get_fdata()                  
                    
    # iterate over all slices and save each slice with the target output format in the output directory
    for ss in range(0, data_volume.shape[2]):        
        image = np.rot90(data_volume[:,:,ss], -1)
        # used for numpy files                
        dict_data = {'image': image}
            
        filename_name = dir_nameoutput + dir_sep + dir_name + dir_sep + targetModality  + dir_sep + str(ss+1)
            
        # PNG
        if variant == 1:
            imsave(filename_name + '.png', image)
        # NUMPY
        elif variant == 2:
            np.save(filename_name + '.npy', dict_data)
        # else
        else:
            print('not supported format')  
            
    print('END OF EXPORTING MRI DATA')
            
    
    
