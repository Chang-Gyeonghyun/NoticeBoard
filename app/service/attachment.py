import io
import os
import secrets
from typing import List
from boto3 import client
import urllib
from fastapi import UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from app.models.models import Attachment
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))    
    
class AttachmentService():    
    def __init__(self):
        self.s3_client = client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
            region_name=os.getenv("AREA")
        )
        self.bucket_name=os.getenv("BUCKET")
        
    async def change_filename(self, file: UploadFile) -> UploadFile:
        ext = os.path.splitext(file.filename)[1]
        random_name = secrets.token_urlsafe(16)
        file.filename = f"{random_name}{ext}"
        return file.filename        
        
    async def upload_to_s3(self, files: List[UploadFile]) -> List[str]:
        screte_name = []
        file_name = []
        for file in files:
            file_name.append(file.filename)
            new_filename = await self.change_filename(file)
            screte_name.append(new_filename)

            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                new_filename,
                ExtraArgs={"ContentType": file.content_type}
            )
        return screte_name, file_name
    
    async def download_file(self, attachment: Attachment):
        ext = attachment.file_name.split('.')[-1]
        s3_response = self.s3_client.get_object(Bucket=self.bucket_name, Key=attachment.file_path)
        file_stream = io.BytesIO(s3_response['Body'].read())
        encoded_filename = urllib.parse.quote(attachment.file_name)
        return StreamingResponse(
            file_stream,
            media_type=f'application/{ext}',
            headers={
                'Content-Disposition': f'attachment; filename*=UTF-8\'\'{encoded_filename}'
            }
        )