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



OzCore is automating my boring stuff. A time saver gadget for me. I can access frequently used modules and methods easliy. Most of the time I am working on my Jupyter Notebooks, and OzCore is my best friend. 


Work In Progress
~~~~~~~~~~~~~~~~

This package is continuously WIP. It is for my development projects and I happily share it with open source developers. But, please bear with the versions and tests, which may effect your applications.


------------


Installation
============

I would prefer to run on an Anaconda environment. Here you will find multiple examples.

I. Anaconda
~~~~~~~~~~~

You may want to set the global Python version with Pyenv as ``pyenv global 3.8.3`` (of course if pyenv is available.)

.. code:: bash

    # create new env 
    conda create -n py383

    conda activate py383

    # this initiates every source bindings to new env
    conda install pip

    # install ozcore
    conda install ozcore



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
    pip install git+https://github.com/ozgurkalan/OzCore --force-reinstall


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

    jupyter nbextension enable --py --sys-prefix widgetsnbextension


Jupyter Extensions
==================

This step copies the ``nbextensions`` javascript and css files into the jupyter server’s search directory, and edits some jupyter config files. 

.. code:: bash

    jupyter contrib nbextension install --user




