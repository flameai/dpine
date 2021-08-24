from django.db import models

class RedirectedURL(models.Model):
    dt = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    dest_url = models.URLField(verbose_name="конечный адрес")
    user = models.CharField(max_length=32, verbose_name="пользователь - ключ сессии", null=False)
    subpart = models.SlugField(max_length=255, verbose_name="слаг для внутреннего узнавания", unique=True)