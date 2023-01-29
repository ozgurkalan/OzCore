# # # # # # # # # # # # # # # # # # # # #
# imports for utils


# jupyter
from .jupyter import Jupyter
jupyter = Jupyter()

# helper functions
from .helper import (
                    dirme, # lists methods of a given module 
                    now_prefix, # datetime today or now as prefix
                    
                    )

# html_markdown functions
from .html_markdown import(
                          html_to_markdown, # clean html and return markdown
                          markdown_to_html, # convert markdown to html
                        )

__all__=["jupyter", "dirme", "now_prefix", "html_to_markdown", "markdown_to_html", ]