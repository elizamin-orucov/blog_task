from .models import Category, About, Contact
from services.weather import get_weather


def category_extra_context(request):
    category = Category.objects.order_by("-created_at")
    about = About.objects.first()
    contact = Contact.objects.first()

    city = "Baku"
    api_key = "913a9d018060805a15ab47e2bce323f0"

    weather_data = get_weather(api_key, city)

    return {
        "category": category,
        "about": about,
        "contact": contact,
        "weather_data": weather_data,
    }
