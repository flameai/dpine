from django.db import models
from django.conf import settings
import redis
import random
import string


redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

class RedirectedURL(models.Model):
    dt = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    dest_url = models.URLField(verbose_name="конечный адрес")
    user = models.CharField(max_length=32, verbose_name="пользователь - ключ сессии", null=False)
    subpart = models.SlugField(max_length=255, verbose_name="субпарт", unique=True)

    @classmethod
    def create_subpart(cls):
        """
        Возвращает случайный субпарт
        """
        size = 6
        exists = True
        count = 0
        while exists:
            subpart = ''.join(random.choice(string.ascii_uppercase + string.digits +string.ascii_lowercase) for _ in range(size))
            if subpart in ['url', 'static']:
                continue
            exists = cls.objects.filter(subpart=subpart).exists()
            count += 1
            if count > 2:
                size += 1
                count = 0
        return subpart

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        redis_instance.set(self.subpart, self.dest_url)
    
    def delete(self, *args, **kwargs):
        subpart = self.subpart
        super().delete(*args, **kwargs)
        redis_instance.delete(subpart)

    class Meta:
        verbose_name = "редирект"
        verbose_name_plural = "редиректы"