from django.contrib import admin

from .models import Tarefa, Usuario

admin.site.register([Usuario, Tarefa])
