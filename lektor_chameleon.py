from chameleon import PageTemplateLoader
from lektor.pluginsystem import Plugin


class Filter:
    def __init__(self, f, ctx):
        self.f = f
        self.ctx = ctx

    def __rrshift__(self, x):
        return self.f(self.ctx, x)


def render_template(self, name, pad=None, this=None, values=None, alt=None):
    ctx = self.make_default_tmpl_values(pad, this, values, alt, template=name)
    ctx.update(self.jinja_env.globals)

    filters = self.jinja_env.filters
    ctx["asseturl"] = Filter(filters["asseturl"], ctx)
    ctx["url"] = Filter(filters["url"], ctx)

    template = self.chameleon_loader[name]
    return template(**ctx)


class ChameleonPlugin(Plugin):
    name = "chameleon"
    description = "Chameleon support for templating"

    def on_setup_env(self, **extra):
        template_paths = self.env.jinja_env.loader.searchpath
        self.env.chameleon_loader = PageTemplateLoader(template_paths)
        self.env.__class__.render_template = render_template
