# AWS Transcribe Audio Script

Simple Python script to transcribe  MP3 audio files using AWS Transcribe. Automatically handles S3 upload, job creation, waiting, and downloading results as both JSON and plain text.

## Features

- Automatic bucket creation if missing
- Speaker identification (up to 5 speakers)
- Outputs clean TXT transcript + full JSON with timestamps/confidence scores
- Single command usage with MP3 file path


## Prerequisites

- Python 3.6+
- AWS account with Transcribe permissions
- Configured AWS credentials (`aws configure` or environment variables `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)


## Installation

```bash
pip install boto3
```


## Usage

```bash
python transcribe.py audio.mp3
```

**Parameters:**

- `mp3_file` (required): Path to your MP3 file
- `--output ./transcripts` (optional): Output directory (default: `./transcripts`)

**Example output files:**

```
./transcripts/
├── audio.mp3.json    # Full AWS JSON with speakers, timestamps, confidence
└── audio.mp3.txt     # Clean concatenated Czech text
```


## How It Works

1. Creates/finds S3 bucket `YOUR_BUCKET`
2. Uploads MP3 to `s3://YOUR_BUCKET/audio/[filename]`
3. Starts AWS Transcribe job with Czech language + speaker labels
4. Polls status every 10s until completion
5. Downloads JSON transcript and extracts plain text

## Costs

- ~\$0.024 per audio minute (first 60min/month free tier)
- S3 storage negligible for temporary files


## Customization

Edit these constants at the top of `transcribe.py`:

```python
BUCKET_NAME = "YOUR_BUCKET"
LANGUAGE_CODE = "cs-CZ"  # en-US, de-DE, etc.
REGION = "eu-central-1"
```

For more speakers: change `"MaxSpeakerLabels": 5`

## IAM Permissions Required

```
AmazonTranscribeFullAccess
AmazonS3FullAccess  # Or create minimal policy for your bucket
```


## Troubleshooting

- **"Access Denied"**: Check AWS credentials and IAM permissions
- **"Bucket exists in another region"**: Delete existing bucket or change `BUCKET_NAME`
- **Poor Czech accuracy**: Ensure clear audio, single speaker preferred
- **Job timeout**: Long files (>4h) need `MediaSampleRateHertz` parameter


## Example Output

**transcript.txt:**

```
Mluvčí 1: Dobrý den, vítejte na schůzce.
Mluvčí 2: Děkuji, pojďme začít s agendou.
```


## License

MIT - use freely for personal/commercial projects.

