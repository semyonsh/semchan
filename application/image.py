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
set_thumb = False


def upload_image(data):
    global set_thumb
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
    # Create a thumbnail of every image
    try:
        img = Image.open(image_stream)

        size = img.size
        print(f'Width: {size[0]}')
        print(f'Height: {size[1]}')

        if size[0] > 4000 or size[1] > 4000:
            print('Dimension overflow! Abort!')
            abort(400)
    except:
        print('Getting dimensions failed! Abort!')
        abort(400)
        
    thumb_stream = BytesIO()
    # need to refactor this
    try:
        if kind.extension != 'gif':
            if size[0] > 200 or size[1] > 200:
                thumb_size = 200, 200
                img.thumbnail(thumb_size)
                format = 'JPEG' if file_ext.lower() == 'jpg' else file_ext.upper()
                img.save(thumb_stream, format, quality=95)
                set_thumb = True
        else:
            set_thumb = False
    except:
        print('Thumbnailing failed! Abort!')
        abort(400)

    image_stream.seek(0)
    thumb_stream.seek(0)

    image_token = str(secrets.token_urlsafe(16))

    try:
        image_filename = image_token + '.' + file_ext
        blob_client = blob_service_client.get_blob_client(container="$web", blob=image_filename)
        mime_type = ContentSettings(content_type='image/' + file_ext)
        blob_client.upload_blob(image_stream.read(), content_settings=mime_type)
    except:
        abort(404)

    if set_thumb:
        thumb_filename = image_token + '_thmb.' + file_ext
        thumb_url = image_url + thumb_filename
        try:
            blob_client = blob_service_client.get_blob_client(container="$web", blob=thumb_filename)
            mime_type = ContentSettings(content_type='image/' + file_ext)
            blob_client.upload_blob(thumb_stream.read(), content_settings=mime_type)
        except:
            abort(404)
    else:
        thumb_url = None

    # set IMAGE_URL in .env to return URL for storage account/cname you set to storage account
    url = image_url + image_filename

    return url, thumb_url
