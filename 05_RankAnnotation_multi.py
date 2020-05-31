# -*- coding: utf-8 -*-
"""
Input - Mturk tier 2 results file (Batch_3998716_batch_results.csv / 06_Thread#_ValidationOutput.csv)
Process Mturk tier 2 results file into a summary file
Output - 07_Thread#_ValidationOutput_SingleColumn.csv (Output file in one column [url, annot, category])
       - 08_Thread#_ValidationOutput_Summary.csv (summary on each annotation, grouped by Score)
       - 09_Thread#_AnnotaionRankInput.csv (Ranking file for Mturk annotation task)
"""

#libs import
import pandas as pd
import numpy as np
import os

#constants declaration
SAVE_FOLDER = 'AnnotationResults'
NUM_ANNOTATION_IMAGES = 5
NUM_VALIDATION_IMAGES = 15
THREAD_NUMBER = 2
REJECTION_TEXT = 'Incorrect classification of Image #{0}. Task rejected due to one of the following reasons: 1. Not all objects on the image are selected with bounding boxes (including parked and small vehicles). 2. Bounding box is not tight around the object. For more annotation details please reference Task Instruction.'

#Load validation result
ValidationOut_Filename = '06_Thread{0}_ValidationOutput.csv'.format(THREAD_NUMBER)
validOut_df = pd.read_csv(os.path.join(SAVE_FOLDER,ValidationOut_Filename))

labels = {
    'Correct annotation' : 1,
    'Annotation doesnt meet requirements' : -1
    }

## Prepare one-column dataframe ( [url_0, annot_0, category_0, url_1, annot_1, category_1] => [url, annot, category] )
df_list = []
for i in range(NUM_VALIDATION_IMAGES):
    
    col_img_url_name = 'Input.image_url_'+str(i)
    col_annot_name = 'Input.image_annotation_'+str(i)
    
    col_annot_cat_name_1 = 'Answer.category_'+str(i)
    col_annot_cat_name_2 = col_annot_cat_name_1+'.label'
    
    if col_annot_cat_name_1 not in validOut_df.columns:
        validOut_df[col_annot_cat_name_1] = ''
    if col_annot_cat_name_2 not in validOut_df.columns:
        validOut_df[col_annot_cat_name_2] = ''
    
    sub_df = validOut_df[[col_img_url_name,col_annot_name,col_annot_cat_name_1,col_annot_cat_name_2]]
    
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
        
#Save result into a file
validOut_SingleCol_df = pd.concat(df_list)
validOut_SingleCol_df['Category'] = validOut_SingleCol_df['category_lbl'].map(labels)
validOut_SingleCol_df.drop(['category_lbl'], axis=1, inplace=True)
ValidationOut_SingleColumn_Filename = '07_Thread{0}_ValidationOutput_SingleColumn.csv'.format(THREAD_NUMBER)
validOut_SingleCol_df.to_csv(os.path.join(SAVE_FOLDER,ValidationOut_SingleColumn_Filename),index=False)

#Prepare a summary file
#current aggregation
validOut_Summary_df = validOut_SingleCol_df.groupby(['image_url','annotation'], as_index=False).sum()
#possible new aggregation with count
#validOut_Summary_df = validOut_SingleCol_df.groupby(['image_url','annotation'], as_index=False).agg(
#        Category=pd.NamedAgg(column='Category', aggfunc='sum'),
#        CatCount=pd.NamedAgg(column='Category', aggfunc='count'),  
#    )

validOut_Summary_df['Decision'] = validOut_Summary_df['Category'].apply(lambda x: 'Correct' if x > 0 else 'Incorrect')
ValidationOut_Summary_Filename = '08_Thread{0}_ValidationOutput_Summary.csv'.format(THREAD_NUMBER)
validOut_Summary_df.to_csv(os.path.join(SAVE_FOLDER,ValidationOut_Summary_Filename),index=False)

#Prepare an annotation rank file

## Load Annotation Output
### [Input.image_url_0, Answer.annotatedResult_0 ] x NUM_ANNOTATION_IMAGES
AnnotationOut_Filename = '03_Thread{0}_AnnotationOutput.csv'.format(THREAD_NUMBER)
annot_df = pd.read_csv(os.path.join(SAVE_FOLDER,AnnotationOut_Filename))

## validOut_Summary_df
### [image_url,annotation,Category(-5:5),CatCount(0:5),Decision(Correct/Incorrect)]
validOut_Summary_df.drop(['annotation','Decision'], axis=1, inplace=True)

df_list = []
for i in range(NUM_ANNOTATION_IMAGES):
    tmp_validSummary_df = validOut_Summary_df.copy()

    col_img_url_name = 'Input.image_url_'+str(i)
    col_cat_Name = 'Category_'+str(i)

    tmp_validSummary_df.rename(columns={'image_url':col_img_url_name,'Category':col_cat_Name},inplace=True)

    annot_df = annot_df.merge(tmp_validSummary_df, on=col_img_url_name, how='left')

## process annot_df
### [Input.image_url_0, Answer.annotatedResult_0, Category_0 ] x NUM_ANNOTATION_IMAGES
def getIncorrectImgNum(x):
    for i in range(NUM_ANNOTATION_IMAGES):
        cat_col_name = 'Category_'+str(i)
        if x[cat_col_name] < 0:
            incNum = i+1
            return incNum
    return -1

annot_df['IncorrectImageNum'] = annot_df.apply(lambda x: getIncorrectImgNum(x),axis=1)

annot_df['Approve'] = annot_df.apply(lambda x: 'x' if x['IncorrectImageNum']<0 else '', axis=1)
annot_df['Reject'] = annot_df.apply(lambda x: REJECTION_TEXT.format(x['IncorrectImageNum']) if x['IncorrectImageNum']>0 else '', axis=1)

for i in range(NUM_ANNOTATION_IMAGES):
    cat_col_name = 'Category_'+str(i)
    annot_df.drop([cat_col_name], axis=1, inplace=True)

annot_df.drop(['IncorrectImageNum'], axis=1, inplace=True)

## Saving result file
AnnotationRankInput_Filename = '09_Thread{0}_AnnotaionRankInput.csv'.format(THREAD_NUMBER)
annot_df.to_csv(os.path.join(SAVE_FOLDER,AnnotationRankInput_Filename),index=False)
