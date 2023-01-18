"""  
Helper functions.

Functions can be directly called from core
    

"""

import datetime
import numpy as np
import pandas as pd
import requests
import zipfile
from pathlib import Path, PosixPath
from IPython.display import display

from typeguard import typechecked

import typer
from tqdm.auto import tqdm

import ast # for safe eval of list nodes in json fields (ast.literal_eval(s))

import html2text  # clean html
from markdown2 import Markdown as md  # markdown to html or vice versa
import emoji


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
    
@typechecked
def unzip(url:str, dest:PosixPath, chunk_size:int=1024*1024, remove_zip: bool=False):
    """ 
    Downloads and unzips a zip file
    
    parameters:
        url: str, uri to zip file
        dest: PosixPath, destination folder
        chunk_size: int, default 1 MB
        remove_zip: bool, default False, unlinks zip file after unzip operation
        
    returns:
        tqdm progress bar and typer echo messages
    """
    stream = requests.get(url, stream=True, verify=False, allow_redirects=True)
    filename = stream.url.split(sep="/")[-1]
    length = int(stream.headers.get("content-length", -1))
    
    if length < 1:
        raise Exception(f"content length is less than 1 bytes")
    
    if not dest.exists():
        raise Exception(f"destination folder does not exist: {dest}")
    
    if dest.is_file():
        dest = dest.parent
        
    dest = dest.resolve()

    typer.echo("Downloading zip file...")

    with tqdm.wrapattr(
    open(dest.joinpath(filename), "wb"), "write",
    unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
    desc=filename, total=length) as f:
        for chunk in stream.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                f.flush()
                
    typer.echo("Extracting zip file...")
    
    with zipfile.ZipFile(dest.joinpath(filename)) as zippo:
        for member in tqdm(zippo.infolist(), desc="Extracting zip file..."):
            zippo.extract(member, dest)
            
    if remove_zip:
        dest.joinpath(filename).unlink()
        typer.secho(f"{filename} is removed.", bold=True, fg="red")
    else:
        typer.secho(f"{filename} is unzipped in {dest}.", bold=True, fg="green")
    