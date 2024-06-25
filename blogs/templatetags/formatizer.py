from django import template
import phonenumbers

register = template.Library()


@register.filter
def change_mobile_format(val):
    return phonenumbers.format_number(val, phonenumbers.PhoneNumberFormat.INTERNATIONAL)