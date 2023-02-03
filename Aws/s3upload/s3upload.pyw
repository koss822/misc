# pip install -r .\requirements.txt --user
import boto3
from pathlib import PureWindowsPath
import sys
import PySimpleGUI as sg

BUCKET = "YOUR_BUCKET"

def upload_to_s3(file_path):
    s3 = boto3.resource("s3")
    object_name = f"public/{fpath.name}"
    s3.Bucket(BUCKET).upload_file(fpath, object_name)
    s3.ObjectAcl(BUCKET, object_name).put(ACL="public-read")
    bucket_location = boto3.client('s3').get_bucket_location(Bucket=BUCKET)
    return f"https://s3-{bucket_location['LocationConstraint']}.amazonaws.com/{BUCKET}/{object_name}"

def copyurl(url):
    layout = [  [sg.Text('S3 uploaded file url')],
                [sg.InputText(url, use_readonly_for_disable=True, disabled=True, key='-IN-')],
                [sg.Button('Ok')]  ]

    window = sg.Window('S3 Upload', layout, finalize=True)

    while True:             # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Ok':
            break

    window.close()

if __name__ == "__main__":
    fpath = PureWindowsPath(sys.argv[1])
    copyurl(upload_to_s3(fpath))