# Sphinx configuration for {{ cookiecutter.project_name }}
# Only present when documentation_tool is 'sphinx'

project = "{{ cookiecutter.project_name }}"
copyright = "2025, {{ cookiecutter.author_name }}"
author = "{{ cookiecutter.author_name }}"
release = "{{ cookiecutter.version }}"
version = "{{ cookiecutter.version }}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []
html_theme = "alabaster"
html_static_path = ["_static"]
html_title = "{{ cookiecutter.project_name }}"
