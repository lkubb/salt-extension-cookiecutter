# Create Salt Extensions

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template that initializes a project structure for developing [Salt](https://github.com/saltstack/salt) extension modules.

The template files themselves are currently sourced almost verbatim from the official [create-salt-extension](https://github.com/saltstack/salt-extension) tool. This template provides the necessary scaffolding to render them via Cookiecutter (using some ugly hacks).

## Why
I like to manage the lifecycle of my projects via [cruft](https://cruft.github.io/cruft/), which wraps Cookiecutter to additionally provide (**1**) boilerplate updates after the initial project generation and (**2**) diffs of what you changed versus the generated data.

## How
### General remarks
You will need to specify the `loaders` argument as a comma-separated string of module types to generate (singular or plural forms are allowed, spaces ignored).[^1] The following module types are available:

* `auth`
* `beacon`
* `cache`
* `cloud`
* `engine`
* `executor`
* `fileserver`
* `grain`
* `log_handler`
* `matcher`
* `metaproxy`
* `module`
* `netapi`
* `output`
* `pillar`
* `pkgdb`
* `pkgfile`
* `proxy`
* `queue`
* `renderer`
* `returner`
* `roster`
* `runner`
* `sdb`
* `serializer`
* `state`
* `thorium`
* `token`
* `top`
* `wheel`
* `wrapper`

[^1]: Sadly Cookiecutter does not support [multichoice variables](https://github.com/cookiecutter/cookiecutter/issues/1002) via its interactive prompt currently. 

### Cruft
The recommended way to use this template is with [cruft](https://cruft.github.io/cruft/#installation). Once this tool is available, creating an extension can be as simple as running:

```console
    $ cruft create https://github.com/lkubb/salt-extension-cookiecutter
```

You will be asked several questions, after which the project skeleton should be available. It will additionally contain a `.cruft.json` file with the inputs you gave and the most recent commit hash of the template repository that was used when creating it.

Future boilerplate updates can be as simple as:

```console
    $ cruft update
```

And you can show a diff of the current state of the code versus the boilerplate at the time of generation by running:

```console
    $ cruft diff
```

This also allows you to modify the inputs in `.cruft.json` and apply them (to existing files). But: The following command will reset your changes to all known files! So better filter the output manually if you already started your work.

```console
    $ cruft diff | git apply  # resets all changes on existing files!
```

### Cookiecutter
You could just use the official tool instead. :)

Otherwise:

```console
    $ git clone https://github.com/lkubb/salt-extension-cookiecutter
    $ cookiecutter salt-extension-cookiecutter
```

## References
* The official tool is found here: https://github.com/saltstack/salt-extension
* The `salt-extensions` organization: https://github.com/salt-extensions
* `cruft` docs: https://cruft.github.io/cruft/
* `cookiecutter` docs: https://cookiecutter.readthedocs.io/en/stable/index.html
* An overview of modular systems in Salt: https://docs.saltproject.io/en/latest/topics/development/modules/index.html
* The Salt-specific `pytest` docs: https://pytest-salt-factories.readthedocs.io/en/latest/
