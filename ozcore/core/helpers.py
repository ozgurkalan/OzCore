"""  
Helper functions.

Functions can be directly called from core

usage example::

    from ozcore import core
    
    core.translate("merhaba")

"""


import datetime
import numpy as np
import pandas as pd

import ast # for safe eval of list nodes in json fields (ast.literal_eval(s))

import html2text  # clean html
from markdown2 import Markdown as md  # markdown to html or vice versa
import emoji
from google_trans_new import google_translator
from IPython.display import display




def now_prefix(separator="-", format="now"):
        """  
        datetime today or now as prefix
            
        parameters:
            separator (str): default None, a seperator string for date and time
            format (str):default Now, :: 

                    ("now")=> "%y%m%d-%H%M%S"
                    ("today")=> "%y%m%d"
                    ("or any valid format")=> "%y%m%d-%H%M%S"
            
        returns: 
            str
                
        hint:
            useful for naming files
        """
        if format == "now":
            format = "%y%m%d" + separator + "%H%M%S"
        elif format == "today":
            format= "%y%m%d"
            
        return datetime.datetime.today().strftime(format)

def clean_html(html):
    """  
    cleans given html and returns a markdown 
    
    parameters:
        html: html markup str as input 
        
    returns:
        str, as mardown 
    """
    cleaner = html2text.html2text(html)
    return cleaner


def md_2_html(md_text):
    """  
    converts markdown to html
    
    parameters:
        md_text: markdown str as input
        
    returns:
        str, as html markup
    """
    markdowner = md()
    html = markdowner.convert(md_text)
    return html

def translate(text="None", dest="en", src="auto", html=False):
    """ 
    translate text via Google Translator.
        | connects free to google translator,
        | limits text to max. 12.000 chars
    
    parameters:
        text: str, text to translate (may use html or markdown too)
        dest: str, destination lang, defaults to english (en)
        src: str, source lang, defaults to auto
        html: bool, if cleaned and set False returns Markdown, if set True returns html 
        
    returns:
        str or html

    warning: 
        | given text should not have special chars 
        | and may need to be cleaned by _clean_html
    """
    # google limits text size:
    if len(text) > 12000:
        text = text[:12000]

    # cleans the text with lean_html (google rejects some tags.)
    text = clean_html(text)

    # first demojinize with special delimiters
    text = emoji.demojize(text, use_aliases=False, delimiters=("__", "__"))

    # Translate
    translator = google_translator()
    T = translator.translate(text=text, lang_tgt=dest, lang_src=src)

    # then re-emojinize
    text_translated = emoji.emojize(T, use_aliases=False, delimiters=("__", "__"))

    if html:
        return md_2_html(text_translated)
    else:
        return text_translated
    
def serialize_a_json_field(val, node=None):
        """ 
        safely eval a field with a string list or dict inherited from a json file
            e.g. [{name:test}] => list object having dict node 'name'
        
        parameters:
            val: json | dict, field value passed
            node: str, key name in the dictionary
            
        returns:
            * semicolon seperated values if val is a set, dict or list
            * if node is given, returns the values in the node as semicolon separated string
            * if val is None, returns None
            * if fails to the opretion returns back the val itself
            
        hint:
            useful in serializing fields in a dataframe having dict like objects
        """
        if val == np.nan: return val # return NaN values back
    
        try:
            val = ast.literal_eval(str(val)) # first be sure it is str then eval as dict/list object

            if node:
                if isinstance(val, dict) and (node in val.keys()):
                    val = val.get(node) # get the node values
                
                
            val = set(list(val)) # return a list
            val = sorted(val)
            return ";".join(val) # return a string separated by ;

        except:
            return val # if try is not successful, return back the value
        
def dirme(me):
    '''
    lists methods of a given module in Jupyter Notebook
    
    parameters:
        me:str, module, argument, method
    
    returns:
        * displays module, arg or method as a pandas DataFrame
        * display option, set to the len of df (in Jupyter Notebook)
    
    '''
    s = pd.Series([e for e in dir(me) if not "__" in e]).sort_values()
    
    op = pd.get_option("max_rows")
    pd.options.display.max_rows=len(s)
    
    display(pd.DataFrame(s))
    
    pd.options.display.max_rows=op