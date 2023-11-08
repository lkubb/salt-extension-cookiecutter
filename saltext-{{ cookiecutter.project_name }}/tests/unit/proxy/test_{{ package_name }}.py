import pytest
import {{ package_namespace_pkg }}{{ package_name }}.proxy.{{ package_name }}_mod as {{ package_name }}_proxy


@pytest.fixture
def configure_loader_modules():
    module_globals = {
        "__salt__": {"this_does_not_exist.please_replace_it": lambda: True},
    }
    return {
        {{ package_name }}_proxy: module_globals,
    }


def test_replace_this_this_with_something_meaningful():
    assert "this_does_not_exist.please_replace_it" in {{ package_name }}_proxy.__salt__
    assert {{ package_name }}_proxy.__salt__["this_does_not_exist.please_replace_it"]() is True
