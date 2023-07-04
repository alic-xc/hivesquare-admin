from math import floor

from django.template import Library
import datetime


register = Library()


@register.filter(expects_localtime=True)
def string_to_date(value):
    if not value:
        return 'N/A'

    return datetime.datetime.fromisoformat(value)


@register.filter(expects_localtime=True)
def remove_second(value):
    if not value:
        return 'N/A'
    print(value)
    date_object = datetime.datetime.fromisoformat(value)
    print(date_object)
    return 'date_object'

@register.filter(expects_localtime=True)
def string_to_date_object(value):
    try:
        return datetime.datetime.strptime(value, '%Y-%m-%d')
    except:
        if value != 'N/A':
            return value.date()
        else:
            return ''


@register.filter(expects_localtime=True)
def string_to_time(value):
    value = str(value).replace('Z', '')
    return datetime.datetime.strptime(value, 'H:%M:%S.%f')


@register.filter()
def harsh_card_no(value):
    harshed = 'XXXX XXXX XXXX '
    card_no = value[-4:]
    return harshed + card_no


@register.filter()
def truncate_ref_id(value):
    ref_id = value[10:]
    return "-" + ref_id


@register.filter()
def progress(amount=None, current_balance=None):

    if amount is None or current_balance is None:
        return 0
    else:
        amount = float(amount)
        current_balance = float(current_balance)

        if current_balance >= amount:
            return 100
        else:
            result = floor((current_balance/amount) * 100)
            return result



@register.filter()
def multiply(a, b):
    if a == 0 or b == 0 or not a or not b:
        return 0
    return float(a) * float(b)


@register.filter()
def divide(a, b):
    if a == 0 or b == 0 or not a or not b:
        return 0
    return float(a) / float(b)