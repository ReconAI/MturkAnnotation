# -*- coding: utf-8 -*-
"""
Input - Dataset.csv and Annotation_Thread#_updated.csv
Update Dataset.csv based on Annotation_Thread#.csv data
Output - Dataset.csv
"""

THREAD_NUMBER = 3

import pandas as pd
import numpy as np

#image_url,annotation,threadNum,isAnnotated
#images/C0150200_r0_w0_2020-02-21_15-30-08.jpg,,1.0,False
df = pd.read_csv('results/Dataset.csv')

#image_url,threadNum,annotation,accepted
#images/C0150302_r2_w4_2020-04-03_07-58-28.jpg,2,,False
#images/C0150302_r1_w3_2020-05-03_07-58-22.jpg,2,{},True
thread_df_filename = 'results/Annotation_Thread' + str(THREAD_NUMBER) + '_updated.csv'
thread_df = pd.read_csv(thread_df_filename)
thread_df.drop(['threadNum'], axis=1, inplace=True)
thread_df.rename(columns={'annotation':'new_annotation'},inplace=True)

joined_thread_df = df.merge(thread_df, on='image_url', how='left')
joined_thread_df['isAnnotated'] = joined_thread_df.apply(lambda x: x.accepted if x.accepted==True else x.isAnnotated, axis=1)
joined_thread_df['threadNum'] = joined_thread_df.apply(lambda x: '' if (x.accepted==True or x.accepted==False) else x.threadNum, axis=1)
joined_thread_df['annotation'] = joined_thread_df.apply(lambda x: x.new_annotation if x.accepted==True else x.annotation, axis=1)
joined_thread_df.drop(['new_annotation','accepted'], axis=1, inplace=True)
joined_thread_df.to_csv('results/Dataset.csv',index=False)

print('Thread file updated and saved')



