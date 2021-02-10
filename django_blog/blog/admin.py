from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import *


@admin.register(BlogUser)
class BlogUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    fieldsets[1][1]['fields'] += ('phone_number', 'position', 'image')


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
# admin.site.register(TagPost)
admin.site.register(Like)
admin.site.register(Category)
