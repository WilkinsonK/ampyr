"""
Defines basic behavior of objects responsible for
brokering calls to/from a target `Web API`.
"""

from ampyr import factories as ft, protocols as pt, typedefs as td
from ampyr import oauth2


class BaseRESTClient(pt.RESTClient):

    __driver_factory__: ft.Callable[[], pt.RESTDriver]
