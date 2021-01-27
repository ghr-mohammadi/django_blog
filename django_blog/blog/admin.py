from django.contrib import admin
from .models import *

admin.site.register(BlogUser)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(TagPost)
admin.site.register(Like)
admin.site.register(Edit)
admin.site.register(TagEdit)
