from django.db import models
from django.contrib.sites.models import Site

# Create your models here.

class RedirectedURL(models.Model):
    dest_url = models.URLField(verbose_name="конечный адрес")
    sessionkey = models.CharField(max_length=32, verbose_name="ключ сессии", null=True)
    subpart = models.SlugField(max_length=255, verbose_name="слаг для внутреннего узнавания", unique=True)