# Copyright (C) 2018-2024 H. Turgut Uyar <uyar@tekir.org>
#
# lektor-chameleon is released under the BSD license.
# Read the included LICENSE.txt file for details.

__version__ = "0.8"

from functools import partial

from chameleon import PageTemplateLoader
from chameleon.loader import TemplateLoader
from lektor.context import get_ctx
from lektor.pluginsystem import Plugin
from lektor.reporter import reporter


chameleon_load = TemplateLoader.load


REG_FILTERS = [
    "filesizeformat", "indent", "latformat", "latlongformat", "longformat",
    "striptags", "tojson",
]

ENV_FILTERS = [
    "asseturl", "dateformat", "datetimeformat", "markdown", "truncate", "url",
    "wordwrap",
]


def load_template(self, filename, *args, **kwargs):
    ctx = get_ctx()
    if filename == ctx.source.datamodel.id + ".html":
        filename = ctx.source.datamodel.id + ".pt"
    template = chameleon_load(self, filename, *args, **kwargs)
    ctx.record_dependency(template.filename)
    return template


def render_template(self, name, pad=None, this=None, values=None, alt=None):
    if isinstance(name, list):
        name = name[0]
    ctx = self.make_default_tmpl_values(pad, this, values, alt, template=name)
    ctx.update(self.chameleon_env.globals)
    ctx.update(self.chameleon_env.filters)
    template = self.chameleon_env.loader.load(name)
    return template(**ctx)


class ChameleonEnvironment:
    def __init__(self, jinja_env) -> None:
        self.loader = PageTemplateLoader(jinja_env.loader.searchpath,
                                         auto_reload=True)
        self.globals = jinja_env.globals
        self.filters = {}
        for filter_name in REG_FILTERS:
            self.filters[filter_name] = jinja_env.filters[filter_name]
        for filter_name in ENV_FILTERS:
            self.filters[filter_name] = partial(jinja_env.filters[filter_name],
                                                jinja_env)


class ChameleonPlugin(Plugin):
    name = "chameleon"
    description = "Support for Chameleon templates."

    def on_setup_env(self, **extra):
        reporter.report_generic("Setting up to use Chameleon templates")
        self.env.chameleon_env = ChameleonEnvironment(self.env.jinja_env)
        TemplateLoader.load = load_template
        self.env.__class__.render_template = render_template
