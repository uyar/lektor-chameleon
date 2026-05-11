# lektor-chameleon

lektor-chameleon is a plugin for the [Lektor](https://www.getlektor.com)
static site generator
that makes is possible to write the templates
using the [Chameleon](https://chameleon.readthedocs.io/) template engine.

To use the plugin, add it to your project:

```sh
$ lektor plugin add lektor-chameleon
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
