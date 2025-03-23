from django.contrib import admin
from forums.models import *

# Register your models here.
admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Comment)
