from __future__ import annotations
from typing import TypeVar, Dict, Set
from pydantic.types import StrictFloat, StrictInt, StrictStr
from nacolla.operations import merge
from nacolla.step import Step
import pytest
from tests.mock_models import *


def _int_to_str(input: WrappedInt) -> WrappedString:
    return WrappedString(a_string=str(input.a_int))


def _annotated_identity_str(input: WrappedString) -> WrappedString:
    return input


def _annotated_identity_dict(input: WrappedDict) -> WrappedDict:
    return input


def _float_to_dict(input: WrappedFloat) -> WrappedDict:
    return WrappedDict(a_dict={"a_value": input.a_float})


_s1: Step[WrappedInt, WrappedString] = Step(
    apply=_int_to_str, next=_annotated_identity_str, name="int_to_str"
)

_s2: Step[WrappedFloat, WrappedDict] = Step(
    apply=_float_to_dict, next=_annotated_identity_dict, name="float_to_dict"
)


def test_merge_incompatible_interfaces():

    with pytest.raises(TypeError):
        merge(_s1, _s1)


def test_merge_singledispatch_default_implementation():

    merged = merge(_s1, _s2)

    with pytest.raises(NotImplementedError):
        merged.apply(WrappedSet(a_set={1, 2, 3}))  # type: ignore

    with pytest.raises(NotImplementedError):
        merged.next(WrappedSet(a_set={1, 2, 3}))  # type: ignore