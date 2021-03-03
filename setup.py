from re import MULTILINE, search

from setuptools import setup  # type: ignore

__NAME__ = "normal_api"

with open("README.md") as f:
    readme = f.read()

# source: https://github.com/Rapptz/discord.py/blob/master/setup.py#L9-L10
with open(f"{__NAME__}/__init__.py") as f:
    content = f.read()
    version = search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content, MULTILINE
    ).group(1)
    author = search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]', content, MULTILINE).group(
        1
    )
    _license = search(
        r'^__license__\s*=\s*[\'"]([^\'"]*)[\'"]', content, MULTILINE
    ).group(1)

setup(
    name = f"{__NAME__}.py",
    description = "An Easy-To-Use Wrapper for the Normal API",
    long_description = readme,
    long_description_content_type = "text/markdown",
    version = version,
    packages = [__NAME__],
    url = F"https://github.com/Soheab/{__NAME__}.py",
    download_url = f"https://github.com/Soheab/{__NAME__}.py/archive/v{version}.tar.gz",
    license = _license,
    author = author,
    install_requires = ["aiohttp"],
    keywords = [
        __NAME__,
        "discord",
        "api",
        "wrapper",
        "memes",
        "image",
        "discord.py",
    ],
    project_urls = {
        "Discord": "https://discord.gg/FyQ3CnmnQK",
        "Documentation": f"https://github.com/Soheab/{__NAME__}.py/blob/main/docs.md",
    },
    python_requires = ">=3.6",
)
