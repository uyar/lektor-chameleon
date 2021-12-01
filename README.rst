|pypi| |license|

.. |pypi| image:: https://img.shields.io/pypi/v/lektor-chameleon.svg?style=flat-square
    :target: https://pypi.org/project/lektor-chameleon/
    :alt: PyPI version.

.. |license| image:: https://img.shields.io/pypi/l/lektor-chameleon.svg?style=flat-square
    :target: https://github.com/uyar/lektor-chameleon/blob/master/LICENSE.txt
    :alt: Project license.

lektor-chameleon is a plugin for the `Lektor <https://www.getlektor.com>`_
static site generator that makes is possible to write the templates using
the `Chameleon <https://chameleon.readthedocs.io/>`_ template engine.

To use the plugin, add it to your project::

  lektor plugin add lektor-chameleon

Since the plugin modifies the default environment, it requires
that it will be explicitly enabled.
To enable the plugin, create the file ``configs/chameleon.ini``
and put the following lines into it::

  [chameleon]
  enabled = yes

If you don't want to use the ".html" extension for your template files,
you can set a different one in the configuration::

  [chameleon]
  enabled = yes
  file_ext = .pt

Usage examples:

.. code-block:: html

   <html lang="${this.alt}">

   <h1 tal:content="this.title">Page title</h1>

   <span tal:replace="bag('translate', this.alt, 'message')">message</span>

Many Lektor and Jinja filters are available using the ``>>`` operator:

.. code-block:: html

   <a href="${'/' >> url}">Home page</a>

   <link rel="stylesheet" href="${'/static/custom.css' >> asseturl}"/>

Filters also accept parameters:

.. code-block:: html

   <a href="${'.' >> url(alt=this.alt)}">link text</a>

But filter parameters must be given as keyword parameters:

.. code-block:: html

   <!-- incorrect -->
   <div tal:replace="this.body >> indent(4)">Page body</div>

   <!-- correct -->
   <div tal:replace="this.body >> indent(width=4)">Page body</div>
