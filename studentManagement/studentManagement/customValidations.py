from django.core.exceptions import ValidationError
import re


class CustomValidations:

    @staticmethod
    def integer_value_length(value_to_check: int, length: int):
        if len(str(value_to_check)) != length:
            raise ValidationError(f'length is not {length}')

    @staticmethod
    def integer_starts_from(value_to_check: int, start_from: int):

        value_initial = int(str(value_to_check)[:1])
        if value_initial < start_from:
            raise ValidationError(f'Not allowed to start from {value_initial}. Should be start from {start_from}')

    @staticmethod
    def check_string_pattern(string_to_check: str, pattern: str):
        regex = re.compile(pattern)
        if not regex.match(string_to_check):
            raise ValidationError(f"These things not allowed {pattern}")



