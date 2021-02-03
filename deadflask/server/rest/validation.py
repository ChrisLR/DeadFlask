from dataclasses import dataclass

_MISSING = object()


@dataclass(frozen=True)
class ValidatedField:
    name: str
    type: type
    optional: bool = False


def validate_post_data(fields, data):
    valid_data = {}
    invalid_data = {}
    for field in fields:
        field_data = data.get(field.name, _MISSING)
        if field_data is _MISSING and not field.optional:
            invalid_data[field.name] = f"{field.name} is missing."
            continue
        elif not isinstance(field_data, field.type):
            try:
                cast_data = field.type(field_data)
                valid_data[field.name] = cast_data
            except ValueError:
                invalid_data[field.name] = f"{field.name} is invalid type, {field.type} expected."
        else:
            if field_data is not _MISSING:
                valid_data[field.name] = field_data

    return valid_data, invalid_data
