from django.db import models

# Create your models here.

class RedirectedURL(models.Model):
    dest_url = models.URLField(verbose_name="конечный адрес")
    user = models.CharField(max_length=32, verbose_name="пользователь - ключ сессии", null=False)
    subpart = models.SlugField(max_length=255, verbose_name="слаг для внутреннего узнавания", unique=True)