# -*- coding: utf-8 -*-
"""
Input - Validation_Review_Thread#.csv and Annotation_Thread#.csv
Update Annotation_Thread#.csv based on Validation_Review_Thread#.csv data, make images provate
Output - Annotation_Thread#_updated.csv
"""

THREAD_NUMBER = 1
IMAGE_LINK_HEADER = 'https://reconai-traffic.s3.eu-central-1.amazonaws.com/'

import pandas as pd
import boto3
import numpy as np
from credentials import *

#image_url,annotation,Category,Decision
#https://reconai-traffic.s3.eu-central-1.amazonaws.com/images/C0153100_r0_w0_2020-02-21_15-30-50.jpg,"{...}",4,Correct
valid_df_filename = 'results/Validation_Review_Thread' + str(THREAD_NUMBER) + '.csv'
valid_df = pd.read_csv(valid_df_filename)

valid_df.rename(columns={'annotation':'new_annotation'},inplace=True)

filt_correctAnnotations = valid_df['Decision'] == 'Correct'
valid_df_correctAnnotations = valid_df.loc[filt_correctAnnotations,['image_url','new_annotation']] #, 

#image_url,threadNum,annotation,accepted
#images/C0150302_r2_w4_2020-04-03_07-58-28.jpg,2,,False
thread_df_filename = 'results/Annotation_Thread' + str(THREAD_NUMBER) + '.csv'
thread_df = pd.read_csv(thread_df_filename)

joined_thread_df = thread_df.merge(valid_df_correctAnnotations, on='image_url', how='left')

joined_thread_df['annotation'] = joined_thread_df.apply(lambda x: x.new_annotation if (~pd.isnull(x.new_annotation)) else x.annotation, axis=1)
joined_thread_df['accepted'] = joined_thread_df.apply(lambda x: False if (pd.isnull(x.new_annotation) or x.new_annotation == '') else True, axis=1)
joined_thread_df.drop(['new_annotation'], axis=1, inplace=True)

joined_thread_df['image_url'] = joined_thread_df['image_url'].str.replace(IMAGE_LINK_HEADER,'')

updated_thread_df_filename = 'results/Annotation_Thread' + str(THREAD_NUMBER) + '_updated.csv'
joined_thread_df.to_csv(updated_thread_df_filename,index=False)


print('Thread file updated and saved')

####Connect to AWS and make images private
###############

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3 = session.resource('s3')
bucket = s3.Bucket(AWS_BUCKET_NAME)

for img_path in joined_thread_df['image_url']:
    for s3_file in bucket.objects.filter(Prefix=img_path):
        key = s3_file.key
        
        #Grant read access to files
        object_acl = s3.ObjectAcl(AWS_BUCKET_NAME,key)
        response = object_acl.put(ACL='private')
        
print('Images made private')
