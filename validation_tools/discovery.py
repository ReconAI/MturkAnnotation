# -*- coding: utf-8 -*-
"""
Set of utilities to discover and download Data Traffic Finland camera images
ToDo: test code
"""

import boto3
from tqdm import tqdm
import os

from credentials import *


#Go over S3 bucket and retrieve unique Camera IDs
def discoverCameraIDs():
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    
    s3 = session.resource('s3')
    v_bucket = s3.Bucket(AWS_BUCKET_NAME)
    
    SensorIDs = []
    
    # saved as 'images/C1458602'
    for s3_file in tqdm(v_bucket.objects.filter(Prefix='images/')): #all():
        key = s3_file.key.split('_')[0]
        
        if key not in SensorIDs:
            SensorIDs.append(key)
    
    print('SensorIds retrieved')
    return SensorIDs
    

# Download N images in assigned folder based on prefix
## Input params:
## p_prefix - prefix to search - 'images/C1458602'
## p_numImages - num images to retrieve - 5
## p_saveFolder - folder to save - 'images'
## p_createUniqueFolder - create unique folder per camera 'images/C1458602/...'
def downloadFilesByPrefix(p_prefix, p_numImages, p_saveFolder, p_createUniqueFolder=True):
    
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    
    s3 = session.resource('s3')
    reconai_bucket = s3.Bucket(AWS_BUCKET_NAME)
    
    common_save_path = p_saveFolder
    
    if (p_createUniqueFolder):
        #p_prefix = 'images/C1458602'
        v_foldername = p_prefix.split('/')[-1]
        common_save_path = os.path.join(common_save_path,v_foldername)
        os.mkdir(common_save_path)
        
    for s3_file in reconai_bucket.objects.filter(Prefix=p_prefix).limit(p_numImages):
        key = s3_file.key
        #key = images/C0150801_r0_w0_2020-03-15_19-57-12.jpg
        filename = key.split('/')[-1]
        path_to_save = os.path.join(common_save_path,filename)
        reconai_bucket.download_file(key, path_to_save)
        

if __name__ == '__main__':
    
    DATA_SAVE_FOLDER = 'data'
	IMAGES_SAVE_FOLDER = 'images'

    #retrieve sensors and save to a file    
    v_sensorIDs = discoverCameraIDs()    
    with open(os.path.join(DATA_SAVE_FOLDER,'UniqueSensors.txt'), 'w') as filehandle:
        for sensor in v_sensorIDs:
            filehandle.write('%s\n' % sensor)
            
    #read sensors file and save images to unique folders
    NUM_IMAGE_TO_RETRIEVE = 5
    with open(os.path.join(DATA_SAVE_FOLDER,'UniqueSensors.txt'), 'r') as filehandle:
        filecontents = filehandle.readlines()
        for SensorPrefix in tqdm(filecontents):
            downloadFilesByPrefix(SensorPrefix, NUM_IMAGE_TO_RETRIEVE, IMAGES_SAVE_FOLDER)
        
    