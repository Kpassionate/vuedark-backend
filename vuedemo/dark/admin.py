from django.contrib import admin

# Register your models here.
from dark.models import Banner, PictureType, News, NewsComment, Goods, GoodsComment, Picture, PictureComment, \
    ShopCar, Product, Video, GoodsPresentation, GoodsImage, PlatformProxy, MemberProxy


class PlatformProxyAdmin(admin.ModelAdmin):
    """
    平台管理员
    """
    list_display = ("id", "username", "gender", "is_active", "last_login", "email")
    search_fields = ('username', )
    actions = None
    exclude = ('last_login',)

    fieldsets = [
        ('基本信息', {
            'fields': (
                'username', 'password', 'is_staff', 'gender', 'email', 'remark', 'is_platform'
            )
        }),
        ('分组权限', {
            'description': '不同的分组具有不同的权限，每个用户可以属于多个分组，因此获得不同分组的所有权限',
            'fields': (
                'groups',
            )
        }),
        ('是否启用', {
            'description': '用户添加后为避免误操作，不可直接删除，但可以取消启用，则此用户进入停用状态',
            'fields': (
                'is_active',
            )
        })
    ]

    filter_horizontal = ('groups',)


admin.site.register(PlatformProxy, PlatformProxyAdmin)


class MemberProxyAdmin(admin.ModelAdmin):

    list_display = ("id", "username", "nickname", "email", "gender", "date_of_birth", "last_login")
    search_fields = ('username', 'nickname')
    actions = None
    exclude = ('last_login',)
    fieldsets = [
        ('基本信息', {
            'fields': (
                'username', 'password', 'gender', 'date_of_birth', 'image',
                'country', 'province', 'city', 'address', 'remark'
            )
        }),
        ('绑定信息', {
            'fields': (
                'mobile', 'email'
            )
        }),
        ('有效状态', {
            'description': '用户添加后为避免误操作，不可直接删除，但可以取消启用，则此用户进入停用状态',
            'fields': (
                'is_active',
            )
        })
    ]


admin.site.register(MemberProxy, MemberProxyAdmin)


class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "img_url"]


admin.site.register(Banner, BannerAdmin)


class PictureTypeAdmin(admin.ModelAdmin):
    list_display = ["title"]


admin.site.register(PictureType, PictureTypeAdmin)


class PictureAdmin(admin.ModelAdmin):
    list_display = ["picture_type", "title", "click"]


admin.site.register(Picture, PictureAdmin)


class PictureCommentAdmin(admin.ModelAdmin):
    list_display = ["picture", "add_time"]


admin.site.register(PictureComment, PictureCommentAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "img_url", "add_time", "click"]


admin.site.register(News, NewsAdmin)


class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ["news", "add_time"]


admin.site.register(NewsComment, NewsCommentAdmin)


class GoodsAdmin(admin.ModelAdmin):
    list_display = ["title", "click"]


admin.site.register(Goods, GoodsAdmin)


class GoodsImageAdmin(admin.ModelAdmin):
    list_display = ["goods", "img_url", "add_time"]


admin.site.register(GoodsImage, GoodsImageAdmin)


class GoodsPresentationAdmin(admin.ModelAdmin):
    list_display = ["goods", "title"]


admin.site.register(GoodsPresentation, GoodsPresentationAdmin)


class GoodsCommentAdmin(admin.ModelAdmin):
    list_display = ["goods", "add_time"]


admin.site.register(GoodsComment, GoodsCommentAdmin)


class ShopCarAdmin(admin.ModelAdmin):
    list_display = ["user", "goods", "nums", "add_time"]


admin.site.register(ShopCar, ShopCarAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "ctime"]


admin.site.register(Product, ProductAdmin)


class VideoAdmin(admin.ModelAdmin):
    list_display = ["title", "click"]


admin.site.register(Video, VideoAdmin)
