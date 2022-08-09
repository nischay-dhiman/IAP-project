from django.core.exceptions import ValidationError


def validate_price(value):
    if value >= 50 and value <= 500:
        return value
    else:
        raise ValidationError("Price field should be between $50 and $500")
