"""
This script removes unwanted boilerplate after generation
and ensures no_saltext_namespace is respected.
"""

import shutil
from pathlib import Path

# Imports for the following constants will not work since this
# script is copied to a temporary location by Cookiecutter.

SALT_LOADERS = (
    "auth",
    "beacons",
    "cache",
    "cloud",
    "engines",
    "executor",
    "fileserver",
    "grain",
    "log_handlers",
    "matchers",
    "metaproxy",
    "module",
    "netapi",
    "output",
    "pillar",
    "pkgdb",
    "pkgfiles",
    "proxy",
    "queue",
    "renderer",
    "returner",
    "roster",
    "runner",
    "sdb",
    "serializers",
    "states",
    "thorium",
    "tokens",
    "top",
    "wheel",
    "wrapper",
)

SINGULAR_MODULE_DIRS = (
    "auth",
    "cache",
    "fileserver",
    "metaproxy",
    "netapi",
    "output",
    "pillar",
    "pkgdb",
    "proxy",
    "roster",
    "sdb",
    "thorium",
    "wheel",
    "wrapper",
)


# Rename .j2 template files
for tpl in Path(".").rglob("*.j2"):
    tpl.rename(tpl.with_suffix(""))


# Remove all unwanted module type boilerplate after generation
selected_mods = {{ cookiecutter.loaders | jsonify }}
if not isinstance(selected_mods, list):
    selected_mods = [x.strip() for x in selected_mods.split(",")]

for mod in SALT_LOADERS:
    if (
        mod in selected_mods
        or mod.rstrip("s") in selected_mods
        or mod + "s" in selected_mods
    ):
        continue
    loader_name = mod.rstrip("s") + ("s" if mod not in SINGULAR_MODULE_DIRS else "")
    shutil.rmtree(
        Path("src") / "saltext" / "{{ cookiecutter.package_name }}" / loader_name
    )
    shutil.rmtree(Path("tests") / "unit" / loader_name)
    shutil.rmtree(Path("tests") / "integration" / loader_name)


# If the project should not use the `saltext` namespace, move it
# one level up.
if {{ cookiecutter.no_saltext_namespace }} is True:
    module_dir = Path("src/saltext/{{ cookiecutter.package_name }}")
    module_dir.rename(module_dir.parent.parent / module_dir.name)
    (module_dir.parent.parent / "saltext").rmdir()
