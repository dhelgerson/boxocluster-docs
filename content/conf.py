# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Boxocluster'
copyright = '2026, SIGHPC'
author = 'SigHPC'

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
html_favicon = "_static/favicon.png"
html_theme_options = {
	"github_url": "https://github.com/userjack6880/picluster/tree/boxocluster",
	"discord_url": "https://discord.gg/H4AEpeg8KU",
    "accent_color": "pink",
    "light_logo": "_static/pngs/logo_h_maroon.png",
    "dark_logo": "_static/pngs/logo_h_white.png",
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
