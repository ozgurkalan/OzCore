""" helpers module """

import pytest
import re
from ozcore import core

def test_now_prefix():
    result = core.now_prefix(separator="**", format="now")
    
    reg = re.compile(r"\d{6}\*{2}\d{6}")
    expected = re.fullmatch(reg, result)
    
    assert expected is not None
    
def test_clean_html():
    result = core.clean_html("<h1>hello</h1>")
    expected = "# hello\n\n"
    
    assert result == expected
    
def test_md_2_html():
    result = core.md_2_html("# hello\n\n")
    expected = "<h1>hello</h1>\n"
    
    assert result == expected

def test_translate():
    result = core.translate(text="merhaba 😃", dest="en", src="auto", html=True)
    expected = "<p>merhaba 😃 </p>\n"
    
    assert result == expected
    
@pytest.mark.parametrize("val, node, expected",
    [
        (None, None, None),
        (list("abc"), "a_node", "a;b;c"),
        ("['a','b','c']", None, "a;b;c"),
        (set(list("cba")), "a_node", "a;b;c"),
        ('{"a_node": {"a","c","b"}}', "a_node", "a;b;c")])
def test_serializing_a_json_dict_like_value(val, node, expected):
    assert core.serialize_a_json_field(val, node) == expected

