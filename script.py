from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil
from datetime import datetime
import os

TIME = datetime.now()

print("EMR Backup script.\nDo not close this script if manually backing up.\nIf there are any errors, contact Ryan at ryaningham2001@gmail.com\n or see the GitHub repo at https://www.github.com/RyanIngham2001/emrbackup")

# authenticate google drive API
gauth = GoogleAuth()
gauth.LoadCredentialsFile("creds.txt")

# create new creds.txt so manual auth not required every time
if not gauth.credentials:
    print("Unrecognised device. Please authorise on Google.")
    gauth.LocalWebserverAuth()

elif gauth.access_token_expired:
    print("Credentials for this device have expired.")
    gauth.Refresh()
else:
    print("Valid authorisation credentials.")
    gauth.Authorize()

print("Saving OAuth credentials...")
gauth.SaveCredentialsFile("creds.txt")

# initialise drive file
drive = GoogleDrive(gauth)
new_file_name = "emrbackup_{}".format(TIME)

# create a copy of the xampp folder for permission reasons 
try:
    print("Copying Xampp folder. This may take some time...")
    shutil.copytree('xampp', 'xampp_copy')
    print("Creating archive. This may take some time...")
    shutil.make_archive(new_file_name, 'zip', 'xampp_copy')
except FileNotFoundError:
    print("ERROR: Xampp folder is not found. Please make sure this script is executing in the same directory as Xampp.\nPress ENTER to quit.")
    stop_code = input()
    quit()

# upload file
xampp_archive = drive.CreateFile(metadata={'title': new_file_name})
print("Uploading archive...")
xampp_archive.Upload()
print("EMR has successfully been backed up to Google Drive.")

# clean up directory
shutil.rmtree('xampp_copy')
os.remove('emrbackup_{}'.format(TIME))


