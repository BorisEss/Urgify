from django.utils.crypto import get_random_string


def upload_img(instance, filename):
    random_string = get_random_string(6)
    ext = filename.split('.')[-1]
    class_name = instance.__class__.__name__
    return f'{class_name}/{instance.slug}/{random_string}.{ext}'
