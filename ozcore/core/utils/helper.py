"""Helper functions

dirme::

    core.dirme(some_class)
    
now_prefix::

    core.now_prefix(separator='_', format='now')

serialize_a_jason_field::

    core.serialize_a_jason_field(some_json_content)

"""
import ast  # for safe eval of list nodes in json fields (ast.literal_eval(s))
import datetime
from typing import Union, Iterable
import re

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from typeguard import typechecked


@typechecked
def now_prefix(separator: str = "-", format: str = "now") -> str:
    """datetime today or now as prefix

    parameters:
        separator:str, default None, a seperator string for date and time
        format:str, default now, ::

                ("now")=> "%y%m%d-%H%M%S"
                ("today")=> "%y%m%d"
                ("or any valid format")=> "%y%m%d-%H%M%S"

    returns:
        str

    hint:
        useful for naming files or folders
    """
    
    if format == "now":
        format = "%y%m%d" + separator + "%H%M%S"
    elif format == "today":
        format = "%y%m%d"

    return datetime.datetime.today().strftime(format)

@typechecked
def serialize_a_json_field(val, node: Union[str, None] = None) -> Union[set, dict, list, str]:
    """Safely eval a field with a string list or dict inherited from a json file
        e.g. [{name:test}] => list object having dict node 'name'

    parameters:
        val: json | dict, field value passed
        node: str, key name in the dictionary

    returns:
        * semicolon seperated values if val is a set, dict or list
        * if node is given, returns the values in the node as semicolon separated string
        * if val is None, returns None
        * if fails to the operation returns back the val itself

    hint:
        useful in serializing fields in a dataframe having dict like objects
    """
    
    if val == np.nan:
        return val  # return NaN values back

    try:
        val = ast.literal_eval(
            str(val)
        )  # first be sure it is str then eval as dict/list object

        if node:
            if isinstance(val, dict) and (node in val.keys()):
                val = val.get(node)  # get the node values

        val = set(list(val))  # return a list
        val = sorted(val)
        return ";".join(val)  # return a string separated by ;

    except:
        return val  # if try is not successful, return back the value

@typechecked
def search_iter(iter: Iterable, s: str=None) -> list:
    """search in a list

    parameters:
        iter: iterable, an iterable (list, tuple, set) to search in
        s: str, a string to search in the list, default None

    returns:
        list, a list of matched items
    """
    s = "" if s is None else s
    
    res = list(filter(lambda v: re.search(s, v), iter))
    
    return res

@typechecked
def dirme(obj: object, s:str=None) -> list:
    """dir() of an object as list search in the list

    parameters:
        obj: object, any object
        s: str, default None, a string to filter the dir() results

    returns:
        list, dir() of the object

    hint:
        useful in getting the dir() of an object as list or searching in the dir() of an object
    """
    
    return search_iter(dir(obj), s)