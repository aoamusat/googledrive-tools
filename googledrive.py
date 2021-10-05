from __future__ import print_function
import os, mimetypes
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload


class GoogleDriveService():
    DRIVE_FOLDER_ID = ""
    SCOPES = [
        "https://www.googleapis.com/auth/drive",
    ]
    
    def __init__(self, service_account_file_path):
        # service account file path
        self.service_account_file_path = service_account_file_path
        return None
    
    def __authenticate(self):
        credentials = Credentials.from_service_account_file(
            filename=self.service_account_file_path,
            scopes=self.SCOPES
        )
        return credentials
    
    def __drive(self):
        # Return google drive resource service instance
        DRIVE = build('drive', 'v3', credentials=self.__authenticate())
        return DRIVE

    def file_list(self):
        # Return lists of files in the Google drive account
        results = self.__drive().files().list().execute()
        files = results.get('files', [])
        return files
    
    def download_file(self, file_id):
        file = self.__drive().files().get_media(fileId=file_id).execute()
        return file
    
    def create_folder(self, name):
        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = self.__drive().files().create(
            body=metadata,
            fields='id'
        ).execute()
        
        return folder.get('id')
    
    def upload_file(self, file_path, drive_folder_id=""):
        try:
            filename = os.path.basename(file_path)
            metadata = None
            if(drive_folder_id == ""):
                metadata = {'name': filename}
            else:
                metadata = {
                    'name': filename, 
                    'parents': [drive_folder_id]
                }
                
            mime_type = mimetypes.MimeTypes().guess_type(filename)[0]
            
            media = MediaFileUpload(file_path, mimetype=mime_type)
            file = self.__drive().files().create(
                body=metadata,
                media_body=media,
                fields="id"
            ).execute()
            
            return file.get('id')
        except Exception as e:
            raise e
        pass
    pass
