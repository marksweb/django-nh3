==========
django-nh3
==========

|actions| |pypi| |black| |pre|

Django integration with for nh3, Python binding to Ammonia HTML sanitizer Rust crate.

`nh3 docs`_

Requirements
------------

Python 3.10 to 3.13 supported.

Django 3.2 to 5.1 supported.


.. _nh3 docs: https://nh3.readthedocs.io/en/latest/?badge=latest



Contributing
------------

The project is in it's infancy, setup because of `bleach becoming deprecated`_.

It is setup with pre-commit to maintain code quality. This includes black for formatting, ruff for linting & checks.
This is much like django, so currently referring to django's own `style docs`_ will be most helpful

To contribute, fork the repo and clone your fork to your machine. Then setup a virtual environment however you prefer to do this.
Then run the following setup the basics:

.. code-block:: bash

   python -m pip install pre-commit tox-uv
   pre-commit install

Tox is used to run tests locally and on github. The test requirements are generated using pip-tools via ``requirements/compile.py``.

.. _style docs: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/#python-style
.. _bleach becoming deprecated: https://bluesock.org/~willkg/blog/dev/bleach_6_0_0_deprecation.html


.. |actions| image:: https://img.shields.io/github/actions/workflow/status/marksweb/django-nh3/main.yml?branch=main&style=for-the-badge
   :target: https://github.com/marksweb/django-nh3/actions?workflow=CI

.. |pypi| image:: https://img.shields.io/pypi/v/django-nh3.svg?style=for-the-badge
   :target: https://pypi.org/project/django-nh3/

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
   :target: https://github.com/psf/black

.. |pre| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
