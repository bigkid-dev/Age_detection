from django.contrib import admin
from .models import ApiModel
# Register your models here.


# class ApiAdmin(admin.ModelAdmin):
#     list = ('image_uri', 'title')



admin.site.register(ApiModel)