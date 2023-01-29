"""HTML and Markdown functions

core.html_to_markdown(some_html_str)::

    >>> some_markdown_str_output

core.markdown_to_html(some_markdown_str)::

    >>> some_html_str_output

"""
import html2text  # clean html
from markdown2 import Markdown as md  # markdown to html or vice versa


def html_to_markdown(html:str)->str:
    """Cleans given html and returns a markdown 
    
    parameters:
        html: html markup str as input 
        
    returns:
        str, as markdown 
    """
    cleaner = html2text.html2text(html)
    return cleaner


def markdown_to_html(md_text:str)->str:
    """Converts markdown to html
    
    parameters:
        md_text: markdown str as input
        
    returns:
        str, as html markup
    """
    markdowner = md()
    html = markdowner.convert(md_text)
    return html