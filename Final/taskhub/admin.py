from django.contrib import admin
from taskhub.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Board)
admin.site.register(Note)
admin.site.register(Task)
