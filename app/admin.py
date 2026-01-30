from django.contrib import admin
from .models import  Relationship , Gender , State
# Register your models here.
admin.site.register(Gender)
admin.site.register(State)
admin.site.register(Relationship)