import pathlib
import re

root = pathlib.Path(__file__).resolve().parent


def _find(path, pattern):
    return re.search(pattern, (root / path).read_text(), re.M).group(1)


def test_versions_agree():
    v = _find("pyproject.toml", r'^version\s*=\s*"([^"]+)"')
    assert _find("__init__.py", r'__version__\s*=\s*"([^"]+)"') == v
    assert _find("CITATION.cff", r"^version:\s*(\S+)") == v
