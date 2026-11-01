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

extensions = [
	"sphinx_tabs.tabs",
	"sphinx.ext.extlinks",
	"sphinx_copybutton",
]

# -- Options for sphinx-copybutton -------------------------------------------
# https://sphinx-copybutton.readthedocs.io/
#
# Adds a "copy to clipboard" button to the top right corner of every code
# block ('code-block', 'parsed-literal' and literal blocks). The code blocks
# in this documentation contain no shell prompts, so the whole block is
# copied as it is written.

# strip a leading shell prompt if a block ever uses one: '$ ' (Linux),
# '> ' or 'PS> ' (Windows PowerShell). This is a regular expression.
copybutton_prompt_text = r"\$ |PS> |> "
copybutton_prompt_is_regexp = True

# copy the whole block, not only the lines that start with a prompt
copybutton_only_copy_prompt_lines = False

# a backslash at the end of a line continues a command, so copy such a
# command as one line
copybutton_line_continuation_character = "\\"

# default selector of the extension, repeated here as documentation: a
# single block can opt out of the button with ':class: no-copybutton'
copybutton_selector = "div:not(.no-copybutton) > div.highlight > pre"

# Zephyr version the workshop is based on. All links to the official Zephyr
# documentation point to this version. Change it only here.
zephyr_version = '4.4.2'
zephyr_docs = f'https://docs.zephyrproject.org/{zephyr_version}'

# Roles for links to the Zephyr documentation, always used with a title:
#   :zdoc:`Threads <kernel/services/threads/index>`   a documentation page
#   :zapi:`GPIO API <gpio__interface>`                a Doxygen API group
#   :zkconfig:`CONFIG_GPIO`                           a Kconfig option
#   :zpage:`All Kconfig options <kconfig.html>`       any other page
#
# For :zapi: use the Doxygen file name of the group, where every '_' of the
# group name is doubled: group 'gpio_interface' is 'group__gpio__interface.html',
# so the target is 'gpio__interface'.
#
# kconfig.html is a search page: the '#CONFIG_...' part is resolved by
# JavaScript in the browser, so a link checker does not find the anchor.
extlinks = {
	'zdoc': (zephyr_docs + '/%s.html', None),
	'zpage': (zephyr_docs + '/%s', None),
	'zapi': (zephyr_docs + '/doxygen/html/group__%s.html', None),
	'zkconfig': (zephyr_docs + '/kconfig.html#%s', '%s'),
}

templates_path = ['_templates']
# files pulled in with '.. include::', not standalone pages
exclude_patterns = ['exercises/_include']

# LinkServer version used in the docs. Change it only here. The values are
# available on every page as substitutions. Substitutions do not expand in
# 'code-block' directives, so blocks that need them use 'parsed-literal'
# (where a backslash must be written as '\\').
linkserver_version = '26.9.130'

rst_epilog = rf"""
.. |zephyr_version| replace:: {zephyr_version}
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
