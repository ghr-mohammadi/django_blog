from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from blog.models import Category, Post, Comment, Like


def create_other_category():
    Category.objects.get_or_create(name='سایر', parent=None)


def get_group_permissions(group):
    def __get_simple_permissions():
        add_comment_permission = Permission.objects.get(name='Can add کامنت')
        change_comment_permission = Permission.objects.get(name='Can change کامنت')
        delete_comment_permission = Permission.objects.get(name='Can delete کامنت')
        view_comment_permission = Permission.objects.get(name='Can view کامنت')

        add_postlike_permission = Permission.objects.get(name='Can add پست‌لایک')
        change_postlike_permission = Permission.objects.get(name='Can change پست‌لایک')
        delete_postlike_permission = Permission.objects.get(name='Can delete پست‌لایک')
        view_postlike_permission = Permission.objects.get(name='Can view پست‌لایک')

        add_commentlike_permission = Permission.objects.get(name='Can add کامنت‌لایک')
        change_commentlike_permission = Permission.objects.get(name='Can change کامنت‌لایک')
        delete_commentlike_permission = Permission.objects.get(name='Can delete کامنت‌لایک')
        view_commentlike_permission = Permission.objects.get(name='Can view کامنت‌لایک')

        return [
            add_comment_permission, change_comment_permission, delete_comment_permission, view_comment_permission,
            add_postlike_permission, change_postlike_permission, delete_postlike_permission, view_postlike_permission,
            add_commentlike_permission, change_commentlike_permission, delete_commentlike_permission, view_commentlike_permission
        ]

    def __get_writer_permissions():
        add_post_permission = Permission.objects.get(name='Can add پست')
        change_post_permission = Permission.objects.get(name='Can change پست')
        delete_post_permission = Permission.objects.get(name='Can delete پست')
        view_post_permission = Permission.objects.get(name='Can view پست')

        add_tag_permission = Permission.objects.get(name='Can add تگ')
        change_tag_permission = Permission.objects.get(name='Can change تگ')
        delete_tag_permission = Permission.objects.get(name='Can delete تگ')
        view_tag_permission = Permission.objects.get(name='Can view تگ')

        return list(set(__get_simple_permissions() + [
            add_post_permission, change_post_permission, delete_post_permission, view_post_permission,
            add_tag_permission, change_tag_permission, delete_tag_permission, view_tag_permission
        ]))

    def __get_editor_permissions():
        return __get_writer_permissions()

    def __get_manager_permissions():
        add_catrgory_permission = Permission.objects.get(name='Can add دسته‌بندی')
        change_catrgory_permission = Permission.objects.get(name='Can change دسته‌بندی')
        delete_catrgory_permission = Permission.objects.get(name='Can delete دسته‌بندی')
        view_catrgory_permission = Permission.objects.get(name='Can view دسته‌بندی')

        change_userblog_permission = Permission.objects.get(name='Can change وبلاگ نویس')
        delete_userblog_permission = Permission.objects.get(name='Can delete وبلاگ نویس')
        view_userblog_permission = Permission.objects.get(name='Can view وبلاگ نویس')

        return list(set(__get_editor_permissions() + [
            add_catrgory_permission, change_catrgory_permission, delete_catrgory_permission, view_catrgory_permission,
            change_userblog_permission, delete_userblog_permission, view_userblog_permission
        ]))

    if group == Group.objects.get(name='ساده'):
        return __get_simple_permissions()
    elif group == Group.objects.get(name='نویسنده'):
        return __get_writer_permissions()
    elif group == Group.objects.get(name='ویرایشگر'):
        return __get_editor_permissions()
    elif group == Group.objects.get(name='مدیر'):
        return __get_manager_permissions()


class Command(BaseCommand):
    help = 'command for groups creation'

    def handle(self, *args, **options):
        create_other_category()

        simple, created = Group.objects.get_or_create(name='ساده')
        writer, created = Group.objects.get_or_create(name='نویسنده')
        editor, created = Group.objects.get_or_create(name='ویرایشگر')
        manager, created = Group.objects.get_or_create(name='مدیر')

        for group in (simple, writer, editor, manager):
            group.permissions.set(get_group_permissions(group))

        self.stdout.write(self.style.SUCCESS('Groups and Permissions of Groups Successfully created.'))
