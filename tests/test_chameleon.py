import os
import subprocess
from importlib import metadata
from pathlib import Path
from shutil import rmtree
from textwrap import dedent

import pytest

import lektor_chameleon


LEKTOR_ROOT = Path("/dev/shm/lektor-chameleon")
LEKTOR_PAGE_TEMPLATE = LEKTOR_ROOT / "templates" / "page.pt"
LEKTOR_HOME_SRC = LEKTOR_ROOT / "content" / "contents.lr"
LEKTOR_HOME_DST = LEKTOR_ROOT / "_build" / "index.html"


@pytest.fixture(autouse=True)
def lektor_init():
    rmtree(LEKTOR_ROOT, ignore_errors=True)
    LEKTOR_PAGE_TEMPLATE.parent.mkdir(parents=True, exist_ok=True)
    LEKTOR_HOME_SRC.parent.mkdir(parents=True, exist_ok=True)
    LEKTOR_HOME_DST.parent.mkdir(parents=True, exist_ok=True)

    project_file = LEKTOR_ROOT / "project.lektorproject"
    project_file.parent.mkdir(parents=True, exist_ok=True)
    project_file.write_text(dedent("""
        [project]
        name = Project
        output_path = _build
    """))

    model_file = LEKTOR_ROOT / "models" / "page.ini"
    model_file.parent.mkdir(parents=True, exist_ok=True)
    model_file.write_text(dedent("""
        [model]
        name = Page
        label = {{ this.title }}

        [fields.title]
        label = Title
        type = string

        [fields.pub_date]
        label = Publication Date
        type = date

        [fields.body]
        label = Body
        type = markdown
    """))

    style_file = LEKTOR_ROOT / "assets" / "static" / "style.css"
    style_file.parent.mkdir(parents=True, exist_ok=True)
    style_file.write_text("")

    current_dir = os.getcwd()
    os.chdir(LEKTOR_ROOT)
    yield

    os.chdir(current_dir)
    rmtree(LEKTOR_ROOT)


def test_installed_version_should_match_tested_version():
    assert metadata.version("lektor_chameleon") == lektor_chameleon.__version__


@pytest.mark.parametrize(("content", "template", "output"), [
    (
        """title: Page title\n""",
        """${ this.title }""",
        """Page title\n""",
    ),
    (
        """body: Page body\n""",
        """${ this.body }""",
        """<p>Page body</p>\n\n""",
    ),
])
def test_interpolation_should_be_substituted_by_result(content, template, output):
    LEKTOR_HOME_SRC.write_text(content)
    LEKTOR_PAGE_TEMPLATE.write_text(template)
    subprocess.run(["lektor", "build"])
    generated = LEKTOR_HOME_DST.read_text()
    assert generated == output


@pytest.mark.parametrize(("content", "template", "output"), [
    (
        """title: Page title\n""",
        """<title tal:content="this.title">Title placeholder</title>""",
        """<title>Page title</title>\n""",
    ),
    (
        """body: Page body\n""",
        """<body tal:content="this.body">\nBody placeholder\n</body>""",
        """<body><p>Page body</p>\n</body>\n""",
    ),
])
def test_tal_content_should_replace_content(content, template, output):
    LEKTOR_HOME_SRC.write_text(content)
    LEKTOR_PAGE_TEMPLATE.write_text(template)
    subprocess.run(["lektor", "build"])
    generated = LEKTOR_HOME_DST.read_text()
    assert generated == output


@pytest.mark.parametrize(("content", "template", "output"), [
])
def test_added_filter_should_produce_correct_result(content, template, output):
    LEKTOR_HOME_SRC.write_text(content)
    LEKTOR_PAGE_TEMPLATE.write_text(template)
    subprocess.run(["lektor", "build"])
    generated = LEKTOR_HOME_DST.read_text()
    assert generated == output


@pytest.mark.parametrize(("content", "template", "output"), [
    (
        """\n""",
        """${ asseturl('/static/style.css') }""",
        """static/style.css?h=da39a3ee\n""",
    ),
    (
        """pub_date: 2024-04-28\n""",
        """${ dateformat(this.pub_date) }""",
        """Apr 28, 2024\n""",
    ),
    (
        """pub_date: 2024-04-28\n""",
        """${ datetimeformat(this.pub_date) }""",
        """Apr 28, 2024, 12:00:00 AM\n""",  # invisible space between 00 and AM
    ),
    (
        """\n""",
        """${ latformat(3.141592) }""",
        """3° 8′ 29″ N\n""",
    ),
    (
        """\n""",
        """${ latlongformat((3.141592, 3.141592)) }""",
        """3° 8′ 29″ N, 3° 8′ 29″ E\n""",
    ),
    (
        """\n""",
        """${ longformat(3.141592) }""",
        """3° 8′ 29″ E\n""",
    ),
    (
        """\n""",
        """${ markdown('*page text*') }""",
        """<p><em>page text</em></p>\n\n""",
    ),
    (
        """\n""",
        """${ tojson({'foo': True}) }""",
        """{"foo": true}\n""",
    ),
    (
        """\n""",
        """${ url('/static/style.css') }""",
        """static/style.css\n""",
    ),
])
def test_added_lektor_filter_should_produce_same_result(content, template, output):
    LEKTOR_HOME_SRC.write_text(content)
    LEKTOR_PAGE_TEMPLATE.write_text(template)
    subprocess.run(["lektor", "build"])
    generated = LEKTOR_HOME_DST.read_text()
    assert generated == output


@pytest.mark.parametrize(("content", "template", "output"), [
    (
        """\n""",
        """${ filesizeformat(1500000, binary=True) }""",
        """1.4 MiB\n""",
    ),
    (
        """body: Page body\n""",
        """<body>\n${ indent(this.body.html, width=2, first=True) }\n</body>""",
        """<body>\n  <p>Page body</p>\n\n</body>\n""",
    ),
    (
        """body: *Page body*\n""",
        """${ striptags(this.body) }""",
        """Page body\n""",
    ),
    (
        """title: foo bar baz qux\n""",
        """${ truncate(this.title, length=9) }""",
        """foo...\n""",
    ),
    (
        """body: Lorem ipsum dolor sit amet\n""",
        """<body>\n${ structure:wordwrap(this.body.html, width=10) }\n</body>""",
        """<body>\n<p>Lorem\nipsum\ndolor sit\namet</p>\n</body>\n""",
    ),
])
def test_added_jinja_filter_should_produce_same_result(content, template, output):
    LEKTOR_HOME_SRC.write_text(content)
    LEKTOR_PAGE_TEMPLATE.write_text(template)
    subprocess.run(["lektor", "build"])
    generated = LEKTOR_HOME_DST.read_text()
    assert generated == output
