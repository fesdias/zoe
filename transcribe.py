import os
import pandas as pd
import time
import boto3

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

transcribe = boto3.client('transcribe', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name = 'sa-east-1')

def check_job_name(job_name):
  job_verification = True
  # all the transcriptions
  existed_jobs = transcribe.list_transcription_jobs()
  for job in existed_jobs['TranscriptionJobSummaries']:

    if job_name == job['TranscriptionJobName']:
      job_verification = False
      break

  if job_verification == False:
    transcribe.delete_transcription_job(TranscriptionJobName=job_name)

  return job_name

def s3toTranscribe(file_name, file_Add):

  job_name = (file_name.split('.')[0]).replace(" ", "")  
  file_format = 'mp4'

  job_name = check_job_name(job_name)
  transcribe.start_transcription_job(
      TranscriptionJobName=job_name,
      Media={'MediaFileUri': file_Add},
      MediaFormat = file_format,
      LanguageCode='pt-BR')
  
  while True:
    result = transcribe.get_transcription_job(TranscriptionJobName=job_name)

    if result['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break

    time.sleep(15)

  if result['TranscriptionJob']['TranscriptionJobStatus'] == "COMPLETED":
    data = pd.read_json(result['TranscriptionJob']['Transcript']['TranscriptFileUri'])
    return data

  return False


  
