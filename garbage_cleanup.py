from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil
from datetime import datetime
import os
import time

# constants
time1 = str(datetime.now())
TIME = time1[0:10]
yy = TIME[0:4]
mm = TIME[5:7]
dd = TIME[8:10]
CURRENT_TIME = time.mktime((int(yy), int(mm), int(dd), 0, 0, 0, 0, 0, 0))
WEEK = 604800


# authenticate google drive API
gauth = GoogleAuth()
gauth.LoadCredentialsFile("creds.txt")

# create new creds so manual auth not required every time
if not gauth.credentials:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("creds.txt")

# list emrbackup files
drive = GoogleDrive(gauth)
file_list = drive.ListFile({"q": "'root' in parents and trashed=false and title contains 'emrbackup'"}).GetList()

# parse returned data to show only file name and unix time

name_list = []
for file in file_list:
    fileID = file['id']
    filename = file['originalFilename']
    fileyear = filename[10:14]
    filemonth = filename[15:17]
    fileday = filename[18:20]
    epoch_time = time.mktime((int(fileyear), int(filemonth), int(fileday), 0, 0, 0, 0, 0, 0))
    
    # if file is older than a week
    if CURRENT_TIME - epoch_time > WEEK:
        file_to_delete = drive.CreateFile({'id': fileID})
        file_to_delete.Trash()
        file_to_delete.Delete()
        print("DELETED {}".format(filename))






