import os
import sys

sys.path.insert(0, os.path.abspath("../../"))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ConvexTrader"
copyright = "2024, Dhyey Mavani, Liam Davis, Ryan Ji, Allison Klinger, Andrew Palena"
author = "Dhyey Mavani, Liam Davis, Ryan Ji, Allison Klinger, Andrew Palena"
release = "0.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.viewcode"]


templates_path = ["_templates"]
html_static_path = []
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "furo"
