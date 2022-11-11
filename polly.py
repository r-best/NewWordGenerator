import os
import boto3

S3_BUCKET=os.environ['S3_Bucket']
polly = boto3.client('polly')

def getMP3(word: str) -> None:
    try:
        response = polly.start_speech_synthesis_task(
            Engine='neural',
            OutputFormat='mp3',
            OutputS3BucketName=S3_BUCKET,
            TextType='ssml',
            Text=f'<phoneme alphabet="ipa" ph="{word}" />',
            VoiceId='Joanna'
        )
        print(response)
        return response["SynthesisTask"]["OutputUri"]
    except Exception as e:
        print(e)
        return -1
