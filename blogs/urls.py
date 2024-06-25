from django.urls import path
from . import views

app_name = "blogs"

urlpatterns = [
    path("contact/", views.contact_us, name="contact-us"),
    path("", views.blog_view, name="blog"),
    path("detail/<slug>/", views.blog_detail_view, name="blog-detail"),
    path("about/", views.about_view, name="about"),
    path("wish/create/", views.wish_create_view, name="wish-create"),
    path("create/", views.create_blog_view, name="blog-create"),
    path("subscribe/", views.subscribe_view, name="subscribe"),
]


