# -*- coding: utf-8 -*-
"""
Input - Dataset.csv
1. From Dataset.csv select THREAD_SIZE of images with empty ThreadNumber, put them into separated dataframe (thread_df)
2. Set thread number to thread_df values based on THREAD_NUMBER
3. Update threadNum for selected records in Dataset.csv
4. Make images public
5. Put thread_df in separate file (01_Thread#_AnnotationInput.csv) with annotation and accepted columns filled with default values
Output - 01_Thread#_Batch.csv, 02_Thread#_AnnotationInput.csv and updated Dataset.csv
"""

#libs import
from credentials import *
import pandas as pd
import boto3
import os
import numpy as np
from tqdm import tqdm

#constants declaration
SAVE_FOLDER = 'AnnotationResults'
IMAGE_LINK_HEADER = 'https://reconai-traffic.s3.eu-central-1.amazonaws.com/'
THREAD_NUMBER = 10
THREAD_SIZE = 50000
NUM_IMAGES_PER_ANNOTATION_TASK = 5

#Dataset handling
df = pd.read_csv(os.path.join(SAVE_FOLDER,'Dataset.csv'))

filt_emptyThreadNum = (df['threadNum'].isnull()) & (df['isAnnotated'] == False)

thread_df = df.loc[filt_emptyThreadNum, ['image_url','threadNum']].head(THREAD_SIZE)
thread_df['threadNum'] = THREAD_NUMBER

df.update(thread_df)

df.to_csv(os.path.join(SAVE_FOLDER,'Dataset.csv'),index=False)

#AWS policies handling
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3 = session.resource('s3')
bucket = s3.Bucket(AWS_BUCKET_NAME)

for img_path in tqdm(thread_df['image_url'].tolist()):
    for s3_file in bucket.objects.filter(Prefix=img_path):
        key = s3_file.key
        
        #Grant read access to files
        object_acl = s3.ObjectAcl(AWS_BUCKET_NAME,key)
        response = object_acl.put(ACL='public-read')

print('Images made public')

#Thread file handling
thread_df['annotation'] = ''
thread_df['accepted'] = False
thread_df['image_url'] = IMAGE_LINK_HEADER +  thread_df['image_url']

## Save thread batch to separate file
ThreadBatchFilename = '01_Thread{0}_Batch.csv'.format(THREAD_NUMBER)
thread_df.to_csv(os.path.join(SAVE_FOLDER,ThreadBatchFilename),index=False)

## Remove unused columns
thread_df.drop(['annotation','accepted','threadNum'], axis=1, inplace=True)

## Add extra lines to single-thread dataset
ROW_COUNT = len(thread_df.index)
ROWS_TO_ADD = 0

while ((ROW_COUNT+ROWS_TO_ADD) % NUM_IMAGES_PER_ANNOTATION_TASK != 0):
    ROWS_TO_ADD = ROWS_TO_ADD + 1

thread_df = thread_df.append(thread_df.head(ROWS_TO_ADD))
print('{0} rows added to a thread'.format(ROWS_TO_ADD))

## Split dataset by NUM_IMAGES_PER_ANNOTATION_TASK columns
dataframes = np.array_split(thread_df, NUM_IMAGES_PER_ANNOTATION_TASK)
new_dataframes = []

for idx, mini_df in enumerate(dataframes):
    url_name = 'image_url_' + str(idx)
    mini_df.rename(columns={'image_url':url_name},inplace=True)
    mini_df.reset_index(inplace=True)
    new_dataframes.append(mini_df)

thread_df_multitask = pd.concat(new_dataframes, axis=1, sort=False)
thread_df_multitask.drop(['index'],axis=1,inplace=True)

AnnotationInputFilename = '02_Thread{0}_AnnotationInput.csv'.format(THREAD_NUMBER)
thread_df_multitask.to_csv(os.path.join(SAVE_FOLDER,AnnotationInputFilename),index=False)
print('Thread file saved')
