import os
import subprocess
from importlib import metadata
from pathlib import Path
from shutil import copytree, rmtree

from pytest import fixture

import lektor_chameleon


LEKTOR_SRC_ROOT = Path(__file__).parent / "project"
LEKTOR_ROOT = Path("/dev/shm/lektor-chameleon")
LEKTOR_BUILD_ROOT = LEKTOR_ROOT / "_build"
LEKTOR_BUILD_INDEX = LEKTOR_BUILD_ROOT / "index.html"


@fixture(autouse=True)
def lektor_init():
    rmtree(LEKTOR_ROOT, ignore_errors=True)
    copytree(LEKTOR_SRC_ROOT, LEKTOR_ROOT)

    current_dir = os.getcwd()
    os.chdir(LEKTOR_ROOT)
    yield

    os.chdir(current_dir)
    rmtree(LEKTOR_ROOT)


def test_installed_version_should_match_tested_version():
    assert metadata.version("lektor_chameleon") == lektor_chameleon.__version__


def test_tal_content_should_replace_content():
    subprocess.run(["lektor", "build"])
    output = LEKTOR_BUILD_INDEX.read_text()
    assert '<main><p>Page content.</p>\n</main>' in output


def test_interpolation_should_replace_content():
    subprocess.run(["lektor", "build"])
    output = LEKTOR_BUILD_INDEX.read_text()
    assert '<title>Page title</title>' in output


def test_context_filter_should_work():
    subprocess.run(["lektor", "build"])
    output = LEKTOR_BUILD_INDEX.read_text()
    assert '<link rel="stylesheet" href="static/style.css"/>' in output


def test_str_filter_should_work():
    subprocess.run(["lektor", "build"])
    output = LEKTOR_BUILD_INDEX.read_text()
    assert '<meta name="keywords" content="chameleon"/>' in output


def test_str_filter_with_parameters_should_work():
    subprocess.run(["lektor", "build"])
    output = LEKTOR_BUILD_INDEX.read_text()
    assert '<h1>  Page title  </h1>' in output


def test_jinja_env_filter_should_work():
    subprocess.run(["lektor", "build"])
    output = LEKTOR_BUILD_INDEX.read_text()
    assert '<footer>Page\ntitle</footer>' in output
