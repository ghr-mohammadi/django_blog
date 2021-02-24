from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import *


@admin.register(BlogUser)
class BlogUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    fieldsets[1][1]['fields'] += ('phone_number', 'image')
    # readonly_fields = ['groups']

    # def save_model(self, request, obj, form, change):
    #     positions = {'normal': 'ساده', 'writer': 'نویسنده', 'editor': 'ویرایشگر', 'manager': 'مدیر'}
    #     for key, value in positions.items():
    #         Group.objects.get(name=value).user_set.remove(obj)
    #     if form.is_valid():
    #         position = positions[form.cleaned_data['position']]
    #         group = Group.objects.get(name=position)
    #         group.user_set.add(obj)
    #         obj.groups.clear()
    #         obj.groups.add(group)
    #
    #     super().save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['like_qty', 'dislike_qty']
    filter_horizontal = ['tags']


# @admin.register(PostLike)
# class PostLikeAdmin(admin.ModelAdmin):
#     readonly_fields = ['user', 'value', 'instance']
#
#
# @admin.register(CommentLike)
# class CommentLikeAdmin(admin.ModelAdmin):
#     readonly_fields = ['user', 'value', 'instance']


admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Category)
# admin.site.register(PostLike)
# admin.site.register(CommentLike)
