import os, secrets, imghdr
from io import BytesIO
from flask import abort
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient, ContentSettings
from decouple import config

connect_str = config('AZURE_STORAGE_CONNECTION_STRING')
image_url = config('IMAGE_URL')

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client=blob_service_client.get_container_client('$web')

upload_extensions = ['.jpg', '.png', '.gif', 'jpeg', 'webp']

#https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

def upload_image(data):
    filename = secure_filename(data.filename)

    file_ext = os.path.splitext(filename)[1]

    if file_ext not in upload_extensions or file_ext != validate_image(data.stream):
        abort(400)

    image_stream = BytesIO()
    data.save(image_stream)
    image_stream.seek(0)

    new_filename = str(secrets.token_urlsafe(16)) +  file_ext 
    blob_client = blob_service_client.get_blob_client(container="$web", blob=new_filename)

    mime_type = ContentSettings(content_type='image/' + file_ext.strip('.'))

    blob_client.upload_blob(image_stream.read(), content_settings=mime_type)

    #set IMAGE_URL in .env to return URL for storage account/cname you set to storage account
    url = image_url + new_filename

    return url