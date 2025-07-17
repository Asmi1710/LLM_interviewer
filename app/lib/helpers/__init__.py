import json, re, pytz
from dateutil.parser import parse as datetime_parser
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timezone
from app.lib.helpers.extensions import MongoEncoder

# Common Operations

"""Generate a random string of fixed length """
def random_string(stringLength=10):
    import random, string
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

def is_true(string):
    return True if str(string) in ['True', 'true', 'Yes', 'yes'] else False
        
def is_false(string):
    return True if str(string) in ['False', 'false', 'No', 'no'] else False

def parse_json(json_str): return json.loads(json_str)

def to_json(obj): return json.dumps(obj, cls=MongoEncoder)

def to_json_dict(obj): return json.loads(to_json(obj))

# Datetime arithmatic
def current_time(): return datetime.now().astimezone()

def current_time_ist(): return datetime.now().astimezone(tz=tz_ist())

def today(): return parse_datetime(str(date.today()))

def today_ist(): return parse_datetime(str(current_time_ist().date()))

def parse_datetime(obj): return obj if isinstance(obj, datetime) else datetime_parser(obj)

def datetime_ago(**delta): return current_time()-relativedelta(**delta)

def datetime_from_now(**delta): return current_time()+relativedelta(**delta)

def date_ago(**delta): return today()-relativedelta(**delta)

def date_ago_ist(**delta): return today_ist()-relativedelta(**delta)

def date_from_now(**delta): return today()+relativedelta(**delta)

# Datetime timezone change
def tz_utc(dt): return dt.astimezone(tz=timezone.utc)

def tz_ist(): return pytz.timezone('Asia/Kolkata')

def tz_local(dt): return dt.astimezone(tz=None)

def flatten(lst): return [element for item in lst for element in flatten(item)] if type(lst) is list else [lst]

def validate_date_time_format(date_str, format='%Y-%m-%d'):
    try:
        if datetime.strptime(date_str, format):
            return True
    except Exception as e:
        return False  

def number_to_words(n):
    def convert_three_digits(num):
        if num > 999: return

        ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        teens = ["", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        words = ""

        if num // 100:
            words += ones[num // 100] + " Hundred"
        num %= 100
        if num // 10 == 1:
            words += " " + teens[num % 10] if num % 10 != 0 else " Ten"
        else:
            words += " " + tens[num // 10] if num // 10 != 0 else ""
            words += " " + ones[num % 10] if num % 10 != 0 else ""

        return words.strip()

    if n == 0: return "Zero"

    numbers = [(10000000, "Crore"), (100000, "Lakh"), (1000, "Thousand"), (1, "")]
    result = ""

    for number, unit in numbers:
        current_part = n // number
        n %= number
        if current_part:
            result += convert_three_digits(current_part) + f" {unit} "

    return result.strip()

def mobile_number_without_special_chars(mobile_number, country_code = '+91'):
    import re

    if not mobile_number: return None
    mobile_number = re.sub(r'\D', '', mobile_number)[-10:]
    return mobile_number if len(mobile_number)==10 else None

def to_lower(match_obj):
    if match_obj.group() is not None:
        return match_obj.group().lower()
    return ''

def underscore(word):
    word = re.sub(r'[A-Z]', lambda x: f"_{to_lower(x)}", word)
    return re.sub("(^_*|_*$)", '', word)

def pluralize(word):
    word = underscore(word)
    if re.search('[sxz]$', word) or re.search('[^aeioudgkprt]h$', word):
        return re.sub('$', 'es', word)

    elif re.search('[aeiou]y$', word):
        return re.sub('y$', 'ies', word)

    else:
        return word + 's'
