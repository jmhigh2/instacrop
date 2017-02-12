from django.db import models

class UploadPicture(models.Model):
    name = models.TextField()

class FacePicture(models.Model):

    id = models.ForeignKey(UploadPicture, primary_key=True)
    name = models.TextField()
