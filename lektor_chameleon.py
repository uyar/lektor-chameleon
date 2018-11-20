from chameleon import PageTemplateLoader
from lektor.pluginsystem import Plugin


def render_template(self, name, pad=None, this=None, values=None, alt=None):
    ctx = self.make_default_tmpl_values(pad, this, values, alt, template=name)
    ctx.update(self.jinja_env.globals)

    filters = self.jinja_env.filters
    ctx["asseturl"] = lambda *a, **kw: filters["asseturl"](ctx, *a, **kw)
    ctx["url"] = lambda *a, **kw: filters["url"](ctx, *a, **kw)

    template = self.chameleon_loader[name]
    return template(**ctx)


class ChameleonPlugin(Plugin):
    name = "chameleon"
    description = "Chameleon support for templating"

    def on_setup_env(self, **extra):
        template_paths = self.env.jinja_env.loader.searchpath
        self.env.chameleon_loader = PageTemplateLoader(template_paths)
        self.env.__class__.render_template = render_template
