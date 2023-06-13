from django.contrib import admin

from publications.models import Publication, Comment

# Register your models here.
admin.site.register(Publication)
admin.site.register(Comment)
