from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import io
import os

from PIL import Image
from PIL import ImageDraw

CLIENT_SECRET_FILE = 'client_secrets.json'

from oauth2client import service_account

from google.cloud import vision

# Create your views here.

def scanImage(path):
    """Detects faces in an image."""

    vision_client = vision.Client.from_service_account_json(CLIENT_SECRET_FILE)

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    faces = image.detect_faces()

    img = Image.open(path) #first we get the image to draw on
    draw = ImageDraw.Draw(img)
    faceNumber = 0
    #os.system('mkdir scans')
    #os.system('cd scans')
    for face in faces:
        vertices = face.bounds.vertices

        coords = []
        for vertice in vertices:
            c = (vertice.x_coordinate, vertice.y_coordinate) #we make a tuple coordinate object
            if (c[1] != None):
                coords.append(c) #and we add it to the array

        #now we have a polygon, so we draw
        if (len(coords) == 4): #if we did indeed get a rectangle
            draw.polygon(coords, outline=(255,255,255,255))
            name = "face_" + str(faceNumber)
            #crop(img, coords, name)
    img.save(path)
    faceNumber += 1


def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.path(filename)
        scanImage(uploaded_file_url)


        return render(request, 'index/result.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'index/upload.html')
