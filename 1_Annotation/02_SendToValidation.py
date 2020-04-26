# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 18:08:26 2020

@author: kompich
"""

import pandas as pd

df = pd.read_csv('AMTAssignment/Batch_3998716_batch_results.csv') #

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


sub_df.to_csv('AMTAssignment/to_Validation.csv',index=False)
