from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    gender_list = (
        ('male', '男'),
        ('female', '女')
    )

    nickname = models.CharField(verbose_name='昵称', max_length=10, blank=True)
    image = models.ImageField(upload_to='', verbose_name='头像', default="media/default.jpg", )
    mobile = models.CharField(verbose_name='手机号', max_length=11, blank=True, null=True)
    gender = models.CharField(verbose_name='性别', max_length=10, choices=gender_list, default="male")
    is_platform = models.BooleanField(verbose_name='是否平台用户', default=False)
    date_of_birth = models.DateField(verbose_name='出生年月', default="2000-1-1")
    country = models.CharField(verbose_name='国家', max_length=50, blank=True, null=True)
    province = models.CharField(verbose_name='省份', max_length=50, blank=True, null=True)
    city = models.CharField(verbose_name='城市', max_length=50, blank=True, null=True)
    address = models.CharField(verbose_name='详细地址', max_length=200, blank=True, null=True)
    remark = models.CharField(verbose_name='备注', max_length=200, null=True, blank=True)
    REQUIRED_FIELDS = ['email', 'is_platform']

    class Meta:
        verbose_name = '会员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return self.username

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.username

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.password = make_password(self.password)
        else:
            if not self.password.startswith('pbkdf2_sha256$'):
                user = User.objects.get(id=self.pk)
                if user.password != self.password:
                    self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)


class MemberManager(models.Manager):

    def get_queryset(self):
        return super(MemberManager, self).get_queryset().filter(is_platform=False)

    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email


class PlatformManager(models.Manager):

    def get_queryset(self):
        return super(PlatformManager, self).get_queryset().filter(is_platform=True)

    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email


class MemberProxy(User):
    objects = MemberManager()

    class Meta:
        proxy = True
        verbose_name_plural = '会员用户'
        verbose_name = verbose_name_plural


class PlatformProxy(User):
    objects = PlatformManager()

    class Meta:
        proxy = True
        verbose_name_plural = '平台管理员'
        verbose_name = verbose_name_plural


class Banner(models.Model):
    title = models.CharField(verbose_name='名称', max_length=200)
    img_url = models.ImageField(verbose_name='图片', upload_to='')

    class Meta:
        verbose_name = '轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(verbose_name='标题', max_length=50)
    zhaiyao = models.CharField(verbose_name='摘要', max_length=500)
    click = models.IntegerField(verbose_name='点击数')
    img_url = models.ImageField(verbose_name='图片链接', upload_to='')
    content = models.TextField(verbose_name='内容')
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '资讯'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class NewsComment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='资讯')
    user_name = models.CharField(verbose_name='匿名用户', max_length=50)
    content = models.CharField(verbose_name='评论', max_length=500)
    add_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name


class PictureType(models.Model):
    title = models.CharField(verbose_name='分类名称', max_length=200)

    class Meta:
        verbose_name = '图片分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Picture(models.Model):
    title = models.CharField(max_length=200, verbose_name='图片标题')
    picture_type = models.ForeignKey(PictureType, verbose_name='图片分类', on_delete=models.CASCADE)
    click = models.IntegerField(verbose_name='点击次数')
    add_time = models.DateTimeField(verbose_name='上传时间', auto_now_add=True)
    img_url = models.ImageField(verbose_name='图片链接', upload_to='')
    zhaiyao = models.CharField(verbose_name='摘要', max_length=500)
    content = models.TextField(verbose_name='详情描述')

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class PictureComment(models.Model):
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, verbose_name='图片')
    user_name = models.CharField(verbose_name='匿名用户', max_length=50)
    content = models.CharField(verbose_name='评论', max_length=500)
    add_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)

    class Meta:
        verbose_name = '图片评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name


class Goods(models.Model):
    title = models.CharField(verbose_name='标题', max_length=50)
    no = models.CharField(verbose_name='商品编号', max_length=200)
    zhaiyao = models.CharField(verbose_name='摘要', max_length=500)
    click = models.IntegerField(verbose_name='点击数')
    img_url = models.ImageField(verbose_name='图片链接', upload_to='')
    content = models.TextField(verbose_name='内容')
    sell_price = models.CharField(verbose_name='售价', max_length=20)
    market_price = models.CharField(verbose_name='定价', max_length=20)
    stock_quantity = models.IntegerField(verbose_name='库存数量')
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class GoodsImage(models.Model):
    goods = models.ForeignKey(Goods, verbose_name='商品', on_delete=models.CASCADE)
    img_url = models.ImageField(verbose_name='图片链接', upload_to='')
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.__str__()


class GoodsComment(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    user_name = models.CharField(verbose_name='匿名用户', max_length=50)
    content = models.CharField(verbose_name='评论', max_length=500)
    add_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)

    class Meta:
        verbose_name = '商品评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name


class GoodsPresentation(models.Model):
    goods = models.ForeignKey(Goods, verbose_name='商品', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=200)
    content = RichTextUploadingField(verbose_name='图文介绍')

    class Meta:
        verbose_name = '商品图文介绍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ShopCar(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name='商品', on_delete=models.CASCADE)
    nums = models.IntegerField(verbose_name='数量', default=0)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return "%s(%d)".format(self.goods.title, self.nums)


class Product(models.Model):
    name = models.CharField(verbose_name='品牌', max_length=200)
    ctime = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    click = models.IntegerField(verbose_name='点击次数')
    add_time = models.DateTimeField(verbose_name='上传时间', auto_now_add=True)
    url = models.FileField(verbose_name='视频链接', upload_to='')
    content = models.TextField(verbose_name='简介')

    class Meta:
        verbose_name = '视频专区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class EmailCode(models.Model):
    code = models.CharField(max_length=10, verbose_name="验证码")
    email = models.EmailField(verbose_name='邮箱')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
