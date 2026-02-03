# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'boxocluster'
copyright = '2026, SIGHPC'
author = 'SIGHPC'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx_copybutton',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

myst_heading_anchors = 3
myst_enable_extensions = [
    'deflist',
    'attrs_inline',
    'linkify',
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'shibuya'

html_static_path = ['_static']
html_favicon = "_static/favicon.ico"
html_theme_options = {
    "accent_color": "pink",
    "light_logo": "_static/pngs/logo_h_maroon.png",
    "dark_logo": "_static/pngs/logo_h_white.png",
}
html_css_files = ['custom.css']
