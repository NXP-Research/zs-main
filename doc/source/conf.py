# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'NXP Zephyr Workshop'
copyright = '2026, NXP'
author = 'NXP'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_tabs.tabs"]

templates_path = ['_templates']
# files pulled in with '.. include::', not standalone pages
exclude_patterns = ['exercises/_include']

# LinkServer version used in the docs. Change it only here. The values are
# available on every page as substitutions. Substitutions do not expand in
# 'code-block' directives, so blocks that need them use 'parsed-literal'
# (where a backslash must be written as '\\').
linkserver_version = '26.9.130'

rst_epilog = rf"""
.. |linkserver_version| replace:: {linkserver_version}
.. |linkserver_deb| replace:: LinkServer_{linkserver_version}.x86_64.deb.bin
.. |linkserver_deb_bold| replace:: **LinkServer_{linkserver_version}.x86_64.deb.bin**
.. |linkserver_exe_bold| replace:: **LinkServer_{linkserver_version}.exe**
.. |linkserver_path_cmd| replace:: $env:Path += ";C:\\NXP\\LinkServer_{linkserver_version}"
"""


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

# removes the "Built with Sphinx..." bit from the bottom of the page
html_show_sphinx = False

html_static_path = ['_static']
html_css_files = [
	'css/main.css'
]
