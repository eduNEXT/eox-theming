Change Log
==========

..
   All enhancements and patches to eox-theming will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (http://semver.org/).
.. There should always be an "Unreleased" section for changes pending release.
Unreleased
----------

[1.0.0] - 2020-11-05
--------------------

Added
~~~~~

* Support for the juniper release.
* A new backend for the storages.

Changed
~~~~~~~

* Middleware is now installed introspecting settings.MIDDLEWARE

Removed
~~~~~~~

* Settings module aws.py. It was used only for compatibility with hawthorn releases.
