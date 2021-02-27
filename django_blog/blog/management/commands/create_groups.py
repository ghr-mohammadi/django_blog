from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from blog.models import Category, Post, Comment, Like


def create_other_category():
    Category.objects.get_or_create(name='سایر', parent=None)


def get_group_permissions(group):
    def __get_simple_permissions():
        add_comment_permission = Permission.objects.get(name='Can add کامنت')
        add_postlike_permission = Permission.objects.get(name='Can add پست‌لایک')
        add_commentlike_permission = Permission.objects.get(name='Can add کامنت‌لایک')
        return [add_comment_permission, add_postlike_permission, add_commentlike_permission]

    def __get_writer_permissions():
        add_post_permission = Permission.objects.get(name='Can add پست')
        add_tag_permission = Permission.objects.get(name='Can add تگ')
        change_post_permission = Permission.objects.get(name='Can change پست')
        return list(set(__get_simple_permissions() + [add_post_permission, add_tag_permission, change_post_permission]))

    def __get_editor_permissions():
        change_comment_permission = Permission.objects.get(name='Can change کامنت')
        return list(set(__get_writer_permissions() + [change_comment_permission]))

    def __get_manager_permissions():
        add_catrgory_permission = Permission.objects.get(name='Can add دسته‌بندی')
        change_catrgory_permission = Permission.objects.get(name='Can change دسته‌بندی')
        delete_catrgory_permission = Permission.objects.get(name='Can delete دسته‌بندی')
        change_userblog_permission = Permission.objects.get(name='Can change وبلاگ نویس')
        delete_userblog_permission = Permission.objects.get(name='Can delete وبلاگ نویس')
        return list(set(__get_editor_permissions() + [add_catrgory_permission, change_catrgory_permission,
                                                      delete_catrgory_permission, change_userblog_permission, delete_userblog_permission]))

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
