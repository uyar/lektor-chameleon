from importlib import metadata

import lektor_chameleon


def test_installed_version_should_match_tested_version():
    assert metadata.version("lektor_chameleon") == lektor_chameleon.__version__
