"""
Defines basic behavior of objects responsible for
brokering calls to/from a target `Web API`.
"""

from ampyr import factories as ft, protocols as pt, typedefs as td
from ampyr.clients import drivers


# Labeling the below as 'Base' because we need to
# define some pre-subclass initialization
# behaviors. Strictly speaking, we do not-- and
# should not expect this class to be initialized
# directly.
class BaseRESTClient(pt.RESTClient):
    """
    Handles basic meta behavior for subsequent
    classes and subclasses.

    Warning: Not meant to be used directly.
    """

    __driver_cls__: type[pt.RESTDriver]
    __driver__:     pt.RESTDriver
    """
    Handles the low-level basics of interacting
    with a RESTful `Web API`.
    """

    def __init_subclass__(cls, *, driver: type[pt.RESTDriver] = None):
        super().__init_subclass__()

        if driver is None:
            driver = drivers.BasicRESTDriver
        cls.__driver_cls__ = driver


class SimpleRESTClient(BaseRESTClient, driver=drivers.BasicRESTDriver):
    """
    Basic implementation. Defines constructor for
    all subsequent derivatives.

    Warning: Not meant to be used directly.
    """

    def _build_authflow(self):
        return self.__driver__.build_authflow()
