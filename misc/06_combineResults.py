# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:29:56 2020

@author: kompich
"""

import pandas as pd
import numpy as np

df_annotinp = pd.read_csv('results/00_AnnotationOutput.csv')

df_annotinp = df_annotinp[['Input.image_url','Answer.annotatedResult.boundingBoxes']]
df_annotinp.rename(columns={'Input.image_url':'image_url','Answer.annotatedResult.boundingBoxes':'image_annotation'},inplace=True)

df_valout = pd.read_csv('results/03_ValidationOutputSummary.csv')

df_merge = pd.merge(df_valout, df_annotinp, on='image_url')

df_merge.to_csv('results/04_ValidationOutputMerged.csv')


