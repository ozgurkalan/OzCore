# # # # # # # # # # # # # # # # # # # # #
# imports for utils

# import check_modules
from .__import_check import check_modules

__all__ = ["check_modules"]

# helper functions
from .helper import (
    now_prefix,  # datetime today or now as prefix
    serialize_a_json_field,  # validate and join nodes of json or dict
)

__all__ += ["now_prefix", "serialize_a_json_field"]

# jupyter
if check_modules("jupyter"):
    from .jupyter import Jupyter as __Jupyter
    jupyter = __Jupyter()
    
    from .helper import dirme

    __all__ += ["jupyter", "dirme"]


# html_markdown functions
if check_modules("markdown2","html2text"):
    from .html_markdown import (
        html_to_markdown,  # clean html and return markdown
        markdown_to_html,  # convert markdown to html
    )

    __all__ += ["html_to_markdown", "markdown_to_html"]

# zipper functions
if check_modules("tqdm", "requests"):
    from .zipper import (
        unzip_url,  # download and unzip a zip file from a url
        backup,  # zip and backup files
    )

    __all__ += ["unzip_url", "backup"]
