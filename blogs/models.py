from django.db import models
from django.db.models import Q
from services.slugify import slugify
from services.uploader import Uploader
from services.choices import BLOG_STATUS
from ckeditor.fields import RichTextField
from services.generator import CodeGenerator
from django.contrib.auth import get_user_model
from services.mixin import DateMixin, SlugMixin
from mptt.models import MPTTModel, TreeForeignKey
from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()


class Category(DateMixin, MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, blank=True, null=True,related_name="children")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    @property
    def category_count(self):
        return Blog.objects.filter(category__in=[self.id]).count()


class Subscribe(DateMixin):
    email = models.EmailField(max_length=150)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "email"
        verbose_name_plural = "Subscribes"


class Blog(SlugMixin):
    title = models.CharField(max_length=150)
    text = RichTextField()
    view_count = models.PositiveIntegerField(default=0, editable=False)
    category = models.ManyToManyField(Category, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=BLOG_STATUS, default='Active')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.code = CodeGenerator().create_blog_shortcode(model_=self.__class__, size=8)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"


class BlogImage(DateMixin):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=Uploader.blog_image_uploader, max_length=500)

    def __str__(self):
        return self.blog.title

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'BlogImage'
        verbose_name_plural = 'BlogImages'


class ContactUs(DateMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=150)
    message = models.TextField(max_length=350)

    def __str__(self):
        return f"{self.subject} {self.created_at.strftime('%d.%m.%Y')}"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Contact Us"


class BlogReview(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    message = models.TextField(max_length=250)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Blog reviews"


class About(DateMixin):
    story = RichTextField()
    our_mission = RichTextField()

    def __str__(self):
        return "About"

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "About"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__class__.objects.exclude(id=self.id).delete()


class Contact(DateMixin):
    phone = PhoneNumberField(region="AZ")
    email = models.EmailField(max_length=150)

    def __str__(self):
        return "Contact"

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "Contact Information"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__class__.objects.exclude(id=self.id).delete()


class WishList(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)

    def __str__(self):
        return self.blog.title







