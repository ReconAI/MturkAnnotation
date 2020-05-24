# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 18:08:26 2020

@author: kompich
"""

NUM_SAMPLES_IN_TASK = 10
THREAD_NUMBER = 3

import pandas as pd
import numpy as np

df = pd.read_csv('results/Batch_3998716_batch_results.csv') #

sub_df = df[['Input.image_url','Answer.annotatedResult.boundingBoxes']]

sub_df.rename(columns={'Input.image_url':'image_url','Answer.annotatedResult.boundingBoxes':'image_annotation'},inplace=True)

print(sub_df.dtypes)

print(sub_df['image_annotation'].head())

sub_df['image_annotation'] = sub_df['image_annotation'].str.replace('"height"', 'height')
sub_df['image_annotation'] = sub_df['image_annotation'].str.replace('"label"', 'label')
sub_df['image_annotation'] = sub_df['image_annotation'].str.replace('"left"', 'left')
sub_df['image_annotation'] = sub_df['image_annotation'].str.replace('"top"', 'top')
sub_df['image_annotation'] = sub_df['image_annotation'].str.replace('"width"', 'width')

sub_df['image_annotation'] = sub_df['image_annotation'].str.replace('"', "'")
print(sub_df['image_annotation'].head())

overlay_begin = "{'boundingBox': {labels: ['Car', 'Van', 'Truck', 'Trailer', 'Bus', 'Motorbike', 'Bicycle', 'Heavy Equipment', 'Car Trailer', 'Tractor', 'Pedestrian'], value: "
overlay_end = "},}"

sub_df['image_annotation'] = overlay_begin + sub_df['image_annotation'].replace('"',"'") + overlay_end

# here we have a good single-line dataset
ROW_COUNT = len(df.index)
ROWS_TO_ADD = 0

while ((ROW_COUNT+ROWS_TO_ADD) % NUM_SAMPLES_IN_TASK != 0):
    ROWS_TO_ADD = ROWS_TO_ADD + 1

sub_df_footer = sub_df.head(ROWS_TO_ADD)
sub_df = sub_df.append(sub_df_footer)

## Split dataset by NUM_SAMPLES_IN_TASK columns
dataframes = np.array_split(sub_df, NUM_SAMPLES_IN_TASK)
new_dataframes = []

for idx, mini_df in enumerate(dataframes):
    print(len(mini_df))
    
    url_name = 'image_url_' + str(idx)
    annot_name = 'image_annotation_' + str(idx)
    mini_df.rename(columns={'image_url':url_name,'image_annotation':annot_name},inplace=True)
    mini_df.reset_index(inplace=True)
    new_dataframes.append(mini_df)
    
    
new_sub_df = pd.concat(new_dataframes, axis=1, sort=False)

new_sub_df.drop(['index'],axis=1,inplace=True)

save_filename = 'results/Validation_Thread' + str(THREAD_NUMBER) + '.csv'

new_sub_df.to_csv(save_filename,index=False)

































