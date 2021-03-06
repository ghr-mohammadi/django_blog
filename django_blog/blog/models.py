from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


# from django.db.models.signals import pre_delete
# from django.dispatch import receiver


def profile_user_path(instance, filename):
    return f'profile/user_{instance.id}/{filename}'


class BlogUser(AbstractUser):
    phone_number = models.CharField(verbose_name='شماره تلفن', validators=[RegexValidator(regex='0[1-9][0-9]{9}', message='شماره تلفن وارد کنید')], max_length=11, blank=True)
    image = models.ImageField(verbose_name='تصویر پروفایل', upload_to=profile_user_path, blank=True)

    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['first_name', 'last_name', 'phone_number', 'image']

    class Meta:
        verbose_name = 'وبلاگ نویس'
        verbose_name_plural = 'وبلاگ نویسان'
        ordering = ['-date_joined']


class AbstractText(models.Model):
    accept_values = [(False, 'تایید نمی‌کنم'), (True, 'تایید می‌کنم')]
    active_values = [(False, 'غیرفعال'), (True, 'فعال')]

    creator = models.ForeignKey(BlogUser, verbose_name='نویسنده', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='متن')
    is_accepted = models.BooleanField(verbose_name='تایید کردن', choices=accept_values, default=accept_values[0][0])
    is_activated = models.BooleanField(verbose_name='وضعیت فعالیت', choices=active_values, default=active_values[0][0])
    create_datetime = models.DateTimeField(verbose_name='زمان ایجاد', auto_now_add=True)
    like_qty = models.IntegerField(verbose_name='تعداد پسندیدن', default=0)
    dislike_qty = models.IntegerField(verbose_name='تعداد نپسندیدن', default=0)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(verbose_name='دسته‌بندی', max_length=80, unique=True)
    parent = models.ForeignKey('self', verbose_name='زیر مجموعه', on_delete=models.CASCADE, null=True, blank=True)
    creator = models.ForeignKey(BlogUser, verbose_name='نویسنده', null=True, blank=True, on_delete=models.SET_NULL)

    # def delete(self, *args, **kwargs):
    #     if self.parent:
    #         for post in Post.objects.filter(category=self):
    #             post.category = self.parent
    #             post.save()
    #     else:
    #         for post in Post.objects.filter(category=self):
    #             post.delete()
    #     super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'


class Tag(models.Model):
    name = models.CharField(verbose_name='تگ', max_length=80, unique=True)
    creator = models.ForeignKey(BlogUser, verbose_name='نویسنده', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"


def get_patent():
    pass


def post_user_path(instance, filename):
    return f'post/user_{instance.creator.id}/{filename}'


class Post(AbstractText):
    title = models.CharField(verbose_name='عنوان', max_length=250)
    category = models.ForeignKey(Category, verbose_name='دسته‌بندی', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='تگ‌ها')
    image = models.ImageField(verbose_name='تصویر پست', upload_to=post_user_path, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"
        ordering = ['-create_datetime']


class Comment(AbstractText):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='پست')

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت‌ها"
        ordering = ['create_datetime']


class Like(models.Model):
    values = [(True, 'like'), (False, 'dislike')]
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name='وبلاگ نویس')
    value = models.BooleanField(verbose_name='مقدار', choices=values, default=values[0][0])

    class Meta:
        abstract = True


class PostLike(Like):
    instance = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='پست')

    class Meta:
        verbose_name = "پست‌لایک"
        verbose_name_plural = "پست‌لایک‌ها"
        unique_together = ("user", "instance")


class CommentLike(Like):
    instance = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='کامنت')

    class Meta:
        verbose_name = "کامنت‌لایک"
        verbose_name_plural = "کامنت‌لایک‌ها"
        unique_together = ("user", "instance")
