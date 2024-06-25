import pathlib
from django import forms
from .models import ContactUs, Blog, BlogImage, BlogReview


class ContactForms(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields:
            self.fields[filed].widget.attrs.update({"class": "form-control", "placeholder": filed.title})
        self.fields["first_name"].widget.attrs.update({"placeholder": "First name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Last name"})


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = (
            "title",
            "text"
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update({"cols": 70})
        for filed in self.fields:
            self.fields[filed].widget.attrs.update({"class": "form-control", "placeholder": filed.title})


class BlogImageForm(forms.ModelForm):

    class Meta:
        model = BlogImage
        fields = (
            "image",
            )

    def clean(self):
        image = self.cleaned_data.get("image")

        if image is not None and image is not False:
            image_path = pathlib.Path(str(image)).suffix
            if image_path not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError("Sadəcə jpg, jpeg və png formatında şəkil yüklənə bilər")
        return self.cleaned_data


class BlogReviewForm(forms.ModelForm):

    class Meta:
        model = BlogReview
        fields = (
            "message",
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].widget.attrs.update({"class": "form-control", "cols": 30, "rows": 10, "placeholder": "Leave a comment"})

