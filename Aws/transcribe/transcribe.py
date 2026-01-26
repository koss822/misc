#!/usr/bin/env python3
import sys
import argparse
import boto3
import time
import json
import os
from botocore.exceptions import ClientError

BUCKET_NAME = "YOUR_BUCKET"  # Fixed bucket, auto-created if missing
LANGUAGE_CODE = "cs-CZ"  # Fixed for Czech
REGION = "eu-west-1"

def upload_to_s3(s3_client, bucket, local_file, s3_key):
    try:
        s3_client.upload_file(local_file, bucket, s3_key)
        print(f"Uploaded to s3://{bucket}/{s3_key}")
        return f"s3://{bucket}/{s3_key}"
    except ClientError as e:
        print(f"Upload error: {e}")
        return None

def create_bucket_if_not_exists(s3_client, bucket, region):
    try:
        s3_client.head_bucket(Bucket=bucket)
        print(f"Bucket {bucket} exists.")
    except ClientError:
        s3_client.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f"Created bucket {bucket}")

def start_transcription(transcribe_client, job_name, media_uri, bucket):
    job_args = {
        "TranscriptionJobName": job_name,
        "LanguageCode": LANGUAGE_CODE,
        "Media": {"MediaFileUri": media_uri},
        "OutputBucketName": bucket,
        "Settings": {
            "ShowSpeakerLabels": True,
            "MaxSpeakerLabels": 5  # Adjust based on expected speakers
        }
    }
    try:
        response = transcribe_client.start_transcription_job(**job_args)
        print(f"Started job: {job_name}")
        return response["TranscriptionJob"]["TranscriptionJobName"]
    except ClientError as e:
        print(f"Job start error: {e}")
        return None

def wait_for_completion(transcribe_client, job_name):
    while True:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        print(f"Status: {status}")
        if status in ["COMPLETED", "FAILED"]:
            if status == "COMPLETED":
                uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
                print(f"Transcript ready: {uri}")
                return uri
            else:
                print("Job failed")
                return None
        time.sleep(10)

def download_transcript(s3_client, uri, file_name, output_dir):
    print(f"uri: {uri}")
    # Extract key from S3 URI
    key = uri.split('/', 4)[-1]
    print(f"key: {key}")
    bucket = uri.split('/')[3]
    print(f"bucket: {bucket}")
    local_json = os.path.join(output_dir, f"{file_name}.json")
    local_txt = os.path.join(output_dir, f"{file_name}.txt")
    
    s3_client.download_file(bucket, key, local_json)
    
    # Convert JSON to plain text
    with open(local_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    text = data["results"]["transcripts"][0]["transcript"]
    with open(local_txt, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved: {local_txt}")

def main():
    parser = argparse.ArgumentParser(description="AWS Transcribe Czech MP3 file")
    parser.add_argument("mp3_file", help="Path to MP3 file")
    parser.add_argument("--output", default="./transcripts", help="Output directory")
    args = parser.parse_args()

    if not os.path.exists(args.mp3_file):
        print("File does not exist!")
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)

    s3 = boto3.client('s3', region_name=REGION)
    transcribe = boto3.client('transcribe', region_name=REGION)

    # Ensure bucket exists
    create_bucket_if_not_exists(s3, BUCKET_NAME, REGION)

    # Upload file
    file_name = os.path.basename(args.mp3_file)
    s3_key = f"audio/{file_name}"
    media_uri = upload_to_s3(s3, BUCKET_NAME, args.mp3_file, s3_key)
    if not media_uri:
        sys.exit(1)

    # Start job
    job_name = f"cz-transcribe-{file_name}-{int(time.time())}"
    job_name = start_transcription(transcribe, job_name, media_uri, BUCKET_NAME)
    if not job_name:
        sys.exit(1)

    # Wait and download
    uri = wait_for_completion(transcribe, job_name)
    if uri:
        download_transcript(s3, uri, file_name, args.output)

if __name__ == "__main__":
    main()
