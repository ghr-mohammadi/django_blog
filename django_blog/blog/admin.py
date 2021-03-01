from functools import reduce
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import *

admin.site.site_header = 'مدیریت وبلاگ'
admin.site.site_title = 'مدیریت وبلاگ'
admin.site.index_title = 'مدیریت وبلاگ'


class CommentInLine(admin.TabularInline):
    model = Comment
    fields = ['creator', 'text', 'is_accepted', 'is_activated', 'like_qty', 'dislike_qty']
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
    fieldsets[2][1]['fields'] = ('is_active', 'groups', 'user_permissions')
    filter_horizontal = ['user_permissions']

    def save_model(self, request, obj, form, change):
        if Group.objects.get(name='ویرایشگر') in form.cleaned_data['groups'] or Group.objects.get(name='مدیر') in form.cleaned_data['groups']:
            obj.is_staff = True
        else:
            obj.is_staff = False
        super().save_model(request, obj, form, change)

    class Media:
        js = ['/static/js/jquery-3.5.1.min.js', '/static/js/extra_script.js']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['creator', 'title', 'text', 'image', 'category', 'tags', 'is_accepted', 'is_activated', 'like_qty', 'dislike_qty']
    readonly_fields = ['creator', 'is_activated', 'like_qty', 'dislike_qty']
    filter_horizontal = ['tags']
    inlines = [CommentInLine]
    list_filter = [PostFilter, CommentFilter]
    actions = ['accept_posts', 'accept_comments', 'accept_posts_and_comments']

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'creator'):
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not hasattr(instance, 'creator'):
                instance.creator = request.user
            instance.save()
        super().save_formset(request, form, formset, change)

    def accept_posts(self, request, queryset):
        queryset.update(is_accepted=True)
    accept_posts.short_description = 'تایید پست‌های انتخاب شده'

    def accept_comments(self, request, queryset):
        for q in queryset:
            q.comment_set.update(is_accepted=True)
    accept_comments.short_description = 'تایید کامنت‌های موارد انتخاب شده'

    def accept_posts_and_comments(self, request, queryset):
        queryset.update(is_accepted=True)
        for q in queryset:
            q.comment_set.update(is_accepted=True)
    accept_posts_and_comments.short_description = 'تایید پست‌ها و کامنت‌های موارد انتخاب شده'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ['creator', 'name']
    readonly_fields = ['creator']

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'creator'):
            obj.creator = request.user
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['creator', 'name', 'parent']
    readonly_fields = ['creator']

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'creator'):
            obj.creator = request.user
        super().save_model(request, obj, form, change)
