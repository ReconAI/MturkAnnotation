# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:29:56 2020

@author: kompich
"""

import pandas as pd
import numpy as np

df = pd.read_csv('AMTAssignment/Batch_3998716_batch_results_reviewed.csv')

rejectText = 'Task rejected due to one of the following reasons: 1. Not all objects on the image are selected with bounding boxes (including parked and small vehicles); 2. Bounding box is not tight around the object. For more annotation details please reference Task Instruction.'

df['Approve'] = df.apply(lambda x: 'x' if x['CVApproval']==1 else df['Approve'], axis=1)
df['Reject'] = df.apply(lambda x: rejectText if x['CVApproval']==-1 else '', axis=1)

print(df[['Approve','Reject','CVApproval']].head(100))

df.drop(['CVApproval'], axis=1, inplace=True)

df.to_csv('AMTAssignment/Batch_3998716_batch_results_reviewed_toturk.csv')
