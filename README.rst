|pypi| |license|

.. |pypi| image:: https://img.shields.io/pypi/v/lektor-chameleon.svg?style=flat-square
    :target: https://pypi.org/project/lektor-chameleon/
    :alt: PyPI version.

.. |license| image:: https://img.shields.io/pypi/l/lektor-chameleon.svg?style=flat-square
    :target: https://pypi.org/project/lektor-chameleon/
    :alt: Project license.

This plugin makes it possible to write `Lektor <https://www.getlektor.com>`_
templates using `Chameleon <https://chameleon.readthedocs.io/>`_.
It achieves this by replacing the Jinja renderer with the Chameleon renderer
during template rendering.

The names defined in the Jinja environment are available in Chameleon
templates:

.. code-block:: html

   <!-- Jinja -->
   <h1>{{ this.title }}</h1>

   <!-- Chameleon -->
   <h1>${ this.title }</h1>

   <!-- or -->
   <h1 tal:content="this.title">Page title</h1>

   <!-- Jinja -->
   {{ bag('translate', this.alt, 'message') }}

   <!-- Chameleon -->
   <span tal:replace="bag('translate', this.alt, 'message')">message</span>

Many Lektor and Jinja filters are also available using the ``>>`` operator:

.. code-block:: html

   <!-- Jinja -->
   <link rel="stylesheet" href="{{ '/static/custom.css'|url }}"/>

   <!-- Chameleon -->
   <link rel="stylesheet" href="${'/static/custom.css' >> url}"/>

Filters also accept parameters:

.. code-block:: html

   <!-- Jinja -->
   <a href="{{ '.'|url(alt=this.alt) }}">link text</a>

   <!-- Chameleon -->
   <a href="${'.' >> url(alt=this.alt)}">link text</a>

But filter parameters must be given as keyword parameters:

.. code-block:: html

   <!-- incorrect -->
   <div tal:replace="this.body >> indent(4)">Page body</div>

   <!-- correct -->
   <div tal:replace="this.body >> indent(width=4)">Page body</div>
