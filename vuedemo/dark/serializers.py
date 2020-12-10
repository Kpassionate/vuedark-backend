# _*_ coding:utf-8 _*_
import random
import re
import string
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from dark.models import Product, Banner, News, Picture, Goods, NewsComment, PictureType, ShopCar, GoodsComment, \
    GoodsPresentation, Video, PictureComment, GoodsImage, User, EmailCode
from vuedemo.settings import REGEX_EMAIL

__author__ = "super.gyk"


class SendEmailSerializer(serializers.Serializer):
    """
    邮件
    """
    email = serializers.CharField(required=True, max_length=50)

    def validate_email(self, email):
        """
        验证邮箱
        :param email:
        :return:
        """
        # 邮箱是否注册
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError("该邮箱已被注册")

        # 验证手机号码是否合法
        if not re.match(REGEX_EMAIL, email):
            raise serializers.ValidationError("邮箱格式错误")
        # 验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if EmailCode.objects.filter(add_time__gt=one_minutes_ago, email=email).count():
            raise serializers.ValidationError("请一分钟后再次发送")

        return email


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "nickname", "image", "mobile", "email", "date_of_birth", "gender",
                  "country", "province", "city", "address")
        read_only_fields = ("username",)


class RegisterSerializer(ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def random_str(self):
        u_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        username_str = 'lr-' + u_str
        if User.objects.filter(username=username_str).count():
            return self.random_str()
        return username_str

    def create(self, validated_data):
        user = super(RegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.username = self.random_str()
        user.save()
        return user

    def validate_code(self, code):

        verify_records = EmailCode.objects.filter(email=self.initial_data["email"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            # 判断验证码是否过期
            three_minutes_ago = datetime.now() - timedelta(hours=0, minutes=3, seconds=0)
            if three_minutes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "email", "code", "password")
        read_only_fields = ('username',)


class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class PictureTypeSerializer(ModelSerializer):
    class Meta:
        model = PictureType
        fields = "__all__"


class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
        fields = "__all__"


class PictureCommentSerializer(ModelSerializer):
    class Meta:
        model = PictureComment
        fields = "__all__"


class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class NewsCommentSerializer(ModelSerializer):
    class Meta:
        model = NewsComment
        fields = "__all__"


class GoodsSerializer(ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"


class GoodsImageSerializer(ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = "__all__"


class GoodsPresentationSerializer(ModelSerializer):
    class Meta:
        model = GoodsPresentation
        fields = "__all__"


class GoodsCommentSerializer(ModelSerializer):
    class Meta:
        model = GoodsComment
        fields = "__all__"


class ShopCarDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = ShopCar
        fields = ("goods", "nums")


class ShopCarSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label="数量", min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于一",
                                        "required": "请选择购买数量"
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShopCar.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShopCar.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"
