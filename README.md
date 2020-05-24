# MturkAnnotation
Documentation and Instructions for MTruk with helpful scripts<br><br>

<img src="images/VisioProcess.png" height="640" width="800" title="Process diagram"/><br>

## Sequence of actions:

0. See Data Preparation
1. Run 01_DownloadDataset.py. It will create S3Dataset.csv - a raw list of all image urls
2. Run 02_AlterDataset.py. It will create Dataset.csv - file which would be used as a final data storage (img_urls, annotations, remarks isAnnotated, threadNumbers)
3. Run 03_SelectThread.py this will create Annotation_Thread#.csv where annotation results for particular thread will be stored, also script will make images related to the Thread #X public. Don't forget to change thread #!
4. (MTurk) Create MTurk detection project with 1 image per task
5. (MTurk) Upload Annotation_Thread#.csv in Mturk, launch annotation task
6. (MTurk) Download Thread annotation result file (format: Batch_3998716_batch_results.csv)
7. Run 04_SendToValidation_multi.py, specify number of images per task (10), get 'Validation_Thread#.csv'
8. (MTurk) Create MTurk Tier 2 project with (NUMBER!) images per task
9. (MTurk) Upload Validation_Thread#.csv in Mturk, launch validation task
10. (MTurk) Download Thread validation result file (format: Batch_3998716_batch_results.csv)
11. Run 05_summarizeMturkValidationFile_multi.py, specify number of images per task (10), get Validation_Review_Thread#.csv
12. Run 06_updateAnnotationResults.py, input is annotation results file (step 6), it will mark assignmens as Approved/Rejected and save as AnnotationResultsValidated_Thread#.csv
13. Run 07_postValidationThreadUpdate.py, specify thread number. it will merge data from Annotation_Thread#.csv from Validation_Review_Thread#.csv into Annotation_Thread#_updated.csv and make images private
14. (MTurk) Upload AnnotationResultsValidated_Thread#.csv to Annotation task results review
15. (MTurk) Close annotation task
16. Run 08_mergeDatabaseResults.csv, specify Annotation_Thread#_updated.csv, it will update records in 04_MergeDatabaseResults (put annotation data and isAnnotated, remove threadNumber)

## File samples

1. S3Dataset.csv - list of links to images from S3 Bucket
2. Dataset.csv - S3 image links with annotation, threadNumber and isAnnotated columns
3. Annotation_Thread#.csv - 1000 images from Dataset.csv, MTurk Tier 1 input
4. Batch_3998716_batch_results.csv - MTurk Tier 1 output
5. Validation_Thread#.csv - MTurk Tier 2 input
6. Batch_4050706_batch_results.csv - MTurk Tier 2 output
7. Validation_Review_Thread#.csv - Summary of MTurk Tier 2 results
8. AnnotationResultsValidated_Thread#.csv - Approval/Validation csv for MTurk Tier 1 task
9. Annotation_Thread#_updated.csv - Annotation_Thread with annotations filled up

# Data Preparation
This part of repository provides instructions and scripts on 'how-to':<br>
1. Save data in AWS S3
2. Be able to download samples for review
3. Prepare batch dataset ready for annotation
<br>
*To execute some scripts you have to obtain credentials.py file
<br>

## 1. Save data in AWS S3 bucket

On this step you have to create an S3 bucket, upload data in ther and Disable 'Block all public access'.<br>
Optionally if your dataset is not private, then you can follow publishing steps.<br>
Instructions are provided below.<br>

[Basic instruction](https://blog.mturk.com/tutorial-how-to-label-thousands-of-images-using-the-crowd-bea164ccbefc) <br><br>

If you already have S3 bucket with data, follow the steps below:

<img src="S3_Instructions/01_EnablePublicAccess.png" height="640" width="800" title="S3 Enable public access"/><br>
<img src="S3_Instructions/02_InstructionImagesFolder.png" height="640" width="800" title="Publish iamge folder"/><br>
<img src="S3_Instructions/03_checklinks.png" height="640" width="800" title="Test the link"/><br>

Test a link to the file in separate browser and ensure that file is available.<br>

## 2. Be able to download samples for review

Scripts '[01_discover.py](https://github.com/ReconAI/MturkAnnotation/blob/master/0_Prepartion/01_discover.py)' and '[02_imageList.py](https://github.com/ReconAI/MturkAnnotation/blob/master/0_Prepartion/02_imageList.py)' are using [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library to check the contents of S3 bucket and download sample images for visual review.<br>
From visual review you can prepare a document similar to [CamerasAnnotation.xlsx](https://github.com/ReconAI/MturkAnnotation/blob/master/0_Prepartion/result/CamerasAnnotation.xlsx) containig list of all cameras with the classification of their parameters (type of camera, highway/country/road view and etc.)<br>
XSLT file can be exported in [CamerasAnnotation.csv](https://github.com/ReconAI/MturkAnnotation/blob/master/0_Prepartion/result/CamerasAnnotation.csv) for furthere handling using [Pandas](https://pandas.pydata.org/docs/).

## 3. Prepare batch dataset ready for annotation

As mentioned in item #2, [CamerasAnnotation.csv](https://github.com/ReconAI/MturkAnnotation/blob/master/0_Prepartion/result/CamerasAnnotation.csv) can be parsed using [Pandas](https://pandas.pydata.org/docs/) and batches of data can be picked for further processing using '[03_parseAnnotationFile.py](https://github.com/ReconAI/MturkAnnotation/blob/master/0_Prepartion/03_parseAnnotationFile.py)'.<br> 


## ToDo

1. FOLDER PER EACH THREAD 
