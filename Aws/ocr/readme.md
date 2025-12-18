# JPG OCR with Amazon Textract

This project contains a simple Python script that runs OCR (Optical Character Recognition) on all `.jpg` images located in the same directory as the script and saves the recognized text into `.txt` files.

Each image `image.jpg` produces a corresponding `image.txt` file with the extracted text.

## Prerequisites

- Python 3.8+ installed
- An AWS account
- IAM user or role with permissions to use **Amazon Textract**
- AWS credentials configured locally (for example using `aws configure`)
- The `boto3` package installed

### Install dependencies

```
pip install boto3
```

### Configure AWS credentials

You can configure your AWS credentials using the AWS CLI:

```
aws configure
```

You will be prompted for:

- AWS Access Key ID  
- AWS Secret Access Key  
- Default region name (for example: `eu-central-1`)  
- Default output format (optional)

Alternatively, you can set credentials using environment variables such as `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION`.

## How it works

1. The script finds all `.jpg` files in the directory where the script itself is located.
2. For each image, it:
   - Reads the file into memory as bytes.
   - Sends the bytes to Amazon Textract using the `detect_document_text` API.
   - Collects all text blocks of type `LINE`.
3. The recognized text is written to a `.txt` file with the same base name as the image file.

Example:

- `invoice1.jpg` → `invoice1.txt`  
- `scan_2024.jpg` → `scan_2024.txt`

## Usage

1. Copy your `.jpg` files into the same directory as the script.
2. Run the script:

```
python ocr_jpg_textract.py
```

(assuming you saved the script as `ocr_jpg_textract.py`)

3. After the script finishes, you will see new `.txt` files in the same directory with the extracted text.

## Customization

- **Different image extensions**  
  To process other extensions (e.g. `.jpeg` or `.png`), adjust the glob pattern in the script, for example:  
```
jpg_files = sorted(script_dir.glob("*.jpeg"))
```
or use multiple patterns.

- **Recursive processing**  
To process images in subdirectories as well, use:
```
jpg_files = sorted(script_dir.rglob("*.jpg"))
```

- **Single output file**  
If you prefer to combine text from all images into one file, you can open a single output file in the script and append text for each image.

## Notes

- The script uses the synchronous `detect_document_text` API, which is suitable for single-page images such as JPGs.
- For large documents or multi-page PDFs, consider using Textract's asynchronous APIs instead.

