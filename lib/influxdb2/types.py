"""Custom Types.



"""
import typing

NullStr = typing.TypeVar("NullStr", str, None)
"""String that can be None."""

TimeVal = typing.TypeVar("TimeVal", str, int, float)
