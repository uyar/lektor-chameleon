# lektor-chameleon

lektor-chameleon is a plugin for the [Lektor](https://www.getlektor.com)
static site generator
that makes is possible to write the templates
using the [Chameleon](https://chameleon.readthedocs.io/) template engine.

> *Warning* The current stable release of Lektor (3.3.x) requires
> that plugins have a `setup.py` file and does not pick up plugins
> which only have a `pyproject.toml` file.
> Until this issue gets resolved in the stable release,
> Lektor needs to be installed as a prerelease:
>
> ```sh
> pip install --pre lektor
> ```

To use the plugin, add it to your project:

```sh
lektor plugin add lektor-chameleon
```

Templates must have the ``.pt`` file extension.

Usage examples:

```html
<html lang="${ this.alt }">

<h1 tal:content="this.title">Page title</h1>

<span tal:replace="bag('translate', this.alt, 'message')">message</span>
```

## Filters

Lektor filters are available as functions:

- [asseturl](https://www.getlektor.com/docs/api/templates/filters/asseturl/)
- [dateformat](https://www.getlektor.com/docs/api/templates/filters/dateformat/)
- [datetimeformat](https://www.getlektor.com/docs/api/templates/filters/datetimeformat/)
- [latformat](https://www.getlektor.com/docs/api/templates/filters/latformat/)
- [latlongformat](https://www.getlektor.com/docs/api/templates/filters/latlongformat/)
- [longformat](https://www.getlektor.com/docs/api/templates/filters/longformat/)
- [markdown](https://www.getlektor.com/docs/api/templates/filters/markdown/)
- [tojson](https://www.getlektor.com/docs/api/templates/filters/tojson/)
- [url](https://www.getlektor.com/docs/api/templates/filters/url/)

For convenience, the following Jinja filters have also been made available
as functions:

- [filesizeformat](https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.filesizeformat)
- [indent](https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.indent)
- [striptags](https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.striptags)
- [truncate](https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.truncate)
- [wordwrap](https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.wordwrap)

Usage examples:

```html
<a href="${ url('/') }">Home page</a>

<a href="${ url('/', alt=this.alt) }">link text</a>

<link rel="stylesheet" href="${ asseturl('/static/custom.css') }"/>

<div tal:content="striptags(this.body)">Shortened body text</div>

<div tal:replace="indent(this.body.html, 2)">Page body</div>

<body>
  ${ structure:wordwrap(this.body.html, width=72) }
</body>
```

## Extending templates

In order to have a base template that you want to extend for other templates,
you have to use the macro and slot mechanism in Chameleon.

For example, a base template could look like this:

```html
<html>
<head>
  <!-- ... -->
</head>
<body>
  <!-- ... -->
  <div metal:define-slot="content">
    Page content
  </div>
  <!-- ... -->
</body>
```

Assuming the base template is saved in a file called `layout.pt`,
a template that extends it would look like this:

```html
<html tal:define="layout load:layout.pt" metal:use-macro="layout">

  <div metal:fill-slot="content">
    <p tal:replace="this.body">Page body</p>
  </div>

</html>
```

## Macros

Macros are written using Chameleon's METAL expressions.
For example, the pagination macro template created by Lektor quickstart
can be implemented as:

```html
<div class="pagination" metal:define-macro="pagination">
  <span tal:condition="not current.has_prev">&laquo; Previous</span>
  <a tal:condition="current.has_prev" href="${ url(current.prev) }">&laquo; Previous</a>

  | <span tal:replace="current.page">Current page</span> |

  <span tal:condition="not current.has_next">Next &raquo;</span>
  <a tal:condition="current.has_next" href="${ url(current.next) }">Next &raquo;</a>
</div>
```

Note that the macro requires a variable called `current`
which is assumed to hold the current page in the pagination.
The template that uses the macro has to define it
when calling the macro:

```html
<html
  tal:define="
    layout load:layout.pt;
    pagination load:macros/pagination.pt;
  "
  metal:use-macro="layout">

<div tal:define="current this.pagination"
    metal:use-macro="pagination.macros.pagination">Pagination links</div>

</html>
```

Also note that the pagination macro template is loaded at the top `html` tag,
so that it can be used in the `metal:use-macro` clause.

## Templating flow blocks

Flow block templates follow the same rules as Jinja flow block templates.
The `this` parameter refers to the block and the `record` parameter
refers to the object that contains the block.
