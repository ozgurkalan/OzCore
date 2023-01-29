""" helper functions """

import pytest
import re
from ozcore import core

def test_now_prefix():
    result = core.now_prefix(separator="**", format="now")
    
    reg = re.compile(r"\d{6}\*{2}\d{6}")
    expected = re.fullmatch(reg, result)
    
    assert expected is not None

def test_dirme():
    result = core.dirme(core)
    # IPython.display.display has NoneType
    assert type(result) is type(None)