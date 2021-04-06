# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('..'))




# -- Project information -----------------------------------------------------

project = 'OzCore'
copyright = '2021, OZinClouds'
author = 'Ozgur Kalan'

# The full version, including alpha/beta/rc tags
release = '1.2'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
'sphinx.ext.autodoc', 
'sphinx.ext.doctest',
'sphinx.ext.intersphinx', 
'sphinx.ext.todo',
'sphinx.ext.ifconfig', 
'sphinx.ext.viewcode',
'sphinx.ext.inheritance_diagram',
'sphinx.ext.autosummary',
"sphinx.ext.autosectionlabel",
'sphinxcontrib.napoleon',
"myst_parser",
]



# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']

html_css_files = ["css/custom.css"]
html_js_files = ['js/custom.js']

html_theme_options = {
    'logo_only': True,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    # 'style_nav_header_background': 'white',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}
html_show_sourcelink = False

html_sidebars = {
   # '**': ['genindex.html'],
}


# -- Options for Napoleon settings -------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_attr_annotations = True
napoleon_type_aliases = None

# -- Options for TODO-------------------------------------------------
todo_include_todos = True

# -- Options for autodoc -------------------------------------------------
autodoc_default_options = {
    'member-order': 'bysource',
    'special-members': '__init__',
}






# -- END -------------------------------------------------