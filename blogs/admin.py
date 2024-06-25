from django.contrib import admin
from .models import (
    ContactUs, About, Blog, BlogImage, Category, Contact, WishList, Subscribe
)


class ImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1


class BlogAdmin(admin.ModelAdmin):
    list_display_links = ("title",)
    list_display = ("title", "status")
    list_filter = ("title", "status")
    list_editable = ("status",)
    inlines = (ImageInline,)


admin.site.register(Blog, BlogAdmin)
admin.site.register(ContactUs)
admin.site.register(Subscribe)
admin.site.register(Category)
admin.site.register(WishList)
admin.site.register(Contact)
admin.site.register(About)
