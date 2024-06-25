from django.template.defaultfilters import slugify

class Uploader:

    @staticmethod
    def blog_image_uploader(instance, filename):
        return f"blogs/{slugify(instance.blog.title)}/{filename}"



