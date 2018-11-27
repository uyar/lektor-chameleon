from functools import partial

from chameleon import PageTemplateLoader
from lektor.pluginsystem import Plugin
from markupsafe import Markup


_CONTEXT_FILTERS = {"url", "asseturl", "markdown"}
_STR_FILTERS = {
    "capitalize",
    "center",
    "indent",
    "length",
    "lower",
    "replace",
    "title",
    "trim",
    "truncate",
    "upper",
    "wordcount",
    "wordwrap",
}
_JINJA_ENV_FILTERS = {"attr", "replace", "truncate", "wordwrap"}


class Filter:
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.ctx = self.name in _CONTEXT_FILTERS
        self.str = self.name in _STR_FILTERS

    def __call__(self, *args, **kwargs):
        return Filter(self.name, partial(self.func, *args, **kwargs))

    def __rrshift__(self, x):
        markup = self.str and hasattr(x, "html")
        p = x.html if markup else x
        t = self.func(p)
        y = t.unescape() if hasattr(t, "unescape") else t
        return Markup(y) if markup else y


def render_template(self, name, pad=None, this=None, values=None, alt=None):
    ctx = self.make_default_tmpl_values(pad, this, values, alt, template=name)
    ctx.update(self.jinja_env.globals)

    for f_name, f_filter in self.chameleon_filters.items():
        ctx[f_name] = f_filter(ctx) if f_filter.ctx else f_filter

    template = self.chameleon_loader[name]
    return template(**ctx)


class ChameleonPlugin(Plugin):
    name = "chameleon"
    description = "Chameleon support for templating"

    def on_setup_env(self, **extra):
        template_paths = self.env.jinja_env.loader.searchpath
        self.env.chameleon_loader = PageTemplateLoader(template_paths)

        filters = {n: Filter(n, f) for n, f in self.env.jinja_env.filters.items()}
        for f_name in _JINJA_ENV_FILTERS:
            filters[f_name] = filters[f_name](self.env.jinja_env)
        self.env.chameleon_filters = filters

        self.env.__class__.render_template = render_template
