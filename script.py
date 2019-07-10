from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil
from datetime import datetime
import os

TIME = datetime.now()

# authenticate google drive API
gauth = GoogleAuth()
gauth.LoadCredentialsFile("creds.txt")

# create new creds.txt so manual auth not required every time
if not gauth.credentials:
    gauth.LocalWebserverAuth()

elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("creds.txt")

# initialise drive file
drive = GoogleDrive(gauth)
new_file_name = "emrbackup_{}".format(TIME)

# create a copy of the xampp folder for permission reasons 
try:
    shutil.copytree('xampp', 'xampp_copy')
    shutil.make_archive(new_file_name, 'zip', 'xampp_copy')
except FileNotFoundError:
    print("ERROR: Xampp folder is not found. Please make sure this script is executing in the same directory as Xampp.\nPress ENTER to quit.")
    stop_code = input()
    quit()

# upload file
xampp_archive = drive.CreateFile(metadata={'title': new_file_name})
xampp_archive.Upload()

# clean up directory
shutil.rmtree('xampp_copy')
os.remove('emrbackup_{}'.format(TIME))


