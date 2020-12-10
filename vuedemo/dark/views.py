from random import choice

import django_filters
from django.contrib.auth.backends import ModelBackend
from django.core.mail import send_mail
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, status, permissions, authentication
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from dark.models import Product, Banner, PictureType, Picture, News, Goods, NewsComment, ShopCar, GoodsComment, \
    GoodsPresentation, Video, PictureComment, GoodsImage, User, EmailCode
from dark.serializers import ProductSerializer, BannerSerializer, PictureTypeSerializer, PictureSerializer, \
    NewsSerializer, GoodsSerializer, NewsCommentSerializer, ShopCarSerializer, GoodsCommentSerializer, \
    GoodsPresentationSerializer, VideoSerializer, PictureCommentSerializer, GoodsImageSerializer, SendEmailSerializer, \
    RegisterSerializer, UserSerializer, ShopCarDetailSerializer
from utils.permissions import IsOwnerOrReadOnly
from vuedemo.settings import EMAIL_TITLE, EMAIL_FROM


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            # username、email can login
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SendEmailViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送邮箱验证码
    """
    serializer_class = SendEmailSerializer

    def generate_code(self):
        """
        生成验证code
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        code = self.generate_code()

        # 发送邮件
        title = EMAIL_TITLE
        email_from = EMAIL_FROM
        message = "【神秘空间】您正在激活账户，您的激活码为{code}。如非本人操作，请忽略本邮件".format(code=code)
        send_mail(title, message, email_from, [email])

        try:
            code_record = EmailCode(code=code, email=email)
            code_record.save()
            return Response({
                "email": email,
                "message": "请注意查看激活邮件"
            }, status=status.HTTP_201_CREATED)

        except:
            return Response({
                'message': "请求失败"
            }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):

    serializer_class = RegisterSerializer()
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserSerializer
        elif self.action == "create":
            return RegisterSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["username"] = user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 返回当前用户
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         return User.objects.filter(username=self.request.user)


class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class BannerViewSet(ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class PictureTypeViewSet(ModelViewSet):
    queryset = PictureType.objects.all()
    serializer_class = PictureTypeSerializer


class PictureFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Picture
        fields = ['picture_type']


class PictureViewSet(ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = PictureFilter

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PictureCommentFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = PictureComment
        fields = ['picture']


class PictureCommentViewSet(ModelViewSet):
    queryset = PictureComment.objects.all()
    serializer_class = PictureCommentSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = PictureCommentFilter


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NewsCommentFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = NewsComment
        fields = ['news']


class NewsCommentViewSet(ModelViewSet):
    queryset = NewsComment.objects.all()
    serializer_class = NewsCommentSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = NewsCommentFilter


class GoodsViewSet(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GoodsImageFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = GoodsImage
        fields = ['goods']


class GoodsImageViewSet(ModelViewSet):
    queryset = GoodsImage.objects.all()
    serializer_class = GoodsImageSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsImageFilter


class GoodsCommentFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = GoodsComment
        fields = ['goods']


class GoodsCommentViewSet(ModelViewSet):
    queryset = GoodsComment.objects.all()
    serializer_class = GoodsCommentSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsCommentFilter


class GoodsPresentationFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = GoodsPresentation
        fields = ['goods']


class GoodsPresentationViewSet(ModelViewSet):
    queryset = GoodsPresentation.objects.all()
    serializer_class = GoodsPresentationSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsPresentationFilter


class ShopCarViewSet(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create：
        加入购物车
    delete：
        删除购物记录
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCarSerializer
    lookup_field = "goods_id"

    def perform_create(self, serializer):
        shop_car = serializer.save()
        goods = shop_car.goods
        goods.stock_quantity -= shop_car.nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.stock_quantity += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShopCar.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.stock_quantity -= nums
        goods.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCarDetailSerializer
        else:
            return ShopCarSerializer

    def get_queryset(self):
        return ShopCar.objects.filter(user=self.request.user)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
