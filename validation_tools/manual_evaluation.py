# -*- coding: utf-8 -*-
"""
Tool for manual evaluation
#ToDo: update original dataset

"""

import cv2
import numpy as np
import json
import requests
import boto3
import pandas as pd
import os
from tqdm import tqdm

from utilities import *
from credentials import *

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

if __name__ == '__main__':
    
    DATASET_FOLDER = 'data'
    df = pd.read_csv(os.path.join(DATASET_FOLDER,'test_dataset_evaluate.csv'))
    
    #filter isAnntated=True
    filter_df = df['isAnnotated'] == True
    annotated_df = df.loc[filter_df,['image_url','annotation']]
    
    print('image publish started')
    url_list = annotated_df['image_url'].tolist()
    s3ImageSharing(url_list)
    
    INDEX = 0
    LENGTH = len(annotated_df)
    
    while(True):
        v_row = annotated_df.iloc[INDEX]
        
        v_row['image_url'] = IMAGE_LINK_HEADER + v_row['image_url']
        
        row_image, row_annotation_bboxes = processImage(v_row['image_url'], v_row['annotation'])
        row_annotated_image = drawAnnotation(row_image, row_annotation_bboxes)
        
        cv2.imshow('image',row_annotated_image)
        
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
            annotated_df.at[INDEX, 'CVApproval'] = 1
            INDEX = IndexAdd(INDEX,LENGTH)
            
        if cv2.waitKey(0) & 0xFF == ord('s'): 
            #good annotation
            print('S button pressed. Bad annotation.')
            annotated_df.at[INDEX, 'CVApproval'] = -1
            INDEX = IndexAdd(INDEX,LENGTH)
            
        if cv2.waitKey(0) & 0xFF == ord('q'):
            print('Q button pressed. Exiting...')
            break
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    print('image privatization started')
    s3ImageSharing(url_list,False)
    print('Done')

    cv2.destroyAllWindows()
    annotated_df.to_csv(os.path.join(DATASET_FOLDER,'test_dataset_evaluate_updated.csv'),index=False)
    