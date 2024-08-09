# S3 Upload utility

### Description
This simple python utility will add right-click context menu to every file to upload it to S3 and make it public. Once you click on the file it will be uploaded and you will be provided a public link. Usefull for sharing images and other files.

### Screenshot
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/s3upload-context-menu.png "S3 Upload context menu")
![Screenshot](https://github.com/koss822/misc/raw/master/imgs/s3upload-dialog.png "S3 Upload dialog")

### Installation
1. Edit bucket in s3upload.pyw
2. Under Administrator run "pip install -r requirements.txt"
3. Edit paths in right-click-menu.reg
4. Edit bucket variable in s3upload.pyw
5. Import registry file
6. Make sure you have correctly filed credentials in .aws in your home directory