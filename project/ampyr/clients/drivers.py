"""Describes API driver mechanics."""

from ampyr import factories as ft, protocols as pt, typedefs as td
from ampyr import oauth2, cache


class BaseRESTDriver(pt.RESTDriver):
    """
    Handles basic meta behavior for subsequent
    classes and subclasses.

    Warning: Not meant to be used directly.
    """

    cache_manager: td.ClassVar[pt.CacheManager]
    """Brokers data to/from some cache."""

    authflow_cls: td.ClassVar[type[pt.OAuth2Flow]]
    """
    Authorization flow object used to aquire
    access tokens.
    """

    url_for_oauth: td.ClassVar[td.OptString] = None
    """
    Points to the URL used for `OAuth2.0`.
    """

    url_for_token: td.ClassVar[td.OptString] = None
    """
    Points to the URL responsible for requesting
    auth tokens.
    """

    client_id: str
    """
    `OAuth2.0` client identifier of your
    application.
    """

    client_secret: str
    """
    `OAuth2.0` client secret token of your
    application.
    """

    client_userid: td.OptString
    """
    Identifier used to allow access for the
    specified data of this user.
    """

    client_scope: td.OptAuthScope
    """
    Series of strings-- or keywords in a string
    separated by some delimiter-- to allow access
    to varying portions of data from the target
    `Web API`.
    """

    __authflow: pt.OAuth2Flow

    # Determines whether or not requests sent to
    # the host requires an `OAuth2.0` token.
    __requires_oauth: td.ClassVar[bool]

    @property
    def authflow(self):
        """
        Represents an Authentication Flow
        procedure defined by `OAuth2.0`. This
        object is responsible for aquiring an
        authentication token.
        """

        return self.__authflow

    # NOTE: this is to be the DEFAULT behavior.
    # When a user interacts with this class, they
    # should be encouraged to override this class
    # to produce their own OAuth2Flow
    # construction.
    def build_authflow(self):

        args = (self.client_id, self.client_secret, self.client_userid)

        kwds = {
            "scope": self.client_scope,
            "url_for_oauth": self.url_for_oauth,
            "url_for_token": self.url_for_token
        }

        return self.authflow_cls(*args, **kwds)

    def prepare_send_headers(self):
        return td.RequestHeaders()

    def prepare_send_params(self, params: td.OptMetaData):
        return params

    @cache.cachemethod
    def send(self):
        ...

    @classmethod
    def build_cache_manager(cls):
        return cache.NullCacheManager()

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 client_userid: td.OptString = None,
                 client_scope: td.OptAuthScope = None):
        """Construct a `RESTDriver` object."""

        self.client_id = client_id
        self.client_secret = client_secret
        self.client_userid = client_userid
        self.client_scope = client_scope

        self.__authflow = self.build_authflow()

    def __init_subclass__(cls, *, authflow_cls: type[pt.OAuth2Flow] = None):
        # Validate required ClassVar attributes.

        cls.authflow_cls = authflow_cls or oauth2.NullFlow
        cls.__requires_oauth = not isinstance(cls.authflow_cls,
                                              oauth2.NullFlow)

        cls.cache_manager = cls.build_cache_manager()


# Labeling the below as 'Basic' because we want
# to allow for this object-- in particular-- to
# be in use. Generally speaking, this object
# should be a 'catch-all' RESTDriver.
#
# Library users can define their own edge case
# drivers if necessary.
class BasicRESTDriver(BaseRESTDriver):
    """
    Basic implementation. Defines constructor for
    all subsequent derivatives.
    """
