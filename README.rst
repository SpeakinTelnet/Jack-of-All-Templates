======================
Jack-of-All-Templates
======================

| |mit-shield| |python-shield| |ruff-shield| |black-shield| |isort-shield|

.. |mit-shield| image:: https://badgen.net/static/license/MIT/blue
    :target: https://codeberg.org/SpeakinTelnet/Jack-of-All-Templates/src/branch/main/LICENSE
    :alt: MIT
.. |python-shield| image:: https://badgen.net/badge/Made%20with/%20Python/blue
   :target: https://www.python.org/

.. |ruff-shield| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff

.. |black-shield| image:: https://badgen.net/badge/Code%20Style/%20Black/black
    :target: https://github.com/psf/black

.. |isort-shield| image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/


A simple and opinionated template aggregator for multiple languages.


Why
---

As someone who takes more time thinking about new projects and how to structure them than
actually coding, the opportunity to create a multi language template while testing both
`Copier <https://github.com/copier-org/copier>`_ and
`Hatch <https://github.com/pypa/hatch>`_ was hard to pass.


Usage
-----

Prerequisite
************

You will need ``Copier`` to use this template, it is recommended to install it using `pipx <https://pypa.github.io/pipx/installation/>`_.

.. code-block::
    
    pipx install copier

Basic Usage
***********

Start by generating a blank project

.. code-block::

    copier copy https://codeberg.org/SpeakinTelnet/Jack-of-All-Templates.git /path/to/project

or 

.. code-block::

    copier copy gh:SpeakinTelnet/Jack-of-All-Templates /path/to/project


then you can change directory to your ``/path/to/project`` and initiate your project as
you'd normally do

.. code-block:: console
    
    cd /path/to/project
    git init
    git add .
    git commit -m "Initial commit"


Testing
-------

since this project is built around Hatch you will first need it

.. code-block::

    pipx install hatch


Then you can run tests using:

.. code-block::

    hatch run test:test
    hatch run lint:style

And for a quick lint using ``ruff``:

.. code-block::

    hatch run lint:fmt

License
-------

This project is licensed under the `MIT License <{{ repo_url }}/src/branch/main/LICENSE>`_


⊂(▀¯▀⊂)  `Donate <https://codeberg.org/SpeakinTelnet/.profile/src/branch/main/DONATE.rst>`_
