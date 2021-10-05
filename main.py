import googledrive

# Path to the service account file
drive = googledrive.GoogleDriveService("credential.json")

# print(drive.upload_file('cyber-securit.jpg'))

for file in drive.file_list():
    print("File Name: %s \t\t File ID: %s" % (file.get('name'), file.get('id')))
    print("Downloading: %s\n" % file.get('webContentLink'))