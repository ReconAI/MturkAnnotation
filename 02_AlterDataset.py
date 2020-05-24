# -*- coding: utf-8 -*-
"""
Input - S3Dataset.csv
2. Add following columns
- name - description - type - default value
- annotaion - contains annotation json - json  - empty
- threadNum - related thread number - int - Nan
- isAnnotated - was this image annotated - bool - False
Output - Dataset.csv
"""

import pandas as pd
import numpy as np

df = pd.read_csv('results/S3Dataset.csv')

df['annotation'] = ''
df['threadNum'] = np.nan
df['isAnnotated'] = False

print(df.head(5))

df.to_csv('results/Dataset.csv',index=False)