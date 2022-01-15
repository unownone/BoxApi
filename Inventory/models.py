from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.sites.models import Site
from datetime import datetime
# Create your models here.
class Boxes(models.Model):
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    area = models.IntegerField(null=True,blank=True)
    volume = models.IntegerField(null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_field = models.DateTimeField(default=timezone.now)
    last_updated = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name='last_updated')
    
    def __str__(self):
        return str(self.created_by)+' on '+str(datetime.strftime(self.date_field,'%Y-%m-%d %H:%M:%S'))
    
class Constraints(models.Model):
    A1 = models.IntegerField(default=100)
    V1 = models.IntegerField(default=1000)
    L1 = models.IntegerField(default=100)
    L2 = models.IntegerField(default=50)
    date_field = models.DateTimeField(default=timezone.now())
    Site = models.OneToOneField(Site,on_delete=models.CASCADE)
    