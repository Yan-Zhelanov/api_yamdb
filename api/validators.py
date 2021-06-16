from datetime import datetime
from django.core.exceptions import ValidationError

def custom_year_validator(value):
    if value > datetime.now().year:
        raise ValidationError(
            ('Год не может быт больше текущего года.'),
            params={'value': value},
        )
