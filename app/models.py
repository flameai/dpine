from django.db import models
from django.contrib.sites.models import Site

# Create your models here.

class RedirectedURL(models.Model):
    dest_url = models.URLField(verbose_name="конечный адрес")
    sid = models.CharField(max_length=100, verbose_name="идентификатор сессии")
    subpart = models.SlugField(max_length=255, verbose_name="слаг для внутреннего узнавания")
    # Создавать будем только для одного сайта, не будем делать Many-to-Many
    sites = models.ForeignKey(Site, verbose_name="сайт", on_delete=models.CASCADE, null=False, blank=False)