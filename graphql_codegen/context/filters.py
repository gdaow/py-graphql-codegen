"""Common filters usables in Mako templates."""


def camel(text: str) -> str:
    """Return the given string in camel case."""
    if len(text) == 0:
        return text

    result = text[0].upper()
    next_upper = False
    for char in text[1:]:
        if char == '_':
            next_upper = True
        else:
            if next_upper:
                char = char.upper()
                next_upper = False
            result = result + char

    return result


def indent(text: str) -> str:
    """Return the given string in camel case."""
    return text.replace('\n', '\n     ')
