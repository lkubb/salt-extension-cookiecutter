import copy
import json
from datetime import datetime
from jinja2.ext import Extension
from pathlib import Path


PROMOTE_IGNORE = ("license", "loaders")

LICENSES = {
    "apache": "License :: OSI Approved :: Apache Software License",
}

# Part of a shamelessly ugly hack to promote variables in ``cookiecutter`` to
# global ones to avoid rewriting the original extension templates
# or not being able to use the ``cookiecutter`` CLI as is.
# Reasons:
# 1. I want this to keep this in sync with upstream without much hassle
# 2. I want this to be usable with cruft to autoupdate the generated project

cc = None
cc_vars = tuple(
    x
    for x in json.loads(
        (Path(__file__).parent.parent / "cookiecutter.json").read_text()
    )
    if not x.startswith("_")
)


def _devour(cookie):
    """
    This will be called by a prerender hook and shoves the nicely scoped
    Jinja context into this module's globals in order for us to get access
    to user-defined vars.
    """
    global cc
    cc = copy.deepcopy(cookie)


class Year(Extension):
    """
    Defines the current year as a global variable named ``year``.
    """

    def __init__(self, env):
        env.globals.update(year=datetime.now().year)


class LazyRender:
    """
    A class that can be instantiated during environment setup that will
    look up its value later once the pre_gen_project hook has loaded the
    ``cookiecutter`` context dict into this module's globals.

    Afaik there is no other easy, less horrendous way to keep the upstream templates
    as-is since only law-abiding functions, tests and filters can get access
    to the template rendering context. There might be a way to write a custom
    parser, but this hack works and should be fine for the purpose.
    """

    def __init__(self, func, *args):
        self.func = func
        self.args = args
        self.resolved = None

    def _load(self):
        if self.resolved is None:
            self.resolved = self.func(*self.args)
        return self.resolved

    def __str__(self):
        return str(self._load())

    def __repr__(self):
        return str(self._load())

    def __bool__(self):
        ret = self._load()
        if isinstance(ret, (bool, int)):
            return bool(ret)
        return bool(str(ret))

    def __iter__(self):
        return iter(self._load())

    def __getattr__(self, attr):
        self._load()
        return getattr(self.resolved, attr)

    def __getitem__(self, key):
        self._load()
        return self.resolved[key]

    def values(self):
        self._load()
        return self.resolved.values()

    def items(self):
        self._load()
        return self.resolved.items()


def digest(var):
    """
    The function to be called by the LazyRender class for general vars
    that don't need special handling.
    """
    return cc[var]


class SaltExt(Extension):
    """
    Helps botching up the Jinja environment.
    """

    def __init__(self, env):
        super().__init__(env)
        env.globals.update(sledgehammer=_devour)
        promote = {
            var: LazyRender(digest, var) for var in cc_vars if var not in PROMOTE_IGNORE
        }
        env.globals.update(
            **promote,
            package_namespace=LazyRender(_package_namespace),
            package_namespace_pkg=LazyRender(_package_namespace_pkg),
            package_namespace_path=LazyRender(_package_namespace_path),
            license_name=LazyRender(_license_name),
            license_classifier=LazyRender(_license_classifier),
            loaders=LazyRender(_loaders),
        )


def _package_namespace():
    return "" if cc["no_saltext_namespace"] else "saltext"


def _package_namespace_pkg():
    ns = _package_namespace()
    if not ns:
        return ns
    return ns + "."


def _package_namespace_path():
    ns = _package_namespace()
    if not ns:
        return ns
    return ns + "/"


def _license_name():
    if cc["license"] == "other":
        pass
    elif cc["license"]:
        license_classifier = LICENSES[cc["license"]]
        license_name = license_classifier.split(" :: ")[-1]
        return license_name
    return ""


def _license_classifier():
    if cc["license"] == "other":
        pass
    elif cc["license"]:
        return LICENSES[cc["license"]]
    return ""


def _loaders():
    load = cc["loaders"]
    if not isinstance(load, list):
        return [x.strip() for x in load.split(",")]
    return load
