from django.shortcuts import render 
import qrcode
from django.core.files.base import ContentFile  # Import ContentFile
from .models import GeneratedImage, DecodeImage
from PIL import Image
from pyzbar.pyzbar import decode
import io
# Create your views here.

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    return img

def home(request):
    if request.method == 'POST':
        myurl = request.POST.get('myurl')
        img = generate_qr_code(myurl)
        
        # Create an in-memory stream to hold the image data
        image_io = io.BytesIO()
        img.save(image_io, format='PNG')  # Save the PIL image to the stream
        
        # Create a ContentFile instance with the image data
        image_file = ContentFile(image_io.getvalue(), name='my_qr_code.png')
        
        # Save the PIL image to the GeneratedImage model's image field
        qr_image = GeneratedImage.objects.create(imag=image_file)
        
        context = {'img': qr_image}

        return render(request, 'index.html', context)  # Return the rendered template

    return render(request, 'index.html')  # Return the rendered template

def decode_qr_code(image_path):
    image = Image.open(image_path)
    decoded_objects = decode(image)
    
    if decoded_objects:
        return decoded_objects[0].data.decode('utf-8')
    else:
        return None

def decodeimg(request):
    context = {'data': None}
    if request.method == 'POST':
        myimg = request.FILES.get('myimg')
        img = DecodeImage(imag=myimg)
        img.save()
        qr_code_path = img.imag.path
        decoded_data = decode_qr_code(qr_code_path)
        
        if decoded_data:
            context['data'] = decoded_data
        else:
            print("No QR code found in the image.")
            print("OKAY")
    return render(request,'decode.html',context)