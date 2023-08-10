""" helper functions """

import pytest
import re
from ozcore import core

def test_now_prefix():
    result = core.utils.now_prefix(separator="**", format="now")
    
    reg = re.compile(r"\d{6}\*{2}\d{6}")
    expected = re.fullmatch(reg, result)
    
    assert expected is not None



@pytest.mark.parametrize("val, node, expected",
    [
        (list("abc"), "a_node", "a;b;c"),
        ("['a','b','c']", None, "a;b;c"),
        (set(list("cba")), "a_node", "a;b;c"),
        ('{"a_node": {"a","c","b"}}', "a_node", "a;b;c")])
def test_serializing_a_json_dict_like_value(val, node, expected):
    assert core.utils.serialize_a_json_field(val, node) == expected
    
    
def test_search_iter():
    # GIVEN an iterable
    # WHEN search_iter is called
    # THEN it should return a list of matched items
    iterable = list("abc")
    
    assert core.search_iter(iterable, "a") == ["a"]
    assert core.search_iter(iterable, "b") == ["b"]
    assert core.search_iter(iterable, "c") == ["c"]
    assert core.search_iter(iterable, "d") == []
    assert core.search_iter(iterable, None) == ["a", "b", "c"]
    
def test_dirme():
    # GIVEN a class
    # WHEN dirme is called
    # THEN it should return a list of attributes of the class
    obj = list("abc")
    
    assert core.dirme(obj) == dir(obj)
    assert core.dirme(obj, "pop") == ["pop"]