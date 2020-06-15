# -*- coding: utf-8 -*-
"""
Set of utilities to help annotators to investigate their cases
ToDo: test code
"""

import boto3
from tqdm import tqdm
import os
import pandas as pd

from utilities import *
from credentials import *

if __name__ == '__main__':
    
    ##Input parameters
    THREAD_NUMBER = 4
    NUM_IMAGES_PER_ANNOTATION_TASK = 5
    NUM_VALIDATION_IMAGES = 15
    SAVE_FOLDER = '../AnnotationResults'
    
    annotation_HIT_ID = '3WRKFXQBPFINSWWP3IFFM7TS97FIY2'
    Worker_ID = 'AWUML5SWVKPN6'

    DATA_SAVE_FOLDER = annotation_HIT_ID

    ##Read all files as datasets
    #AnnotationOutFilename = '03_Thread{0}_AnnotationOutput.csv'.format(THREAD_NUMBER)
    AnnotationOutFilename = '03_Thread4_AnnotationOutput_part3_06072020.csv'
    annotOut_df = pd.read_csv(os.path.join(SAVE_FOLDER,AnnotationOutFilename))
    
    #ValidationOut_Filename = '06_Thread{0}_ValidationOutput.csv'.format(THREAD_NUMBER)
    ValidationOut_Filename = '06_Thread4_ValidationOutput.csv'
    """
    AnnotationRank_Filename = '09_Thread{0}_AnnotaionRankInput.csv'.format(THREAD_NUMBER)
    #AnnotationRank_Filename = ''
    annotRank_df = pd.read_csv(os.path.join(SAVE_FOLDER,AnnotationRank_Filename))
    """


    ### Step 1. Make sure that Annotation is correct
    
    ##Filter Annotation Output by provided HIT ID
    annotout_filter = annotOut_df['HITId'] == annotation_HIT_ID
    annotOut_df = annotOut_df.loc[annotout_filter]

    ##Put HITs images and annotations into two lists
    rowid_list = []
    imgid_list = []
    images_list = []
    annotations_list = []

    for row_index, row in annotOut_df.iterrows():
        for idx in range(NUM_IMAGES_PER_ANNOTATION_TASK):
            rowid_list.append(row_index)
            imgid_list.append(idx)

            image_colname = 'Input.image_url_' + str(idx)
            annot_colname = 'Answer.annotatedResult_' + str(idx) + '.boundingBoxes'

            images_list.append(row[image_colname])
            annotations_list.append(row[annot_colname])

    ##Make all images public
    s3ImageSharing(images_list)
    
    ##Create folder and save images with annotations on top
    if (not os.path.isdir(DATA_SAVE_FOLDER)):
        os.mkdir(DATA_SAVE_FOLDER)
    for row_id, img_id, image_url, annotation in tqdm(zip(rowid_list,imgid_list,images_list,annotations_list)):
        row_image, row_annotation_bboxes = processImageAnnotation(image_url, annotation)
        row_annotated_image = drawAnnotation(row_image, row_annotation_bboxes)
        
        image_name = 'image_'+str(row_id)+'_'+str(img_id)+'.png'

        row_image_path = os.path.join(DATA_SAVE_FOLDER,image_name)
        cv2.imwrite(row_image_path, row_annotated_image)
     
    ### Step 1 Result: 
    #### > if annotation contains issues - let annotator know
    #### > if annotation is correct move to Step 2

    if False:
        ### Step 2. Check how annotation was validated. 
        validOut_df = pd.read_csv(os.path.join(SAVE_FOLDER,ValidationOut_Filename))
        
        # Go through ValidationOutput
        # Search by Input.image_url_str(i)
        # retrieve HITId, WorkerId, Answer.category_str(i) (see ValidOut parsing part)
        # for each image provide list of Validation labels, WorkerIds and HITIds
        
        dataframes_list = []
        
        #iterate columns
        for col_id in range(NUM_VALIDATION_IMAGES):
            
            img_col_name = 'Input.image_url_'+ str(col_id)
            label_col_name = 'Answer.category_' + str(col_id)
            
            img_filter = validOut_df[img_col_name].isin(images_list)
            sub_df = validOut_df.loc[img_filter,['HITId','WorkerId',img_col_name,label_col_name]]
            sub_df.rename(columns={img_col_name:'image_url',label_col_name:'label'},inplace=True)
            dataframes_list.append(sub_df)
        
        image_ranks = pd.concat(dataframes_list)
        
        print(image_ranks.head())
        
        image_ranks.sort_values(by=['image_url','WorkerId'],inplace=True)
        
        filename = 'HIT_' + annotation_HIT_ID + '_RankDetails.csv'
        filename = os.path.join(annotation_HIT_ID,filename)
        image_ranks.to_csv(filename,index=False)
        
        print('Done')
        
    #Step 2 Results: 
    ### Evaluate how workers annotated images, double check results
    
    #Step 3 : To be done:
    ## For each worker count how many HITs he/she accomplished, what's Correct/Incorrect label rate, generally and in this task
    