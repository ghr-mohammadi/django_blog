from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


def profile_user_path(instance, filename):
    return f'profile/user_{instance.id}/{filename}'


class BlogUser(AbstractUser):
    positions = [('normal', 'ساده'), ('writer', 'نویسنده'), ('editor', 'ویراستار'), ('manager', 'مدیر')]

    phone_number = models.CharField(verbose_name='شماره تلفن', validators=[RegexValidator(regex='0[1-9][0-9]{9}', message='شماره تلفن وارد کنید')], max_length=11, blank=True)
    position = models.CharField(verbose_name='رده کاربر', max_length=8, choices=positions, default=positions[0][0], blank=True)
    image = models.ImageField(verbose_name='تصویر پروفایل', upload_to=profile_user_path, blank=True)

    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['first_name', 'last_name', 'phone_number', 'position', 'image']

    class Meta:
        verbose_name = 'وبلاگ نویس'
        verbose_name_plural = 'وبلاگ نویسان'


class Category(models.Model):
    name = models.CharField(verbose_name='دسته‌بندی', max_length=80, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'


class AbstractText(models.Model):
    accept_values = [(False, 'تایید نمی‌کنم'), (True, 'تایید می‌کنم')]
    active_values = [(False, 'غیرفعال'), (True, 'فعال')]

    creator = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='متن')
    is_accepted = models.BooleanField(verbose_name='تایید کردن', choices=accept_values, default=accept_values[0][0])
    is_activated = models.BooleanField(verbose_name='وضعیت فعالیت', choices=active_values, default=active_values[0][0])
    create_datetime = models.DateTimeField(verbose_name='زمان ایجاد', auto_now_add=True)
    like_qty = models.IntegerField(verbose_name='تعداد پسندیدن', default=0)
    dislike_qty = models.IntegerField(verbose_name='تعداد نپسندیدن', default=0)

    class Meta:
        abstract = True


def get_patent(*args):
    for arg in args:
        print(f'{arg}: {type(arg)}')
    return Category.objects.get(name="سایر", parent=None)


def post_user_path(instance, filename):
    return f'post/user_{instance.id}/{filename}'


class Post(AbstractText):
    title = models.CharField(verbose_name='عنوان', max_length=80)
    category = models.ForeignKey(Category, on_delete=models.SET(get_patent))
    tag = models.ManyToManyField('Tag', through='TagPost')
    image = models.ImageField(verbose_name='تصویر پست', upload_to=post_user_path, null=True, blank=True)

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"


class Comment(AbstractText):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='پست')

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت‌ها"


class Tag(models.Model):
    name = models.CharField(verbose_name='تگ', max_length=80)

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"


class TagPost(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='تگ')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='پست')

    class Meta:
        verbose_name = "تگ-پست"
        verbose_name_plural = "تگ-پست‌ها"
        unique_together = ("tag", "post")


class Like(models.Model):
    values = [(0, 'null'), (1, 'like'), (-1, 'dislike')]
    user = models.OneToOneField(BlogUser, on_delete=models.CASCADE, verbose_name='وبلاگ نویس')
    post = models.OneToOneField(Post, on_delete=models.CASCADE, verbose_name='پست')
    value = models.IntegerField(verbose_name='مقدار', choices=values, default=values[0][0])

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک‌ها"
        unique_together = ("user", "post")
