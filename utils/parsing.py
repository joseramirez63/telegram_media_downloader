"""Safe value parsing utilities."""

from typing import Optional


def safe_int(value, default=0, *, min_value: int | None = None):
    """Parse *value* to an ``int``, returning *default* on failure.

    Parameters
    ----------
    value: any
        Value to convert (``int``, ``str``, ``None``, etc.).
    default: int
        Value returned when conversion fails or violates constraints.
    min_value: int or None
        If set, the result must be ``>= min_value``; otherwise *default*
        is returned.

    Returns
    -------
    int
        Parsed integer or *default*.
    """
    try:
        result = int(value)
    except (TypeError, ValueError):
        return default
    if min_value is not None and result < min_value:
        return default
    return result
