from datetime import datetime
from django.core.exceptions import ValidationError


def year_validator(value):
    if value > datetime.now().year:
        raise ValidationError(
            ('Год не может быть больше текущего.'),
            params={'value': value},
        )
