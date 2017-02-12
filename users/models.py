from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

from oauth2client.contrib.django_orm import FlowField
from oauth2client.contrib.django_orm import CredentialsField


# Create your models here.
class FlowModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    flow = FlowField()
    #Google API

class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()
