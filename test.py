# qr_generator.py

# Import modules
import os
import qrcode

# Define a function to generate QR codes for files or folders
def generate_qr(path):
    # Create a QR code object with the path as data
    qr = qrcode.QRCode()
    qr.add_data(path)
    qr.make()
    # Create an image from the QR code object
    img = qr.make_image()
    # Save the image with the file name as prefix
    img.save(os.path.basename(path) + "_QR.png")

# Define a function to generate QR codes for websites
def generate_qr_website(url):
    # Create a QR code object with the url as data
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make()
    # Create an image from the QR code object
    img = qr.make_image()
    # Save the image with the website name as prefix
    img.save(url.split("//")[-1] + "_QR.png")

import base64

# Define a function to encrypt an audio file in a QR code
def encrypt_audio(file):
    # Open the audio file in binary mode
    print('a')
    with open(file, "rb") as f:
        # Read the bytes of the file
        data = f.read()
        # Encode the bytes using Base64
        encoded = base64.b64encode(data)
    print('b')
    # Create a QR code object with the encoded data
    qr = qrcode.QRCode()
    qr.add_data(encoded)
    qr.make()
    # Create an image from the QR code object
    img = qr.make_image()
    # Save the image with the file name as prefix
    img.save(file + "_QR.png")

# Define a function to decrypt an audio file from a QR code
def decrypt_audio(file):
    # Open the QR code image
    img = qrcode.Image.open(file)
    # Decode the QR code data using pyzbar
    decoded = pyzbar.decode(img)[0].data
    # Decode the Base64 data
    data = base64.b64decode(decoded)
    # Save the data as an audio file with the same name as the original file
    with open(file.split("_QR")[0], "wb") as f:
        f.write(data)
