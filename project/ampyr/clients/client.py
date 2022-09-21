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

    __driver_cls: type[pt.RESTDriver]
    __driver: pt.RESTDriver
    """
    Handles the low-level basics of interacting
    with a RESTful `Web API`.
    """

    @property
    def driver(self):
        return self.__driver

    def __init_subclass__(cls, *, driver: type[pt.RESTDriver] = None):
        super().__init_subclass__()

        if driver is None:
            driver = drivers.BasicRESTDriver
        cls.__driver_cls = driver

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 client_userid: td.OptString = None,
                 client_scope: td.OptAuthScope = None):
        """Construct a `RESTClient` object."""

        args = (client_id, client_secret, client_userid, client_scope)
        self.__driver = self.__driver_cls(*args)  #type: ignore[call-arg]


class SimpleRESTClient(BaseRESTClient):
    """
    Basic implementation. Defines constructor for
    all subsequent derivatives.

    Warning: Not meant to be used directly.
    """
