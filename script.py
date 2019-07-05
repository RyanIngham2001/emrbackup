from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil
from datetime import datetime

TIME = datetime.now()

gauth = GoogleAuth()
gauth.LoadCredentialsFile("creds.txt")

if not gauth.credentials:
    gauth.LocalWebserverAuth()

elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("creds.txt")

drive = GoogleDrive(gauth)
new_file_name = "emrbackup_{}".format(TIME)
shutil.make_archive(new_file_name, 'zip', 'xampp')
xampp_archive = drive.CreateFile(metadata={'title': new_file_name})
xampp_archive.Upload()



