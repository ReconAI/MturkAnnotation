# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:29:56 2020

@author: kompich
"""

#"Input.image_url_0","Input.image_annotation_0","Input.image_url_1","Input.image_annotation_1","Input.image_url_2","Input.image_annotation_2"
#category_0, category_1, category_1, category_2,category_9.label??
#category_0, category_1, category_1, category_2,category_9.label??

NUMBER_OF_IMAGES_PER_TASK = 10
THREAD_NUMBER = 3

import pandas as pd
import numpy as np

df = pd.read_csv('results/Batch_4050706_batch_results.csv')

labels = {
    'Correct annotation' : 1,
    'Annotation doesnt meet requirements' : -1
    }

df_list = []

for i in range(NUMBER_OF_IMAGES_PER_TASK):
    
    col_img_url_name = 'Input.image_url_'+str(i)
    col_annot_name = 'Input.image_annotation_'+str(i)
    
    col_annot_cat_name_1 = 'Answer.category_'+str(i)
    col_annot_cat_name_2 = col_annot_cat_name_1+'.label'
    
    if col_annot_cat_name_1 not in df.columns:
        df[col_annot_cat_name_1] = ''
    if col_annot_cat_name_2 not in df.columns:
        df[col_annot_cat_name_2] = ''
    
    
    sub_df = df[[col_img_url_name,col_annot_name,col_annot_cat_name_1,col_annot_cat_name_2]]
    
    print(sub_df.head())
    
    def merge_nans(x,y):
        if pd.isnull(x):
            x = ''
        if pd.isnull(y):
            y = ''
        return x + y
    
    sub_df[col_annot_cat_name_1] = sub_df.apply(lambda x: merge_nans(x[col_annot_cat_name_1], x[col_annot_cat_name_2]),axis=1)
    
    sub_df.rename(columns={col_img_url_name:'image_url',col_annot_name:'annotation',col_annot_cat_name_1:'category_lbl'},inplace=True)
    sub_df.drop([col_annot_cat_name_2], axis=1,inplace=True)
    
    df_list.append(sub_df)
        
merged_df = pd.concat(df_list)
merged_df['Category'] = merged_df['category_lbl'].map(labels)
merged_df.drop(['category_lbl'], axis=1, inplace=True)

#merged_df.to_csv('results/ValidationMerged.csv')

new_df = merged_df.groupby(['image_url','annotation']).sum()
new_df['Decision'] = new_df['Category'].apply(lambda x: 'Correct' if x > 0 else 'Incorrect')

filename = 'results/Validation_Review_Thread' + str(THREAD_NUMBER) + '.csv'
new_df.to_csv(filename)

