======
OzCore
======

OzCore is my core.


.. image:: https://badge.fury.io/py/ozcore.svg
    :target: https://pypi.python.org/pypi/ozcore/
    :alt: PyPI version


.. image:: https://readthedocs.org/projects/ozcore/badge/?version=latest
    :target: https://ozcore.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


.. image:: http://hits.dwyl.com/ozgurkalan/OzCore.svg
    :target: http://hits.dwyl.com/ozgurkalan/OzCore
    :alt: HitCount


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black



OzCore is automating my boring stuff. A time saver gadget for me. 


Installation
============



I. Pip simple
~~~~~~~~~~~~~
Published latest stable version

.. code:: bash

    pip install ozcore



II. Latest from GitHub with Pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Latest dev version from GitHub

.. code:: bash

    pip install git+https://github.com/ozgurkalan/OzCore --force-reinstall --no-deps


III. GitHub clone
~~~~~~~~~~~~~~~~~

.. code:: bash

    git clone https://github.com/ozgurkalan/OzCore.git



Jupyter Kernel
==============

For your Jupyter Notebook to run in your dedicated environment, use the following script::

    # add kernell to Jupyter
    python -m ipykernel install --user --name=<your_env_name>


Fresh installs may have problems with enabling extentions. You shall run the commands below to activate.

.. code:: bash

    jupyter nbextension enable --py --sys-prefix widgetsnbextension


Jupyter Extensions
==================

This step copies the ``nbextensions`` javascript and css files into the jupyter server’s search directory, and edits some jupyter config files. 

.. code:: bash

    jupyter contrib nbextension install --system





