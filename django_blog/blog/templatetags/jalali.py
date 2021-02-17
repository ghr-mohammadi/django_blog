from persiantools.jdatetime import JalaliDateTime, digits, utils
from django import template

register = template.Library()


@register.filter
def to_jalali(value, arg):
    month_map = {
        "Farvardin": "فروردین",
        "Ordibehesht": "اردیبهشت",
        "Khordad": "خرداد",
        "Tir": "تیر",
        "Mordad": "مرداد",
        "Shahrivar": "شهریور",
        "Mehr": "مهر",
        "Aban": "آبان",
        "Azar": "آذر",
        "Dey": "دی",
        "Bahman": "بهمن",
        "Esfand": "اسفند",
    }
    week_map = {
        "Shanbeh": "شنبه",
        "Yekshanbeh": "یکشنبه",
        "Doshanbeh": "دوشنبه",
        "Seshanbeh": "سه‌شنبه",
        "Chaharshanbeh": "چهارشنبه",
        "Panjshanbeh": "پنجشنبه",
        "Jomeh": "جمعه"
    }
    return utils.replace(utils.replace(JalaliDateTime(value).strftime(arg), week_map), month_map)

