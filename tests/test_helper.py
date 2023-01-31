""" helper functions """

import pytest
import re
from ozcore import core

def test_now_prefix():
    result = core.utils.now_prefix(separator="**", format="now")
    
    reg = re.compile(r"\d{6}\*{2}\d{6}")
    expected = re.fullmatch(reg, result)
    
    assert expected is not None

def test_dirme():
    result = core.utils.dirme(core)
    # IPython.display.display has NoneType
    assert type(result) is type(None)


@pytest.mark.parametrize("val, node, expected",
    [
        (None, None, None),
        (list("abc"), "a_node", "a;b;c"),
        ("['a','b','c']", None, "a;b;c"),
        (set(list("cba")), "a_node", "a;b;c"),
        ('{"a_node": {"a","c","b"}}', "a_node", "a;b;c")])
def test_serializing_a_json_dict_like_value(val, node, expected):
    assert core.utils.serialize_a_json_field(val, node) == expected