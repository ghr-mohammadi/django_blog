from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils import timezone


class BlogUser(AbstractBaseUser):
    positions = [
        ('normal', 'ساده'),
        ('writer', 'نویسنده'),
        ('editor', 'ویراستار'),
        ('manager', 'مدیر')
    ]

    first_name = models.CharField(verbose_name='نام', max_length=80)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=80)
    email = models.EmailField(verbose_name='ایمیل', max_length=120, unique=True)
    username = models.CharField(verbose_name='نام کاربری', max_length=80, unique=True)
    password = models.TextField(verbose_name='رمز ورود')
    phone_number = models.CharField(validators=[RegexValidator(regex='09[0-9]{9}', message='شماره موبایل وارد کنید')], max_length=11)
    image = models.ImageField(verbose_name='تصویر پروفایل', upload_to='profile/')
    position = models.CharField(verbose_name='رده کاربر', max_length=8, choices=positions, default=positions[0][0])

    class Meta:
        verbose_name = 'وبلاگ نویس'
        verbose_name_plural = 'وبلاگ نویسان'


def user_directory_path(instance, filename):
    return 'post/user_{0}/{1}'.format(instance.user.id, filename)


class Post(models.Model):
    creator_id = models.OneToOneField(BlogUser, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='متن')
    category = models.CharField(verbose_name='دسته‌بندی', max_length=80)
    category_full = models.TextField(verbose_name='دسته‌بندی - نام کامل')
    status = models.BooleanField(verbose_name='وضعیت', default=False)
    create_time = models.DateTimeField(verbose_name='زمان ایجاد', default=timezone.now)
    parent_post = models.OneToOneField('Post', on_delete=models.CASCADE, null=True)
    tag = models.ManyToManyField('Tag', through='TagPost')
    image = models.ImageField(verbose_name='تصویر پست', upload_to=user_directory_path, null=True)
    like_qty = models.IntegerField(verbose_name='تعداد پسندیدن', default=0)
    dislike_qty = models.IntegerField(verbose_name='تعداد نپسندیدن', default=0)

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"


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
    values = [
        ('null', 0),
        ('like', 1),
        ('dislike', -1)
    ]

    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name='وبلاگ نویس')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='پست')
    value = models.IntegerField(verbose_name='مقدار', choices=values, default=values[0][0])

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک‌ها"
        unique_together = ("user", "post")

# class Edit(models.Model):
