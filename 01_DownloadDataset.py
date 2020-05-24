# -*- coding: utf-8 -*-
"""
Download list of all images from S3 and save them in csv
"""

import boto3
from credentials import *
import pandas as pd


session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3 = session.resource('s3')
your_bucket = s3.Bucket('reconai-traffic')

dataset_arr = []

#C0150801_r0_w0_2020-03-15_19-57-12.jpg
for s3_file in your_bucket.objects.filter(Prefix='images/C'): #all():
    dataset_arr.append(s3_file.key)
print('done')    


df = pd.DataFrame(data=dataset_arr,columns=['image_url'])

print(df.head())

df.to_csv('results/S3Dataset.csv',index=False)
