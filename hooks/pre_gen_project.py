"""
This checks the list of specified loader module types against the ones
that are known, ignoring spaces and singular/plural forms.

It is also part of the ugly hack for keeping the upstream templates
working with Cookiecutter via the following:

Pass the template context var ``cookiecutter`` into the globals of our
Jinja extensions module. Meh. Caveman go boom:
{%- do sledgehammer(cookiecutter) %}
"""

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

selected_mods = {{ cookiecutter.loaders | jsonify }}
if not isinstance(selected_mods, list):
    selected_mods = [x.strip() for x in selected_mods.split(",")]

unknown = set(selected_mods).difference(SALT_LOADERS)
# Allow singular and plural forms to be specified since it will work anyways
unknown_filtered = {
    x
    for x in unknown
    if x.rstrip("s") not in SALT_LOADERS and x + "s" not in SALT_LOADERS
}
if unknown_filtered:
    raise ValueError(
        f"The following loaders are unknown: {', '.join(unknown_filtered)}"
    )
