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
    __driver__: pt.RESTDriver
    """
    Handles the low-level basics of interacting
    with a RESTful `Web API`.
    """

    __authflow__: pt.OAuth2Flow
    """
    Represents an Authentication Flow procedure
    defined by `OAuth2.0`. This object is
    responsible for aquiring an authentication
    token.
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

    def request_token(self):
        return self.__authflow__.aquire()

    def _build_authflow(self):
        self.__authflow__ = self.__driver__.build_authflow()

    def _build_driver(self, client_id: str, client_secret: str,
                      client_userid: td.OptString,
                      client_scope: td.OptAuthScope):

        args = (client_id, client_secret, client_userid, client_scope)
        self.__driver__ = self.__driver_cls__(*args)

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 client_userid: td.OptString = None,
                 client_scope: td.OptAuthScope = None):
        """Construct a `RESTClient` object."""

        self._build_driver(client_id, client_secret, client_userid,
                           client_scope)
        self._build_authflow()
