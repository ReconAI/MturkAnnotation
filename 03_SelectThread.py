# -*- coding: utf-8 -*-
"""
Input - Dataset.csv
1. From Dataset.csv select THREAD_SIZE of images with empty ThreadNumber, put them into separated dataframe (thread_df)
2. Set thread number to thread_df values based on THREAD_NUMBER
3. Update threadNum for selected records in Dataset.csv
4. Make images public
5. Put thread_df in separate file (Annotation_Thread#.csv) with annotation and accepted columns filled with default values

Output - Annotation_Thread#.csv and updated Dataset.csv
"""

import pandas as pd
import boto3
from credentials import *

THREAD_NUMBER = 3
THREAD_SIZE = 10

df = pd.read_csv('results/Dataset.csv')


filt_emptyThreadNum = df['threadNum'].isnull()

thread_df = df.loc[filt_emptyThreadNum, ['image_url','threadNum']].head(THREAD_SIZE)
thread_df['threadNum'] = THREAD_NUMBER

df.update(thread_df)

thread_df['annotation'] = ''
thread_df['accepted'] = False

df.to_csv('results/Dataset.csv',index=False)

threadFilename = 'results/Annotation_Thread' + str(THREAD_NUMBER)+ '.csv'
thread_df.to_csv(threadFilename,index=False)
print('Thread file saved')

####Connect to AWS and make images public
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
        response = object_acl.put(ACL='public-read')
        
print('Images made public')
        
        
        
        
