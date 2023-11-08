import pytest
import salt.modules.test as testmod
import {{ package_namespace_pkg }}{{ package_name }}.modules.{{ package_name }}_mod as {{ package_name }}_module


@pytest.fixture
def configure_loader_modules():
    module_globals = {
        "__salt__": {"test.echo": testmod.echo},
    }
    return {
        {{ package_name }}_module: module_globals,
    }


def test_replace_this_this_with_something_meaningful():
    echo_str = "Echoed!"
    assert {{ package_name }}_module.example_function(echo_str) == echo_str
