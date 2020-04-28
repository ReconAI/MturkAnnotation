# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:29:56 2020

@author: kompich
"""

import pandas as pd
import numpy as np

df = pd.read_csv('results/ValidationTaskOuput.csv')

labels = {
    'Correct annotation' : 1,
    'Annotation doesnt meet requirements' : -1
    }

df = df[['Input.image_url','Answer.category.label']]
df.rename(columns={'Input.image_url':'image_url','Answer.category.label':'category_lbl'},inplace=True)

df['category'] = df['category_lbl'].map(labels)

df.drop(['category_lbl'], axis=1, inplace=True)

#print(df.head())

new_df = df.groupby(['image_url']).sum()

#print(new_df.head())

new_df['Decision'] = new_df['category'].apply(lambda x: 'Correct' if x > 0 else 'Incorrect')

new_df.to_csv('results/ValidationReviewed.csv')
