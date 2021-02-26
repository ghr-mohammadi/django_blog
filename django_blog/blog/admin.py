from functools import reduce
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import *


class CommentInLine(admin.TabularInline):
    fields = ['creator', 'text', 'is_accepted', 'is_activated', 'like_qty', 'dislike_qty']
    model = Comment
    extra = 0
    readonly_fields = ['creator', 'like_qty', 'dislike_qty']
    model.__str__ = lambda self: ''


class PostFilter(admin.SimpleListFilter):
    title = 'وضعیت تاییده پست‌ها'
    parameter_name = 'post_is_accepted'

    def lookups(self, request, model_admin):
        return [(True, 'پست‌های تایید شده'), (False, 'پست‌های در انتظار تایید')]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        return queryset.filter(is_accepted=self.value())


class CommentFilter(admin.SimpleListFilter):
    title = 'وضعیت تاییده کامنت‌ها'
    parameter_name = 'comment_is_accepted'

    def lookups(self, request, model_admin):
        return [('all_accepted', 'تمام کامنت‌ها تایید شده‌اند'), ('not_accepted', 'دارای کامنت تایید نشده'), ('empty', 'بدون کامنت')]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()

        without_comment = queryset.none()
        for q in queryset.all():
            q_comment_set = {comment.is_accepted for comment in q.comment_set.all()}
            if not q_comment_set:
                without_comment |= queryset.filter(id=q.id)

        if self.value() == 'empty':
            return without_comment
        elif self.value() == 'all_accepted':
            return_queryset = queryset.none()
            for q in queryset.all().difference(without_comment):
                if reduce((lambda x, y: x and y), {comment.is_accepted for comment in q.comment_set.all()}):
                    return_queryset |= queryset.filter(id=q.id)
            return return_queryset
        else:
            return_queryset = queryset.none()
            for q in queryset.all().difference(without_comment):
                if not reduce((lambda x, y: x and y), {comment.is_accepted for comment in q.comment_set.all()}):
                    return_queryset |= queryset.filter(id=q.id)
            return return_queryset


@admin.register(BlogUser)
class BlogUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    fieldsets[1][1]['fields'] += ('phone_number', 'image')
    filter_horizontal = ['user_permissions']

    class Media:
        js = ['/static/js/jquery-3.5.1.min.js', '/static/js/extra_script.js']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['creator', 'title', 'text', 'image', 'category', 'tags', 'is_accepted', 'is_activated', 'like_qty', 'dislike_qty']
    readonly_fields = ['like_qty', 'dislike_qty']
    filter_horizontal = ['tags']
    inlines = [CommentInLine]
    list_filter = [PostFilter, CommentFilter]


admin.site.register(Tag)
admin.site.register(Category)
