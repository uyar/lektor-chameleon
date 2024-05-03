# Copyright (C) 2018-2024 H. Turgut Uyar <uyar@tekir.org>
#
# lektor-chameleon is released under the BSD license.
# Read the included LICENSE.txt file for details.

__version__ = "0.9"

from functools import partial

from chameleon import PageTemplateLoader
from chameleon.loader import TemplateLoader
from lektor.context import get_ctx
from lektor.environment import Environment
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


def load_template(loader, filename, *args, **kwargs):
    ctx = get_ctx()
    html_suffix = filename.rfind(".html")
    if html_suffix >= 0:
        filename = filename[:html_suffix] + ".pt"
    template = chameleon_load(loader, filename, *args, **kwargs)
    ctx.record_dependency(template.filename)
    return template


def render_template(env, name, pad=None, this=None, values=None, alt=None):
    template = env.chameleon_env.loader.load(name)
    ctx = env.make_default_tmpl_values(pad, this, values, alt, template=name)
    return template(**ctx)


class ChameleonEnvironment:
    def __init__(self, jinja_env) -> None:
        self.loader = PageTemplateLoader(jinja_env.loader.searchpath)
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
        Environment.render_template = render_template

    def on_process_template_context(self, context, **extra):
        context.update(self.env.chameleon_env.globals)
        context.update(self.env.chameleon_env.filters)
