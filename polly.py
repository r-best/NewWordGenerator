import os
import boto3
import uuid

from typing import Union

S3_BUCKET=os.environ['S3_Bucket']
polly = boto3.client('polly')
s3 = boto3.client('s3')

def getMP3(word: str) -> Union[str, int]:
    try:
        response = polly.synthesize_speech(
            Engine='neural',
            OutputFormat='mp3',
            TextType='ssml',
            Text=f'<phoneme alphabet="ipa" ph="{word}" />',
            VoiceId='Joanna'
        )
        print(response)

        s3_key = f"{uuid.uuid4()}.mp3"
        s3.put_object(
            Body=response['AudioStream'].read(),
            Bucket=S3_BUCKET,
            Key=s3_key
        )

        return f"https://s3.us-east-1.amazonaws.com/phonetics-generator-output/{s3_key}"
    except Exception as e:
        print(e)
        return -1
