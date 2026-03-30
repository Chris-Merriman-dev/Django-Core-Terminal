from django.contrib import admin
from .models import User, Asset, Comment, Directive
# Register your models here.
admin.site.register(User)
admin.site.register(Asset)
admin.site.register(Comment)
admin.site.register(Directive)
