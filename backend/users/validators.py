from django.core.validators import RegexValidator

username_validator = RegexValidator(
    regex=r'^[\w.-]+\Z',
    message=(
        'Enter a valid username. This value may contain only English letters, '
        'numbers, and ./_ characters.'
    )
)
