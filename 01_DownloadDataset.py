# -*- coding: utf-8 -*-
"""
Input - S3 bucket name and folder
Download list of all images from S3 and save them in a csv file
Output - results/S3Dataset.csv
"""

import boto3
from credentials import *
import pandas as pd

#filter images by size, other way to reduce the number of 'bad' images
FILTER_BY_SIZE = True
MIN_IMAGE_SIZE = 2000

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3 = session.resource('s3')
your_bucket = s3.Bucket('reconai-traffic')

dataset_arr = []

#C0150801_r0_w0_2020-03-15_19-57-12.jpg
for s3_file in your_bucket.objects.filter(Prefix='images/C'): #all():
	if FILTER_BY_SIZE:
		if (s3_file.size>2000):
			dataset_arr.append(s3_file.key)
	else:
		dataset_arr.append(s3_file.key)
		
print('done')


df = pd.DataFrame(data=dataset_arr,columns=['image_url'])

print(df.head())

df.to_csv('results/S3Dataset.csv',index=False)
