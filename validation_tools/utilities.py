# -*- coding: utf-8 -*-
"""
Group of methods to manage images
"""

import cv2
import numpy as np
import json
import requests
import boto3
import pandas as pd
import os
from tqdm import tqdm

from credentials import *

IMAGE_LINK_HEADER = 'https://reconai-traffic.s3.eu-central-1.amazonaws.com/'

COLOR_PALLETE = {
    "Car": (44,160,44), 
    "Van": (179,119,30), 
    "Truck": (14,126,254),  
    "Trailer": (40,39,213), 
    "Bus": (188,103,148),
    "Motorbike": (76,82,142),
    "Bicycle": (194,119,227),
    "Heavy Equipment": (129,126,123),
    "Car Trailer": (34,189,188),
    "Tractor": (149,151,254),
    "Pedestrian": (207,188,21)
    }

alpha = 0.4

## Draw annotation on top of the image
## annotation format: [{height:16,label:'Car',left:343,top:170,width:24},{height:8,label:'Car',left:92,top:117,width:10},...]
def drawAnnotation(p_image, p_annotation):
    ground = p_image.copy()
    h, w, c = p_image.shape
    
    for bbox in p_annotation:
        v_label = bbox['label']
        v_height = bbox['height']
        v_width = bbox['width']
        v_left = bbox['left']
        v_top = bbox['top']
        
        cv2.rectangle(p_image, (v_left,v_top), (v_left+v_width,v_top+v_height), COLOR_PALLETE[v_label], -1) 
        cv2.rectangle(ground, (v_left,v_top), (v_left+v_width,v_top+v_height), COLOR_PALLETE[v_label], 2)
    
    return cv2.addWeighted(p_image, alpha, ground, 1 - alpha, 0)

# Input - raw MturkAnnotation text
# Output - json as text which wouldn't crash on json.loads()
def fixAnnotationText(p_annotation):
    p_annotation = p_annotation.replace("\'", "\"")
    p_annotation = p_annotation.replace("},}", "}}")
    p_annotation = p_annotation.replace("value", "\"value\"")
    p_annotation = p_annotation.replace("labels:", "\"labels\":")
    p_annotation = p_annotation.replace("height", "\"height\"")
    p_annotation = p_annotation.replace("label:", "\"label\":")
    p_annotation = p_annotation.replace("left", "\"left\"")
    p_annotation = p_annotation.replace("top", "\"top\"")
    p_annotation = p_annotation.replace("width", "\"width\"")
    
    return p_annotation

## Read the image by the link, parse annotation
## Return - image and annotation
def processImage(p_image_url, p_annotation):
    
    v_response = requests.get(p_image_url, stream=True).raw
    v_image = np.asarray(bytearray(v_response.read()), dtype="uint8")
    v_image = cv2.imdecode(v_image, cv2.IMREAD_COLOR)
    p_annotation = fixAnnotationText(p_annotation)
    v_raw_annotation = json.loads(p_annotation)
    v_annotation_bboxes = v_raw_annotation['boundingBox']['value']
    
    return v_image, v_annotation_bboxes

## image list sharing method
# p_publish = True - publish images
# p_publish = False- make images private

def s3ImageSharing(p_image_url_list, p_publish = True):
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
    
    s3 = session.resource('s3')
    bucket = s3.Bucket(AWS_BUCKET_NAME)    
    
    v_ACL='public-read'
    if (not p_publish):
        v_ACL='private'
    
    for img_path in tqdm(p_image_url_list):
        for s3_file in bucket.objects.filter(Prefix=img_path):
            object_acl = s3.ObjectAcl(AWS_BUCKET_NAME,s3_file.key)
            response = object_acl.put(ACL=v_ACL)
        
    print('OK',v_ACL)
     
## make image public using boto3
def makeImagesPrivate(p_image_url_list):
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
    
    s3 = session.resource('s3')
    bucket = s3.Bucket(AWS_BUCKET_NAME)
    
    for img_path in tqdm(p_image_url_list):
        for s3_file in bucket.objects.filter(Prefix=img_path):
            object_acl = s3.ObjectAcl(AWS_BUCKET_NAME,s3_file.key)
            response = object_acl.put(ACL='private')
    
    return 'private:OK'

# test call for Dataset.csv - like file
# structure:
## image_url, annotation, threadNum, isAnnotated
if __name__ == '__main__':
    
    DATA_SAVE_FOLDER = 'annotated_images'
    
    #read dataset
    DATASET_FOLDER = 'data'
    df = pd.read_csv(os.path.join(DATASET_FOLDER,'test_dataset.csv'))
    
    #filter isAnntated=True
    filter_df = df['isAnnotated'] == True
    annotated_df = df.loc[filter_df,['image_url','annotation']]
    
    #take SAMPLE_SIZE random rows from the dataset
    SAMPLE_SIZE = 100
    annotated_df_sample = annotated_df.sample(n = SAMPLE_SIZE)
    
    print('image publish started')
    url_list = annotated_df_sample['image_url'].tolist()
    s3ImageSharing(url_list)
    
    annotated_df_sample['image_name'] = annotated_df_sample['image_url'].apply(lambda x: x.split('/')[1])
    annotated_df_sample['image_name'] = annotated_df_sample['image_name'].apply(lambda x: x.split('.')[0]) + '.png'
    annotated_df_sample['image_url'] = IMAGE_LINK_HEADER +  annotated_df_sample['image_url']
    
    print('image drawing started')
    for index, row in tqdm(annotated_df_sample.iterrows()):
        row_image, row_annotation_bboxes = processImage(row['image_url'], row['annotation'])
        row_annotated_image = drawAnnotation(row_image, row_annotation_bboxes)
        
        row_image_path = os.path.join(DATA_SAVE_FOLDER,row['image_name'])
        cv2.imwrite(row_image_path, row_annotated_image)
     
    print('image privatization started')
    s3ImageSharing(url_list,False)
    print('Done')

    
    
    
    
        



    
  

    
    
  

