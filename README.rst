This plugin makes it possible to write `Lektor <https://www.getlektor.com>`_
templates using `Chameleon <https://chameleon.readthedocs.io/>`_.

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
