from .forms import ContactForms, BlogForm, BlogImageForm, BlogReviewForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Blog, WishList, BlogImage, Subscribe
from django.core.paginator import Paginator
from django.http import JsonResponse


def contact_us(request):
    form = ContactForms()
    if request.method == "POST":
        form = ContactForms(request.POST or None)
        if form.is_valid():
            form.save()
    context = {
        "form": form
    }
    return render(request, "contact/contact.html", context)


def about_view(request):
    return render(request, "blog/about.html", {})


def blog_view(request):
    blogs = Blog.objects.filter(status="Active").order_by("-created_at")
    
    category = request.GET.getlist("category")
    
    if category:
        blogs = blogs.filter(category__in=category)
    
    paginator = Paginator(blogs, 6)
    page = request.GET.get("page", 1)
    blog_list = paginator.get_page(page)
    context = {
        "blogs": blog_list,
        "paginator": paginator
    }
    return render(request, "blog/blog.html", context)


def blog_detail_view(request, slug):
    form = BlogReviewForm()
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        form = BlogReviewForm(request.POST or None)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.blog = blog
            new_review.user = request.user
            new_review.save()
    context = {
        "blog": blog,
        "form": form,
    }
    return render(request, "blog/single.html", context)


def get_ip_address(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        api = forwarded_for.split(",")[0]
    else:
        api = request.META.get("REMOTE_ADDR")
    return api


def wish_create_view(request):
    id_ = request.POST.get("id")
    key = get_ip_address(request)
    obj, created = WishList.objects.get_or_create(blog_id=int(id_), key=key)
    if not created:
        WishList.objects.filter(blog_id=int(id_), key=key).delete()
    return JsonResponse({"created": created})


@login_required(login_url="accounts:login")
def create_blog_view(request):
    form = BlogForm()
    image_form = BlogImageForm()
    if request.method == "POST":

        form = BlogForm(request.POST or None)
        image_form = BlogImageForm(request.POST, request.FILES)
        categories = request.POST.getlist("categories")

        if form.is_valid() and image_form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.author = request.user
            new_blog.save()  # Save the blog instance first

            # Add the categories to the many-to-many relationship
            new_blog.category.set(categories)

            # Save the blog instance again to update the many-to-many relationship
            new_blog.save()

            # Assuming BlogImageForm has a ForeignKey to Blog model
            BlogImage.objects.create(blog=new_blog, image=image_form.cleaned_data.get("image"))

            return redirect("blogs:blog-detail", slug=new_blog.slug)
    context = {
        "form": form,
        "image_form": image_form
    }
    return render(request, "blog/create.html", context)


def subscribe_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        Subscribe.objects.get_or_create(email=email)
    return redirect("blogs:blog")


