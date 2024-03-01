import re

_boundaries_finder = re.compile("(.)([A-Z][a-z]+)")
_boundaries_finder_2 = re.compile("([a-z0-9])([A-Z])")


def camel_to_snake(txt):
    s1 = _boundaries_finder.sub(r"\1_\2", txt)
    return _boundaries_finder_2.sub(r"\1_\2", s1).lower()
