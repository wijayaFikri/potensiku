from django.contrib import admin
from .models import *
admin.site.register(Question)
admin.site.register(Participant)
admin.site.register(Answer)
admin.site.register(Token)
admin.site.register(Person)

# Register your models here.
