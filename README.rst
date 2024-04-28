lektor-chameleon
================

lektor-chameleon is a plugin for the `Lektor <https://www.getlektor.com>`_
static site generator
that makes is possible to write the templates
using `Chameleon <https://chameleon.readthedocs.io/>`_.

To use the plugin, add it to your project::

  lektor plugin add lektor-chameleon

Templates must have the ``.pt`` file extension.

Usage examples:

.. code:: html

   <html lang="${this.alt}">

   <h1 tal:content="this.title">Page title</h1>

   <span tal:replace="bag('translate', this.alt, 'message')">message</span>

The following Lektor filters are available as functions:

- `asseturl <https://www.getlektor.com/docs/api/templates/filters/asseturl/>`_
- `dateformat <https://www.getlektor.com/docs/api/templates/filters/dateformat/>`_
- `datetimeformat <https://www.getlektor.com/docs/api/templates/filters/datetimeformat/>`_
- `latformat <https://www.getlektor.com/docs/api/templates/filters/latformat/>`_
- `latlongformat <https://www.getlektor.com/docs/api/templates/filters/latlongformat/>`_
- `longformat <https://www.getlektor.com/docs/api/templates/filters/longformat/>`_
- `markdown <https://www.getlektor.com/docs/api/templates/filters/markdown/>`_
- `tojson <https://www.getlektor.com/docs/api/templates/filters/tojson/>`_
- `url <https://www.getlektor.com/docs/api/templates/filters/url/>`_

The following Jinja filters are available as functions:

- `filesizeformat <https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.filesizeformat>`_
- `indent <https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.indent>`_
- `striptags <https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.striptags>`_
- `truncate <https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.truncate>`_
- `wordwrap <https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.wordwrap>`_

Usage examples:

.. code:: html

   <a href="${url('/')}">Home page</a>

   <a href="${url('/', alt=this.alt)">link text</a>

   <link rel="stylesheet" href="${asseturl('/static/custom.css')}"/>

   <div tal:content="striptags(this.body)">Shortened body text</div>

   <div tal:replace="indent(this.body.html, 2)">Page body</div>

   <body>
     ${ structure:wordwrap(this.body.html, width=72) }
   </body>
