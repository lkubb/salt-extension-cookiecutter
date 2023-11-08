"""
Salt SDB module
"""
import logging

log = logging.getLogger(__name__)

__virtualname__ = "{{ package_name }}"


def __virtual__():
    # To force a module not to load return something like:
    #   return (False, "The {{ project_name }} sdb module is not implemented yet")

    # Replace this with your own logic
    if "{{package_name}}.example_function" not in __salt__:
        return False, "The '{{package_name}}' execution module is not available"
    return __virtualname__


def get(key, profile=None):
    """
    This example function should be replaced

    CLI Example:

    .. code-block:: bash

        salt '*' sdb.get "sdb://{{ package_name}}/foo"
    """
    return key
