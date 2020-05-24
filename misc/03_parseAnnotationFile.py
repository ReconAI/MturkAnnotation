# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 00:16:31 2020

@author: kompich
"""

import pandas as pd
import boto3

###########
##Variables
############

RoadTypeEnum = [3.0] #Highway
ImageTypeEnum = [0.0,1.0] #Analog, Digital
CarVisibleEnum = [0.0,1.0,2.0] #Multiple cars, Some cars, No cars
NUM_CAMERAS_TO_SAVE = 5
NUM_IMAGES_TO_SAVE = 10
bucketName = 'reconai-traffic'
sampleCamerasList = []
ImageLinks = []

################
###### Parse cameras dataset and pick 5 of each type (Road Type)x(Image Type)x(Number of cars)
###############

df = pd.read_csv('CamerasAnnotation.csv')

df.dropna(subset=['Width'], inplace=True) # Remove empty records


for v_roadType in RoadTypeEnum:
    for v_imgType in ImageTypeEnum:
        for v_carVisible in CarVisibleEnum:
            v_subset = df.loc[(df['RoadType'] == v_roadType) &
                              (df['CarsVisible'] == v_carVisible) &
                              (df['ImageType'] == v_imgType)]
            
            sampleCamerasList = sampleCamerasList + v_subset['Code'].tolist()[0:NUM_CAMERAS_TO_SAVE]
            
#print(sampleCamerasList)
#print(len(sampleCamerasList))

################
######Connect to AWS and discover top 10 images for each camera
###############

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3 = session.resource('s3')
reconai_bucket = s3.Bucket(bucketName)


for v_cameraName in sampleCamerasList:

    prefixFilter = 'images/' + v_cameraName
    
    for s3_file in reconai_bucket.objects.filter(Prefix=prefixFilter).limit(NUM_IMAGES_TO_SAVE):
        key = s3_file.key
        
        #Grant read access to files
        object_acl = s3.ObjectAcl('reconai-traffic',key)
        response = object_acl.put(ACL='public-read')
        
        #Prepare link for image
        link = 'https://reconai-traffic.s3.eu-central-1.amazonaws.com/' + key
        ImageLinks.append(link)
        
with open('linksDataset.txt','w') as f:
    f.write('\n'.join(ImageLinks))