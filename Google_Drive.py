import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

class Driver():
    
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = str()
    relative_path = os.path.dirname(os.path.realpath(__file__))
    
    def __init__(self):
        creds = None
     
        if os.path.exists(os.path.join(self.relative_path, 'token.pickle')):
            with open(os.path.join(self.relative_path, 'token.pickle'), 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(self.relative_path, 'credentials.json'), self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(os.path.join(self.relative_path, 'token.pickle'), 'wb') as token:
                pickle.dump(creds, token)

        # Build the service
        self.service = build('drive', 'v3', credentials=creds)
    
   
    def items(self, parent_id):
        service = self.service

        # Initialize the result list and page token
        all_items_container = []
        next_page_token = None

        while True:
            query = ""
            if parent_id:
                query = f"'{parent_id}' in parents"  # Filter by the given parent ID

            results = service.files().list(
                pageSize=1000,  # Fetch up to 1000 items per request (max allowed)
                pageToken=next_page_token,
                fields="nextPageToken, files(id, name, mimeType, parents, size, createdTime)",
                q=query  # Apply the filter query
                
            ).execute()

            items = results.get('files', [])
            all_items_container.extend(items)  # Add the files/folders to the list
            next_page_token = results.get('nextPageToken')
            
            if not next_page_token:
                break

        return all_items_container

    
    def create_file(self, file_name , folder_id):
        
        service = self.service 
        file_metadata = {'name': file_name,'parents':[folder_id]}    
        file = service.files().create(body=file_metadata, fields='id').execute()
    
    
    def upload_file(self, file_path, folder_id, mime_type='application/octet-stream'):
        service = self.service

        # Set the file metadata
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id] }
        
        media = MediaFileUpload(file_path, mimetype=mime_type)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()


    def download_file(self, file_id, destination_folder):
        service = self.service
        file_metadata = service.files().get(fileId=file_id).execute()
       
        file_name = file_metadata['name']
        destination_path = os.path.join(destination_folder, file_name )
        
        # Download the file
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(destination_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
    
    def delete_file(self, file_id):
        service = self.service
        service.files().delete(fileId=file_id).execute()
        
    def create_folder(self, folder_name, parent_folder_id):
        service = self.service
        
        # Prepare metadata for the new folder
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        # If a parent folder ID is provided, set it as the parent
        if parent_folder_id:
            folder_metadata['parents'] = [parent_folder_id]
        
        # Create the folder
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        

    def delete_folder(self, folder_id):
        service = self.service
        
        try:
            # List all files in the folder to check if it's empty
            query = f"'{folder_id}' in parents"
            results = service.files().list(q=query, fields="files(id)").execute()
            files = results.get('files', [])
            
            if files:
                # Delete all files in the folder first
                for file in files:
                    self.delete_file(file['id'])  # Using the delete_file method to delete files
            
            # Now delete the folder itself
            service.files().delete(fileId=folder_id).execute()        
        except Exception as e:
            print(f"An error occurred: {e}")  
    
    def download_folder(self, folder_id, destination_folder):
        service = self.service
        file_metadata = service.files().get(fileId=folder_id).execute()
        folder_name = file_metadata['name']
        
        os.makedirs(os.path.join(destination_folder,folder_name))
        destination_folder = os.path.join(destination_folder,folder_name)
        
        query = f"'{folder_id}' in parents"
        results = service.files().list(
            q=query, fields="nextPageToken, files(id, name, mimeType)"
        ).execute()
        
        files = results.get('files', [])
        if files:
            for file in files:
                file_id = file['id']
                self.download_file(file_id, destination_folder)
    
    def upload_folder(self, local_folder_path, parent_folder_id):
        service = self.service
        
        # Create a folder in Google Drive
        folder_metadata = {
            'name': os.path.basename(local_folder_path),
            'mimeType': 'application/vnd.google-apps.folder',
            'parents' : [parent_folder_id]
        }
        
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder['id']        
        # Iterate over all files and subfolders in the local folder
        for item in os.listdir(local_folder_path):
            item_path = os.path.join(local_folder_path, item)
            
            if os.path.isdir(item_path):
                # If it's a subfolder, upload it recursively
                self.upload_folder(item_path, folder_id)
            else:
                # If it's a file, upload it
                self.upload_file(item_path, folder_id)  # Call upload_file method to upload files
    
if __name__ == "__main__":
    obj = Driver()
    items = obj.items('1UAQw6zcJXpDza4u7vOyhTQv5L8YDmamU')
    print(items)
    # for file in obj.all_items():
    #     print(file['parents'])