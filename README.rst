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






It is automating my boring stuff. A time saver for me. I can access frequently used modules and methods easliy. Most of my time is passing with Jupyter Notebooks, and OzCore is my best friend. 

Many code snippets derive from a hard processes. I search for the best fitting options and try them sometimes for hours or days. OzCore keeps my good practices as side notes. My quality time for coding is mostly passing with annoying dev-environment, re-setups and glitches. OzCore skips the hard process and provides me with a fresh working environment, where All necessary packages installed.

Goals
=====

* a Jupyter Notebook having the most used modules.
* shorthand to 
    * path operations
    * tmp folder actions
    * Sqlite operations
    * CSV operations
    * Dataframe operations
    * Dummy records
    * Jupyter initial setups
    * Jupyter Notebook grid plugins
    * and some MS Office automations


Warnings
========

Work In Progress
~~~~~~~~~~~~~~~~

This package is continuously WIP. It is for my development projects and I happily share it with open source developers. But, please bear with the versions and tests, which may effect your applications.


Massive Dependencies
~~~~~~~~~~~~~~~~~~~~

Since OzCore is a collection of snippets using diverse packages, massive amount of dependencies will be downloaded.

.. warning::

    Please see dependencies in ``pyproject.toml`` before installing.

MacOS bound modules
~~~~~~~~~~~~~~~~~~~

Some of the helper modules and functions are directly referenced to MacOS environment. Espacially Windows users may not like it. And some references are pointing to options which may not be available in your system. Such as OneDrive folder or gDrive folder. I have tests to distinguish between users, nevertheless you should be aware of this.

------------


Installation
============

I would prefer to run on an Anaconda environment. Here you will find multiple examples.

.. warning::

    Python environment management has become a disaster. Please be sure where you are with ``which python`` . 


I. Anaconda
~~~~~~~~~~~

.. code:: bash

    # new env needs ipython, you may also clone an existing env
    conda create -n py383 python=3.8.3 ipython  

    conda activate py383

    pip install ozcore



II. Virtualenv
~~~~~~~~~~~~~~

.. code:: bash

    # create a virtualenv
    python -m venv .venv

    source .venv/bin/activate

    pip install ozcore


III. Pip simple
~~~~~~~~~~~~~~~

.. code:: bash

    # in any environment having pip
    pip install ozcore


IV. Poetry with Pyenv
~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    # in any package folder (3.8.4 version of python is arbitrary)
    pyenv local 3.8.4

    poetry shell

    poetry add ozcore


V. GitHub with Pip
~~~~~~~~~~~~~~~~~~

.. code:: bash

    # in any environment having pip
    pip install https://github.com/ozgurkalan/OzCore.git


VI. GitHub clone
~~~~~~~~~~~~~~~~

.. code:: bash

    # in some folder, e.g. Desktop
    git clone https://github.com/ozgurkalan/OzCore.git



Jupyter Kernel
==============

Jupyter has its own configuration. Espacially when you have Anaconda installed,  ``kernel.json`` may have what conda sets. 

For your Jupyter Notebook to run in your dedicated environment, please use the following script::

    # add kernell to Jupyter
    python -m ipykernel install --user --name=<your_env_name>

    # remove the kernel from Jupyter
    jupyter kernelspec uninstall <your_env_name>


Fresh installs may have problems with enabling extentions. You shall run the commands below to activate.

.. code:: bash

    jupyter nbextension enable --py --sys-prefix qgrid
    jupyter nbextension enable --py --sys-prefix widgetsnbextension


Jupyter Extensions
==================

This step copies the ``nbextensions`` javascript and css files into the jupyter server’s search directory, and edits some jupyter config files. 

.. code:: bash

    jupyter contrib nbextension install --user




