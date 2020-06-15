# -*- coding: utf-8 -*-
"""
Set of utilities to give insights on current annotation status
ToDo: test code
"""

from tqdm import tqdm
import os
import pandas as pd
import matplotlib.pyplot as plt

from utilities import *

if __name__ == '__main__':

    ##Input parameters
    SAVE_FOLDER = '../AnnotationResults'
    DatasetFilename = 'Dataset.csv'
    df = pd.read_csv(os.path.join(SAVE_FOLDER,DatasetFilename))

    df_filter = df['isAnnotated'] == True
    df = df.loc[df_filter]

    annotList = df['annotation'].tolist()

    totalImagesCnt = len(annotList)
    emptyImagesCnt = 0
    objCountDict = {}
    objWidthList = []
    
    for row in tqdm(annotList):
        
        row_annotation_bboxes = processAnnotation(row)
        
        if len(row_annotation_bboxes) == 0:
            emptyImagesCnt = emptyImagesCnt + 1
        else:
            for v_obj in row_annotation_bboxes:
                v_label = v_obj['label']
                if v_label in objCountDict.keys():
                    objCountDict[v_label] = objCountDict[v_label] + 1
                else:
                    objCountDict[v_label] = 0
                    
                v_width = int(v_obj['width'])
    
                objWidthList.append(v_width)


    print('>{0} empty images out of {1}'.format(emptyImagesCnt,totalImagesCnt))
    print('>objCountDict:{0}'.format(objCountDict))
    
    plt.hist(objWidthList, 5, density=True, facecolor='g', alpha=0.75)

    plt.xlabel('Width')
    plt.ylabel('Count')
    plt.title('Histogram of Width')
    plt.show()
    
    #>21412 empty images out of 39031
    #>objCountDict:{'Car': 65115, 'Bus': 1180, 'Truck': 6504, 'Van': 5842, 'Trailer': 1745, 'Heavy Equipment': 492, 'Tractor': 67, 'Motorbike': 200, 'Car Trailer': 176, 'Pedestrian': 375, 'Bicycle': 60}
    
    
