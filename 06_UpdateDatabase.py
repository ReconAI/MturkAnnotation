# -*- coding: utf-8 -*-
"""
Input - input is 08_Thread#_ValidationOutput_Summary.csv and Database.csv
Will update Database.csv and fill annotations for correctly annotated images
Output - Database.csv
"""

#libs import
from credentials import *
import pandas as pd
import boto3
import numpy as np
from tqdm import tqdm
import os

#constants declaration
IMAGE_LINK_HEADER = 'https://reconai-traffic.s3.eu-central-1.amazonaws.com/'
SAVE_FOLDER = 'AnnotationResults'
THREAD_NUMBER = 7

#Load Dataset.csv
#image_url,annotation,threadNum,isAnnotated
#images/C0150200_r0_w0_2020-02-21_15-30-08.jpg,,1.0,False
df = pd.read_csv(os.path.join(SAVE_FOLDER,'Dataset.csv'))

#Load validation summary
#image_url,annotation,Category(-5:5),Decision(Correct/Incorrect)
#https://reconai-traffic.s3.eu-central-1.amazonaws.com/images/C0153100_r0_w0_2020-02-21_15-30-50.jpg,"{...}",4,Correct
ValidationSummary_Filename = '08_Thread{0}_ValidationOutput_Summary.csv'.format(THREAD_NUMBER)
valid_df = pd.read_csv(os.path.join(SAVE_FOLDER,ValidationSummary_Filename))

#Modify validation dataset
valid_df.rename(columns={'annotation':'new_annotation'},inplace=True)
valid_df['image_url'] = valid_df['image_url'].str.replace(IMAGE_LINK_HEADER,'')
valid_df['accepted'] = valid_df['Decision'] == 'Correct'

"""
#Connect to AWS and make images private

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3 = session.resource('s3')
bucket = s3.Bucket(AWS_BUCKET_NAME)

for img_path in tqdm(valid_df['image_url'].tolist()):
    for s3_file in bucket.objects.filter(Prefix=img_path):
        key = s3_file.key
        
        #Grant read access to files
        object_acl = s3.ObjectAcl(AWS_BUCKET_NAME,key)
        response = object_acl.put(ACL='private')
        
print('Images made private')
"""
#Filter correct annotation from validation dataset
updated_df = df.merge(valid_df, on='image_url', how='left')
updated_df['isAnnotated'] = updated_df.apply(lambda x: x.accepted if x.accepted==True else x.isAnnotated, axis=1)
updated_df['threadNum'] = updated_df.apply(lambda x: '' if (x.accepted==True or x.accepted==False) else x.threadNum, axis=1)
updated_df['annotation'] = updated_df.apply(lambda x: x.new_annotation if x.accepted==True else x.annotation, axis=1)
updated_df.drop(['new_annotation','accepted','Category','Decision','CatCount'], axis=1, inplace=True)
updated_df.to_csv(os.path.join(SAVE_FOLDER,'Dataset.csv'),index=False)
print('Thread file updated and saved')
