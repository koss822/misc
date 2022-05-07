import json
import gzip
from json.decoder import JSONDecodeError
import boto3
import requests
from pathlib import Path


def lambda_handler(event, context):
    url = "http://bulk.openweathermap.org/sample/daily_14.json.gz"
    tmpFile = "daily_14.json.gz"
    htmlFile = "msd.html"
    bucket = "s3.enigma14.eu"
    tmpDir = "/tmp/"

    # Download file
    r = requests.get(url)
    filename = Path(tmpDir + tmpFile)
    filename.write_bytes(r.content)
    print("Downloading file...")

    # Upload file to S3
    s3 = boto3.client('s3')
    with open(tmpDir + tmpFile, "rb") as f:
        s3.upload_fileobj(f, bucket, tmpDir + tmpFile)
    print("Uploading file...")

    def load_data(mystr):
        splitted = mystr.split('\n')
        for e in splitted:
            try:
                yield json.loads(e)
            except GeneratorExit:
                raise GeneratorExit
            except:
                pass

    print("Reading GZIP/JSON file...")
    with gzip.open(tmpDir + tmpFile, 'r') as jsgz:
        json_bytes = jsgz.read()
    json_str = json_bytes.decode('utf-8')

    print("Loading data...")
    data = load_data(json_str)

    print("Searching...")
    for line in data:
        if line["city"]["name"] == "Prague":
            clouds = line["data"][0]["clouds"]
            break

    print("Generating ...")
    htmlclouds = ""
    for i in range(int(clouds)):
        htmlclouds += "<img src=\"http://s3.enigma14.eu/msd/cloud-icon-small.png\" />"

    html = f"""
    <html><body>
    <h2>Prague</h2>
    <h3>Clouds: {clouds}</j3>
    <hr />
    {htmlclouds}
    </body></html>
    """

    with open(tmpDir + htmlFile, "w") as hfile:
        hfile.write(html)

    with open(tmpDir + htmlFile, "rb") as f:
        s3.upload_fileobj(f, bucket, htmlFile)
