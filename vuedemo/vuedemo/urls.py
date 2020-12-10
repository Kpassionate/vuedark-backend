"""vuedemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from dark.views import ProductViewSet, BannerViewSet, PictureTypeViewSet, PictureViewSet, NewsViewSet, GoodsViewSet, \
    NewsCommentViewSet, ShopCarViewSet, GoodsCommentViewSet, VideoViewSet, PictureCommentViewSet, \
    GoodsImageViewSet, GoodsPresentationViewSet, SendEmailViewSet, UserViewSet
from vuedemo.settings import MEDIA_ROOT

router = routers.DefaultRouter()

router.register('send_email', SendEmailViewSet, base_name='send_email')
router.register('user', UserViewSet, basename='user'),

# router.register('user_info', UserViewSet, base_name='user_info')
router.register('banner', BannerViewSet, base_name='banner')

router.register('picture_type', PictureTypeViewSet, base_name='picture_type')
router.register('picture', PictureViewSet, base_name='picture')
router.register('picture_comment', PictureCommentViewSet, base_name='picture_comment')

router.register('news', NewsViewSet, base_name='news')
router.register('news_comment', NewsCommentViewSet, base_name='news_comment')

router.register('goods', GoodsViewSet, base_name='goods')
router.register('goods_image', GoodsImageViewSet, base_name='goods_image')
router.register('goods_presentation', GoodsPresentationViewSet, base_name='goods_presentation')
router.register('goods_comment', GoodsCommentViewSet, base_name='goods_comment')

router.register('shop_car', ShopCarViewSet, base_name='shop_car')
router.register('product', ProductViewSet, base_name='product')
router.register('video', VideoViewSet, base_name='video')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    url(r'^api/login/$', obtain_jwt_token),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),  # 指定上传媒体位置
]

