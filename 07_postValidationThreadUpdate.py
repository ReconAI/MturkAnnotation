# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:29:56 2020

@author: kompich
"""

THREAD_NUMBER = 3
IMAGE_LINK_HEADER = 'https://reconai-traffic.s3.eu-central-1.amazonaws.com/'

import pandas as pd
import boto3
import numpy as np
from credentials import *

#image_url,annotation,Category,Decision
#https://reconai-traffic.s3.eu-central-1.amazonaws.com/images/C0153100_r0_w0_2020-02-21_15-30-50.jpg,"{...}",4,Correct
valid_df_filename = 'results/Validation_Review_Thread' + str(THREAD_NUMBER) + '.csv'
valid_df = pd.read_csv(valid_df_filename)
valid_df['image_url'] = valid_df['image_url'].str.replace(IMAGE_LINK_HEADER,'')
valid_df.rename(columns={'annotation':'new_annotation'},inplace=True)

filt_correctAnnotations = valid_df['Decision'] == 'Correct'
valid_df_correctAnnotations = valid_df.loc(filt_correctAnnotations, ['image_url','annotation'])


#image_url,threadNum,annotation,accepted
#images/C0150302_r2_w4_2020-04-03_07-58-28.jpg,2,,False
thread_df_filename = 'results/Annotation_Thread' + str(THREAD_NUMBER) + '.csv'
thread_df = pd.read_csv(thread_df_filename)

joined_thread_df = thread_df.join(valid_df_correctAnnotations, on='image_url')
def update_annotation(old_annotation, new_annotation):
    if pd.isnull(new_annotation):
        return old_annotation, False
    return new_annotation, True       
joined_thread_df['annotation','accepted'] = joined_thread_df.apply(lambda x: update_annotation(x['annotation'], x['new_annotation']),axis=1)

joined_thread_df.drop(['new_annotation','Category','Decision'], axis=1, inplace=True)

updated_thread_df_filename = 'results/Annotation_Thread' + str(THREAD_NUMBER) + '_updated.csv'
joined_thread_df.to_csv(updated_thread_df_filename)

print('Thread file updated and saved')

####Connect to AWS and make images private
###############

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3 = session.resource('s3')
bucket = s3.Bucket(AWS_BUCKET_NAME)

for img_path in thread_df['image_url'].tolist():
    for s3_file in bucket.objects.filter(Prefix=img_path):
        key = s3_file.key
        
        #Grant read access to files
        object_acl = s3.ObjectAcl(AWS_BUCKET_NAME,key)
        response = object_acl.put(ACL='private')
        
print('Images made public')
        

