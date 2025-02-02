import os
import uuid
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from django.conf import settings
import qrcode
from django.core.files import File
from django.contrib.auth.decorators import login_required, user_passes_test
from cloudinary.uploader import destroy
from cloudinary.uploader import upload
import cloudinary.uploader

# Eliminar la imagen si existe
       
        

def compress_img(photo, quality = "auto", folder = "", format = "jpg"):  
    result = upload(photo, quality=quality, format=format, folder=folder)
    return result['secure_url']


def delete_img(photo):
    destroy(photo.public_id)

def generate_qr(code):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(code)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    file_name = f'qr_code_{code}.png'
    
    upload_result = cloudinary.uploader.upload(
        buffer,
        public_id=file_name,
        folder="Loans_Qrs",
        transformation={'quality': 'auto:eco'}
    )
    return upload_result['public_id']

def generate_code(length = 10):
    return str(uuid.uuid4()).replace('-', '')[:length]


def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func