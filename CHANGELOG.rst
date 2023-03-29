v2.0.4
~~~~~~

* refactored dependencies

v2.0.3
~~~~~~

* refactored init files for modules sqlite, csv
* added pydantic to requirements optional
* poetry export requirements.txt has -E all tag
* removed pngTable function


v2.0.2
~~~~~~

* check_modules function added
* utils __init__ refactored with check_modules
* arcname added to zipped files in utils
* pyproject optionals added: [all] for extras
* all typeguard previous `check_argument_types` functions replaced with @typechecked wrapper


v2.0.1
~~~~~~

* too many fixes
* revamped modules


v1.1.15
~~~~~~~

* removed office module from OzCore

v1.1.14
~~~~~~~

* fixed Sphinx

v1.1.13
~~~~~~~

* moved all dependencies to the group Dev
* Poetry version updated
* fixed alembic migration module import issue
* fixed qgrid ipywidgets issue by downgrading ipywidgets
* removed google translate module and translate helper function


v1.1.12
~~~~~~~

* fixed ipyaggrid view
* added group by column for AG Grid

v1.1.11
~~~~~~~

* Include unzip helper function
* Add dependencies: pytest_httpserver, typer, tqdm
* config and Makefile for pre-publish actions of the package
* ozcore.__version__ is available

v1.1.10
~~~~~~~
Include seaborn in dependencies which pulled scipy as dependecy. Corrected installation on a conda environment in README.


v1.1.9
~~~~~~
Include jupyter_contrib_nbextensions in dependencies. Update some of the docstrings. Include handcrafted requirements.txt in docs folder to meet ReadTheDocs build requirements.

v1.1.8
~~~~~~
Reduce number of modules. Fit to ReadTheDocs requirements and include a requirements.txt derived from poetry.

v1.1.7
~~~~~~
Rearrange and fix docs

v1.1.6
~~~~~~
A stable version after experimenting PyPi automation with Github actions.

v1.0.1
~~~~~~
Initial commit
