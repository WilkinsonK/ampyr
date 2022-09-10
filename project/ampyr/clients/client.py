"""
Defines basic behavior of objects responsible for
brokering calls to/from a target `Web API`.
"""

from ampyr import factories as ft, protocols as pt, typedefs as td
from ampyr import oauth2


# Labeling the below as 'Basic' because we want
# to allow for this object-- in particular-- to
# be in use. Generally speaking, this object
# should be a 'catch-all' RESTDriver.
#
# Library users can define their own edge case
# drivers if necessary.
class BasicRESTDriver(pt.RESTDriver):

    requires_oauth: td.ClassVar[bool]
    """
    Determines whether or not requests sent to
    the host requires an `OAuth2.0` token.
    """

    def build_authflow(self):
        ...


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
    """
    Handles the low-level basics of interacting
    with a RESTful `Web API`.
    """

    def __init_subclass__(cls, *, driver: type[pt.RESTDriver] = None):
        super().__init_subclass__()

        if driver is None:
            driver = BasicRESTDriver
        cls.__driver_cls__ = driver


class SimpleRESTClient(BaseRESTClient, driver=BasicRESTDriver):
    """
    Basic implementation. Defines constructor for
    all subsequent derivatives.

    Warning: Not meant to be used directly.
    """
