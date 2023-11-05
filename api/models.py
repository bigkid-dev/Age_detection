from django.db import models

# Create your models here.
class ApiModel(models.Model):
    image_uri = models.ImageField(upload_to='post_images')
    title = models.TextField(default=True)

    def __str__(self):
        return self.title

   