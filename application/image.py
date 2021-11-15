import imghdr
import os
import secrets
import filetype
from io import BytesIO

from PIL import Image
from azure.storage.blob import BlobServiceClient, ContentSettings
from decouple import config
from flask import abort
from werkzeug.utils import secure_filename

connect_str = config('AZURE_STORAGE_CONNECTION_STRING')
image_url = config('IMAGE_URL')

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client('$web')

upload_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']


def upload_image(data):
    filename = secure_filename(data.filename)

    file_ext = os.path.splitext(filename)[1].strip('.')

    if file_ext not in upload_extensions and file_ext.lower() not in upload_extensions:
        abort(400)

    image_stream = BytesIO()
    data.save(image_stream)
    image_stream.seek(0)


    kind = filetype.guess(image_stream.read())
    if kind is None:
        print('Cannot guess file type! Abort!')
        abort(400)
    elif kind.extension not in upload_extensions:
        print(f'File extension: {kind.extension}')
        print(f'File MIME type: {kind.mime}')
        print('Wrong extension! Abort!')
        abort(400)
    else:
        print(f'Image {filename} accepted ')
        print(f'File extension: {kind.extension}')
        print(f'File MIME type: {kind.mime}')

    image_stream.seek(0)

    # Check dimensions, if pixels exceed default limit of 178956970 it will error out with DecompressionBombError
    # Also verify with Pillow
    try:
        img = Image.open(image_stream)
        size = img.size
        print(f'Width: {size[0]}')
        print(f'Height: {size[1]}')

        if size[0] > 2000 or size[1] > 2000:
            print('Dimension overflow! Abort!')
            abort(400)
    except:
        print('Cannot get dimensions! Abort!')
        abort(400)

    image_stream.seek(0)

    new_filename = str(secrets.token_urlsafe(16)) + '.' + file_ext
    blob_client = blob_service_client.get_blob_client(container="$web", blob=new_filename)

    mime_type = ContentSettings(content_type='image/' + file_ext)

    blob_client.upload_blob(image_stream.read(), content_settings=mime_type)

    # set IMAGE_URL in .env to return URL for storage account/cname you set to storage account
    url = image_url + new_filename

    return url
