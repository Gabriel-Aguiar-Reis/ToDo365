from django.contrib import admin

from .models import Task, User

admin.site.register([User, Task])