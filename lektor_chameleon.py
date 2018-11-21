from functools import partial

from chameleon import PageTemplateLoader
from lektor.pluginsystem import Plugin


class Filter:
    def __init__(self, func, ctx=None):
        self.func = func if ctx is None else partial(func, ctx)

    def __call__(self, **kwargs):
        return Filter(partial(self.func, **kwargs))

    def __rrshift__(self, x):
        return self.func(x)


_CONTEXT_FILTERS = {"url", "asseturl", "markdown"}


def render_template(self, name, pad=None, this=None, values=None, alt=None):
    ctx = self.make_default_tmpl_values(pad, this, values, alt, template=name)
    ctx.update(self.jinja_env.globals)

    for f_name, f_func in self.jinja_env.filters.items():
        ctx[f_name] = Filter(f_func, ctx=ctx if f_name in _CONTEXT_FILTERS else None)

    template = self.chameleon_loader[name]
    return template(**ctx)


class ChameleonPlugin(Plugin):
    name = "chameleon"
    description = "Chameleon support for templating"

    def on_setup_env(self, **extra):
        template_paths = self.env.jinja_env.loader.searchpath
        self.env.chameleon_loader = PageTemplateLoader(template_paths)
        self.env.__class__.render_template = render_template
