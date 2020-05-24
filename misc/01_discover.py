# -*- coding: utf-8 -*-
"""

"""

import boto3
from credentials import *

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3 = session.resource('s3')
your_bucket = s3.Bucket('reconai-traffic')

SensorIDs = []

#C0150801_r0_w0_2020-03-15_19-57-12.jpg
for s3_file in your_bucket.objects.filter(Prefix='images/'): #all():
    key = s3_file.key.split('_')[0]
    
    if key not in SensorIDs:
        SensorIDs.append(key)

print(SensorIDs)






