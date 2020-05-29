# -*- coding: utf-8 -*-
"""
Input - Mturk tier 1 results file  (Batch_3998716_batch_results.csv / 03_Thread#_AnnotationOutput.csv)
Process Mturk tier 1 results into input format for Mturk tier 2
Output - 04_Thread#_AnnotaionOutput_SingleCol.csv and 05_Thread#_ValidationInput.csv
"""

#libs import
import pandas as pd
import numpy as np
import os
from tqdm import tqdm

#constants declaration
SAVE_FOLDER = 'AnnotationResults'
NUM_ANNOTATION_IMAGES = 5
NUM_VALIDATION_IMAGES = 15
THREAD_NUMBER = 2

#Load annotation result

AnnotationOutFilename = '03_Thread{0}_AnnotationOutput.csv'.format(THREAD_NUMBER)
annotOut_df = pd.read_csv(os.path.join(SAVE_FOLDER,AnnotationOutFilename))

## Prepare one-column dataframe ( [url_0, annot_0,url_1, annot_1] => [url, annot]   )
df_list = []
for i in range(NUM_ANNOTATION_IMAGES):
    col_img_url_name = 'Input.image_url_'+str(i)
    col_annot_name = 'Answer.annotatedResult_{0}.boundingBoxes'.format(i)
    sub_df = annotOut_df[[col_img_url_name,col_annot_name]]
    sub_df.rename(columns={col_img_url_name:'image_url',col_annot_name:'image_annotation'},inplace=True)
    df_list.append(sub_df)

## Single column [image_url, image_annotation] dataset
annotOut_df = pd.concat(df_list)

AnnotationOutSingleFilename = '04_Thread{0}_AnnotaionOutput_SingleCol.csv'.format(THREAD_NUMBER)
annotOut_df.to_csv(os.path.join(SAVE_FOLDER,AnnotationOutSingleFilename),index=False)

#sub_df -> annotOut_df

overlay_begin = "{'boundingBox': {labels: ['Car', 'Van', 'Truck', 'Trailer', 'Bus', 'Motorbike', 'Bicycle', 'Heavy Equipment', 'Car Trailer', 'Tractor', 'Pedestrian'], value: "
overlay_end = "},}"
## ToDo: Find a way to make it prettier
annotOut_df['image_annotation'] = annotOut_df['image_annotation'].str.replace('"height"', 'height')
annotOut_df['image_annotation'] = annotOut_df['image_annotation'].str.replace('"label"', 'label')
annotOut_df['image_annotation'] = annotOut_df['image_annotation'].str.replace('"left"', 'left')
annotOut_df['image_annotation'] = annotOut_df['image_annotation'].str.replace('"top"', 'top')
annotOut_df['image_annotation'] = annotOut_df['image_annotation'].str.replace('"width"', 'width')
annotOut_df['image_annotation'] = annotOut_df['image_annotation'].str.replace('"', "'")
annotOut_df['image_annotation'] = overlay_begin + annotOut_df['image_annotation'].replace('"',"'") + overlay_end

## Add extra columns in the end of dataset if needed
## Thread df and annotOut_df!!! Uncomment below if fails
## ROW_COUNT = len(df.index)
ROW_COUNT = len(annotOut_df.index)
ROWS_TO_ADD = 0

while ((ROW_COUNT+ROWS_TO_ADD) % NUM_VALIDATION_IMAGES != 0):
    ROWS_TO_ADD = ROWS_TO_ADD + 1

annotOut_df = annotOut_df.append(annotOut_df.head(ROWS_TO_ADD))

## Split dataset by NUM_VALIDATION_IMAGES columns
dataframes = np.array_split(annotOut_df, NUM_VALIDATION_IMAGES)
new_dataframes = []

for idx, mini_df in enumerate(dataframes):
    url_name = 'image_url_' + str(idx)
    annot_name = 'image_annotation_' + str(idx)
    mini_df.rename(columns={'image_url':url_name,'image_annotation':annot_name},inplace=True)
    mini_df.reset_index(inplace=True)
    new_dataframes.append(mini_df)
    
validInput_df = pd.concat(new_dataframes, axis=1, sort=False)
validInput_df.drop(['index'],axis=1,inplace=True)

ValidationInpFilename = '05_Thread{0}_ValidationInput.csv'.format(THREAD_NUMBER)
validInput_df.to_csv(os.path.join(SAVE_FOLDER,ValidationInpFilename),index=False)
