# Copyright (C) 2018-2026 H. Turgut Uyar <uyar@tekir.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__version__ = "0.12"

from functools import partial
from pathlib import Path

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
    if isinstance(filename, str):
        filename = [filename]
    for template_name in filename:
        html_suffix = template_name.rfind(".html")
        if html_suffix >= 0:
            template_name = template_name[:html_suffix] + ".pt"
        try:
            template = chameleon_load(loader, template_name, *args, **kwargs)
            ctx.record_dependency(template.filename)
            break
        except Exception:
            pass
    else:
        raise RuntimeError("no template found for %s" % filename)
    return template


def render_template(env, name, pad=None, this=None, values=None, alt=None):
    loader = env.chameleon_env.loader
    template = loader.load(name)
    ctx = env.make_default_tmpl_values(pad, this, values, alt, template=name)
    try:
        return template(**ctx)
    except Exception as e:
        template_dirname = Path(loader.search_path[0]).name
        exc_text = str(e)
        file_path = ""
        location = ""
        for line in exc_text.splitlines():
            tokens = line.split("- Filename:")
            if len(tokens) == 2:
                full_path = tokens[1].strip()
                if full_path.startswith("... "):
                    full_path = full_path[4:]
                path_parts = Path(full_path).parts
                index = next(
                    i
                    for i in reversed(range(len(path_parts)))
                    if path_parts[i] == template_dirname
                )
                file_path = str(Path(*path_parts[index:]))
                continue

            tokens = line.split("- Location:")
            if len(tokens) == 2:
                location = tokens[1].strip().replace(":", "")
                break
        if (file_path != "") and (location != ""):
            exc_text = "%(exc)s - file: %(tmpl)s - %(loc)s" % {
                "exc": f"{e.__class__.__name__}: {', '.join(e.args)}",
                "tmpl": f"'{file_path}'",
                "loc": location[1:-1],
            }
        raise RuntimeError(exc_text)


class ChameleonEnvironment:
    def __init__(self, jinja_env) -> None:
        self.loader = PageTemplateLoader(jinja_env.loader.searchpath)
        self.globals = jinja_env.globals
        self.filters = {}
        for filter_name in REG_FILTERS:
            self.filters[filter_name] = jinja_env.filters[filter_name]
        for filter_name in ENV_FILTERS:
            self.filters[filter_name] = partial(
                jinja_env.filters[filter_name],
                jinja_env,
            )


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
