Theming API V1 development
-----------------------------

Status
======

Accepted

Context
=======

We are implementing a new set of Theming tools that offers flexibility and high level of customization for new OpenedX
themes creation process. We are trying to cover features the current comprehensive theming does not support by
exposing a robust API that, based on a self-explained theme configuration, can preview and deploy new themes with much
less effort.

Decisions
=========

#. **API development**

   a. Render method of html_block theme element does not support html sanitizing. Right now it is rendering its content
      as it comes from the theme configuration
