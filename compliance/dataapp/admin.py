from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.User)

admin.site.register(models.Post)

# @admin.register(models.Post)
# class CommentAdmin(admin.ModelAdmin):
#     list_display=('name', 'email', 'post', 'created', 'active')
#     list_filter = ('active', 'created', 'updated')
#     search_fields = ('name', 'email', 'body')