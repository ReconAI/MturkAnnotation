# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 21:04:13 2020

@author: kompich
"""

import pandas as pd
#import boto3

from PIL import Image
import cv2
from io import BytesIO
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json 

def IndexAdd(v_index,v_length):
    v_index = v_index + 1
    if (v_index>=v_length):
        v_index = 0
    return v_index

def IndexSub(v_index,v_length):
    v_index = v_index - 1
    if (v_index<0):
        v_index = v_length - 1
    return v_index

color_pallete = {
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


df = pd.read_csv('AMTAssignment/Redone.csv') #Batch_3998716_batch_results.csv

df['CVApproval'] = 0

INDEX = 0
LENGTH = len(df)
alpha = 0.4


while(True):
    v_row = df.iloc[INDEX]
    
    v_url = v_row['Input.image_url']
    v_annotation = v_row['Answer.annotatedResult.boundingBoxes']

    resp = requests.get(v_url, stream=True).raw
    v_image = np.asarray(bytearray(resp.read()), dtype="uint8")
    v_image = cv2.imdecode(v_image, cv2.IMREAD_COLOR)
    ground = v_image.copy()
    
    h, w, c = v_image.shape

    json_annotation = json.loads(v_annotation)

    for bbox in json_annotation:
        v_label = bbox['label']
        v_height = bbox['height']
        v_width = bbox['width']
        v_left = bbox['left']
        v_top = bbox['top']
        
        color = (0, 255, 0) #BGR
        fontColor = (255, 255, 255) #BGR
        thickness = -1
        
        cv2.rectangle(v_image, (v_left,v_top), (v_left+v_width,v_top+v_height), color_pallete[v_label], thickness) 
        #cv2.putText(v_image,v_label, (v_left,v_top), cv2.FONT_HERSHEY_SIMPLEX, 0.6,fontColor,2)
    
    cv2.putText(v_image,str(INDEX), (0,h), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 255, 255),1)
    
    image_new = cv2.addWeighted(v_image, alpha, ground, 1 - alpha, 0)
    
    cv2.imshow('image',image_new)
    
    if cv2.waitKey(0) & 0xFF == ord('a'):
        #Iterate left <<
        print('A button pressed <<. Press 2 more times')
        INDEX = IndexSub(INDEX,LENGTH)
        
    if cv2.waitKey(0) & 0xFF == ord('d'):
        #Iterate right >>
        print('D button pressed >>. Press 2 more times')
        INDEX = IndexAdd(INDEX,LENGTH)
        
    
    if cv2.waitKey(0) & 0xFF == ord('w'):
        #good annotation
        print('W button pressed. Good annotation.')
        df.at[INDEX, 'CVApproval'] = 1
        INDEX = IndexAdd(INDEX,LENGTH)
        
    if cv2.waitKey(0) & 0xFF == ord('s'): 
        #good annotation
        print('S button pressed. Bad annotation.')
        df.at[INDEX, 'CVApproval'] = -1
        INDEX = IndexAdd(INDEX,LENGTH)
        
    if cv2.waitKey(0) & 0xFF == ord('q'):
        print('Q button pressed. Exiting...')
        break
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
cv2.destroyAllWindows()
df.to_csv('AMTAssignment/Batch_3998716_batch_results_reviewed.csv')
