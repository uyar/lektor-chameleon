lektor-chameleon
================

lektor-chameleon is a plugin for the `Lektor <https://www.getlektor.com>`_
static site generator
that makes is possible to write the templates
using the `Chameleon <https://chameleon.readthedocs.io/>`_ template engine.

To use the plugin, add it to your project::

  lektor plugin add lektor-chameleon

If you don't want to use the ".html" extension for your template files,
you can set a different one in the configuration::

  [chameleon]
  file_ext = .pt

Usage examples:

.. code:: html

   <html lang="${this.alt}">

   <h1 tal:content="this.title">Page title</h1>

   <span tal:replace="bag('translate', this.alt, 'message')">message</span>

Many Lektor and Jinja filters are available using the ``>>`` operator:

.. code:: html

   <a href="${'/' >> url}">Home page</a>

   <link rel="stylesheet" href="${'/static/custom.css' >> asseturl}"/>

Filters also accept parameters:

.. code:: html

   <a href="${'.' >> url(alt=this.alt)}">link text</a>

But filter parameters must be given as keyword parameters:

.. code:: html

   <!-- incorrect -->
   <div tal:replace="this.body >> indent(4)">Page body</div>

   <!-- correct -->
   <div tal:replace="this.body >> indent(width=4)">Page body</div>
