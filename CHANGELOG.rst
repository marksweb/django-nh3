=========
Changelog
=========

unreleased
==========


0.2.0 - 2025-10-03
==================

* chore: Fix typo in utils.py by `@cclauss`_ in `PR 24`_
* pre-commit: django-upgrade --target-version 5.0 by `@cclauss`_ in `PR 25`_
* chore: Re-add Ruff to GitHub Actions by `@zerolab`_ in `PR 26`_
* ci: Explicitly run `ruff check` by `@marksweb`_ in `PR 30`_
* ci: Add django 5.1 testing by `@KozyrevIvan`_ in `PR 36`_
* ci: Switch to UV and extend test suite to new django and python by `@marksweb`_ in `PR 38`_
* fix: Empty value by `@KozyrevIvan`_ in `PR 39`_
* chore: Make test pypi releases verbose to try to catch 400 by `@marksweb`_ in `PR 40`_
* feat: Nh3CharField and Nh3TextField by `@blag`_ in `PR 52`_
* chore: Upgrade commit hooks by `@marksweb`_ in `PR 55`_
* test: Add testing against django 5.2 by `@marksweb`_ in `PR 56`_
* feat: Add `allowed_` prefix to some model and form field arguments by `@blag`_ in `PR 57`_

**New Contributors**

* `@cclauss`_ made their first contribution in `PR 25`_
* `@KozyrevIvan`_ made their first contribution in `PR 36`_
* `@blag`_ made their first contribution in `PR 52`_
* `@blag`_ made their first contribution in `PR 52`_

.. _PR 24: https://github.com/marksweb/django-nh3/pull/24
.. _PR 25: https://github.com/marksweb/django-nh3/pull/25
.. _PR 26: https://github.com/marksweb/django-nh3/pull/26
.. _PR 30: https://github.com/marksweb/django-nh3/pull/30
.. _PR 36: https://github.com/marksweb/django-nh3/pull/36
.. _PR 38: https://github.com/marksweb/django-nh3/pull/38
.. _PR 39: https://github.com/marksweb/django-nh3/pull/39
.. _PR 40: https://github.com/marksweb/django-nh3/pull/40
.. _PR 52: https://github.com/marksweb/django-nh3/pull/52
.. _PR 55: https://github.com/marksweb/django-nh3/pull/55
.. _PR 56: https://github.com/marksweb/django-nh3/pull/56
.. _PR 57: https://github.com/marksweb/django-nh3/pull/57

.. _@blag: https://github.com/blag
.. _@cclauss: https://github.com/cclauss
.. _@KozyrevIvan: https://github.com/KozyrevIvan

0.1.1 - 2023-12-21
==================

* Fix min target for black and the PyPI Changelog URL by `@zerolab`_ in `PR 18`_
* Update project metadata for PEP 621 by `@zerolab`_ in `PR 19`_
* Add coverage report to the GitHub Actions summary by `@zerolab`_ in `PR 20`_
* Drop ruff from GitHub Actions as it is covered by pre-commit.ci by `@zerolab`_ in `PR 21`_
* feat: Use super class to strip value by `@marksweb`_ in `PR 22`_

.. _@marksweb: https://github.com/marksweb
.. _@zerolab: https://github.com/zerolab
.. _PR 18: https://github.com/marksweb/django-nh3/pull/18
.. _PR 19: https://github.com/marksweb/django-nh3/pull/19
.. _PR 20: https://github.com/marksweb/django-nh3/pull/20
.. _PR 21: https://github.com/marksweb/django-nh3/pull/21
.. _PR 22: https://github.com/marksweb/django-nh3/pull/22

0.1.0 - 2023-12-19
==================

- Add templatetags to clean HTML within django templates by `@wes-otf`_ in `PR 16`_.

.. _@wes-otf: https://github.com/wes-otf
.. _PR 16: https://github.com/marksweb/django-nh3/pull/16

0.0.3 - 2023-11-15
==================

- Added pypi publishing

0.0.2 - 2023-11-15
==================

- Added model field with NH3 sanitization
- Added testing against django 5.0


0.0.1 - 2023-03-02
==================

- Initial release offering a form field with NH3 sanitization
