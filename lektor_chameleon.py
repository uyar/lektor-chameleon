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


def render_template(self, name, pad=None, this=None, values=None, alt=None):
    ctx = self.make_default_tmpl_values(pad, this, values, alt, template=name)
    ctx.update(self.jinja_env.globals)

    ctx["asseturl"] = Filter(self.jinja_env.filters["asseturl"], ctx)
    ctx["url"] = Filter(self.jinja_env.filters["url"], ctx)

    template = self.chameleon_loader[name]
    return template(**ctx)


class ChameleonPlugin(Plugin):
    name = "chameleon"
    description = "Chameleon support for templating"

    def on_setup_env(self, **extra):
        template_paths = self.env.jinja_env.loader.searchpath
        self.env.chameleon_loader = PageTemplateLoader(template_paths)
        self.env.__class__.render_template = render_template
