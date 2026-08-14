# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Boxocluster'
copyright = '2026, SIGHPC'
author = 'SigHPC'

html_title = project

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinx_new_tab_link',
    'sphinx_iconify',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

myst_heading_anchors = 3
myst_enable_extensions = [
    'deflist',
    'attrs_inline',
    'linkify',
    'dollarmath',
]

myst_dmath_double_inline = True

# Register sphinx_design directives with MyST Parser
# This allows MyST to parse {tab-set}, {tab-item}, etc. syntax
myst_url_schemes = ('http', 'https', 'mailto', 'ftp')


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'shibuya'
html_theme_options = {
    "default_mode": "light",  # Force light mode on first load
}
html_static_path = ['_static']
html_favicon = "_static/favicon-msu.svg"
html_logo = "_static/logos/HORIZONTAL_WEB_white.svg"
html_theme_options = {
	"github_url": "https://github.com/userjack6880/picluster/tree/boxocluster",
	"discord_url": "https://discord.gg/H4AEpeg8KU",
    "accent_color": "gray",
}
html_css_files = ['custom.css']

# Set this to your published HTML site root.
html_baseurl = "https://boxocluster.com/"  # trailing slash is fine

def add_online_link_banner(app, docname, source):
    """
    Prepend a short banner to each document with a deep link to the published HTML page.
    This affects all builders, including the 'text' builder.
    """
    base = (app.config.html_baseurl or "").rstrip("/") + "/"
    url = f"{base}{docname}.html"

    if app.builder.name == "text":
        banner = (
            "\n\n"
            "Note:\n\n"
            f"    Online version of this page: {url}\n\n"
        )
        source[0] = banner + source[0]

    return

def setup(app):
    app.connect("source-read", add_online_link_banner)
