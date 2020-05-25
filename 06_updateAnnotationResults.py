# -*- coding: utf-8 -*-
"""
Input - Validation_Review_Thread#.csv and Mturk tier 1 results file
Process Mturk tier 1 results file based on Validation_Review_Thread#.csv to Mturk results review format
Output - modified Mturk tier 1 results file in Results Validation format
"""

THREAD_NUMBER = 1
REJECTION_TEXT = 'Task rejected due to one of the following reasons: 1. Not all objects on the image are selected with bounding boxes (including parked and small vehicles); 2. Bounding box is not tight around the object. For more annotation details please reference Task Instruction.'

import pandas as pd
import numpy as np

annot_df = pd.read_csv('results/Annotation_Thread1_OUTPUT.csv')
valid_df_filename = 'results/Validation_Review_Thread' + str(THREAD_NUMBER) + '.csv'
valid_df = pd.read_csv(valid_df_filename)

valid_df.rename(columns={'image_url':'Input.image_url'},inplace=True)

joined_df = annot_df.merge(valid_df, on='Input.image_url', how='left')

joined_df['Approve'] = joined_df.apply(lambda x: 'x' if x['Category']>0 else '', axis=1)
joined_df['Reject'] = joined_df.apply(lambda x: REJECTION_TEXT if x['Category']<=-1 else '', axis=1)

joined_df.drop(['annotation','Category','Decision'], axis=1, inplace=True)

filename = 'results/AnnotationResultsValidated_Thread' + str(THREAD_NUMBER) + '.csv'
joined_df.to_csv(filename,index=False)
