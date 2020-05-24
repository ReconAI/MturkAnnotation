# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:29:56 2020

@author: kompich
"""

THREAD_NUMBER = 3

import pandas as pd
import numpy as np

#image_url,annotation,threadNum,isAnnotated
#images/C0150200_r0_w0_2020-02-21_15-30-08.jpg,,1.0,False
df = pd.read_csv('result/Dataset.csv')

#image_url,threadNum,annotation,accepted
#images/C0150302_r2_w4_2020-04-03_07-58-28.jpg,2,,False
#images/C0150302_r1_w3_2020-05-03_07-58-22.jpg,2,{},True
thread_df_filename = 'results/Annotation_Thread' + str(THREAD_NUMBER) + '_updated.csv'
thread_df = pd.read_csv(thread_df_filename)
thread_df.drop(['threadNum'], axis=1, inplace=True)
thread_df.rename(columns={'annotation':'new_annotation'},inplace=True)

#image_url,annotation,threadNum,isAnnotated, new_annotation,accepted
joined_thread_df = df.join(thread_df, on='image_url')
#return isAccepted, threadNumber, annotation
def update_annotation(p_accepted, p_threadNumber, p_annotation):
    if p_accepted:
        return p_accepted, np.nan, p_annotation
    return p_accepted, np.nan, np.nan       
joined_thread_df['isAccepted','threadNum','annotation'] = joined_thread_df.apply(lambda x: update_annotation(x['accepted'], x['threadNum'], x['new_annotation']),axis=1)
joined_thread_df.drop(['new_annotation','accepted'], axis=1, inplace=True)
joined_thread_df.to_csv('result/Dataset.csv')

print('Thread file updated and saved')
