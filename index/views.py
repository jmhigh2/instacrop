from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import User

from django.http import HttpResponseRedirect, Http404

from oauth2client.contrib.django_orm import Storage
from users.models import CredentialsModel, FlowModel

import io
import os
from oauth2client import client

from PIL import Image
from PIL import ImageDraw

CLIENT_SECRET_FILE = 'client_secrets.json'

from oauth2client import service_account
from google.cloud import vision

GOOGLE_SCOPES = 'https://www.google.com/m8/feeds/'
APPLICATION_NAME = 'Contact Photo'
CLIENT_SECRET_CONTACTS = 'contacts.json'

if os.getcwd() == '/app': #heroku settings
    REDIRECT_URI = 'http://gcphoto.herokuapp.com/auth'
else:
    REDIRECT_URI = 'http://127.0.0.1:8000/auth'


def crop(img, coords, savename):
    #print(coords)
    #print("IMAGE SIZE: " + str(img.size))
    x1 = coords[0][0]
    y1 = coords[0][1]
    x2 = coords[2][0]
    y2 = coords[2][1]

    #width = (x2 - x1)
    #height = (y2 - y1)
    #print("X: " + str(x1))
    #print("Y: " + str(y1))
    #print("HEIGHT: " + str(height))
    #print("WIDTH: " + str(width))
    #print("")
    newImg = img.crop((x1, y1, x2, y2))

    newImg.save('media/' + savename)


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
            name = "face_" + str(faceNumber) + ".jpg"
            crop(img, coords, name)
        faceNumber += 1
    img.save("media/totalscan.jpg")
    faceNumber += 1

    return faceNumber


def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        file_url = fs.path(filename)
        number = scanImage(file_url)

        return render(request, 'index/result.html', {
            'filename': 'media/'+ filename, 'number': range(0,number-1)
        })
    return render(request, 'index/upload.html')



def link_google(request):
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_CONTACTS, scope=GOOGLE_SCOPES,
    redirect_uri=REDIRECT_URI)

    flow.user_agent = APPLICATION_NAME
    auth_uri = flow.step1_get_authorize_url()

    user = User.objects.get(username = request.user)
    storage = Storage(FlowModel, 'id', user, 'flow')
    storage.put(flow)

    return HttpResponseRedirect(auth_uri)


def google_auth(request):

    from gdata.contacts import service, client
    import gdata.gauth
    auth_code = request.GET.get('code')

    CLIENT_ID = '59838547405-9e8js0kkmsgahjhfq220s6o3cd4n7lmm.apps.googleusercontent.com'  # Provided in the APIs console
    CLIENT_SECRET = 'zqUU0Tnu-RPA73qZQcXUsccF'  # Provided in the APIs console
    SCOPE = 'https://www.google.com/m8/feeds'
    USER_AGENT = 'dummy'

    auth_token = gdata.gauth.OAuth2Token(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    scope=SCOPE, user_agent=USER_AGENT)

    user = User.objects.get(username = request.user)

    import atom.http_core

    redirect_url = REDIRECT_URI + '?code='+ auth_code
    print redirect_url

    url = atom.http_core.ParseUri(redirect_url)
    print url.query
    auth_token.redirect_uri = REDIRECT_URI
    auth_token.get_access_token(url.query)

    gd_client = gdata.contacts.client.ContactsClient(source='Contact Photo')
    auth_token.authorize(gd_client)

    feed = gd_client.GetContacts()
    print feed



    return render(request, 'users/success.html')
