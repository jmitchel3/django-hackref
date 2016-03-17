import random
import string

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch


try:
    code_count = settings.HACKREF_CHARACTER_COUNT
except:
    code_count = 8


def unique_string_generator(size=code_count, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))



def model_code_generator(ModelClass):
    code = unique_string_generator()
    while ModelClass.objects.filter(code=code).exists():
        code = unique_string_generator()
    return code




def get_redirect_path(setting_var, value):
    try:
        path = reverse(value)
    except NoReverseMatch:
        raise NoReverseMatch("{setting_var}: Improperly configured in \
Django Settings.\n`{value}` is not a valid URL name.\
\n\nTo fix url pattern name, read about `reverse` here: \
\nhttps://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse".format(
                    setting_var=setting_var, value=value)
            )
    return path


def clean_message(setting_var, value):
    if type(message) != str:
        raise ImproperlyConfigured("{setting_var} must be a string.\
            \n`{value}` is not.")
    return value

