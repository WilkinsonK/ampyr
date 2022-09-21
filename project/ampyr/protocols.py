"""
Definitions below are for the interfaces used in
this package.
"""

from abc import abstractmethod
from typing import Protocol

from ampyr import typedefs as td


class CacheManager(Protocol[td.GT]):
    """
    Brokers transactions of cached data.
    Primarily for the use of relieving more
    expensive transactions.
    """

    @abstractmethod
    def find(self, key: str) -> None | td.GT:
        """
        Attempt to retrieve data from the cache
        assigned to the given key. Returns `None`
        if it fails.
        """

    @abstractmethod
    def save(self, key: str, data: td.GT) -> td.GT:
        """
        Attempt to insert data into the cache,
        assigning it to the given key.
        """


class HasCacheHandler(Protocol):
    """
    Some object which has an attribute named
    'cache_manager' and is of type
    `CacheManager`.
    """

    cache_manager: CacheManager
    """Brokers data to/from some cache."""


class RemoteAccessManager(Protocol):
    """
    Connects to some remote host or service.
    """

    @abstractmethod
    def detach(self) -> td.ReturnState:
        """Disconnects from the target."""

    @abstractmethod
    def attach(self) -> td.ReturnState:
        """Connects to the target."""

    @abstractmethod
    def ping(self) -> td.ReturnState:
        """
        Sends a ping returning the state of the
        target.
        """


class MetaConfig(Protocol):
    """
    Some family or group of attributes intended
    for a specific purpose.
    """

    def asdict(self) -> td.MetaData:
        """
        Breaks down this `MetaConfig` into
        a dictionary.
        """


class OAuth2Flow(Protocol):
    """
    Represents an Authentication Flow procedure
    defined by `OAuth2.0`. This object is
    responsible for aquiring an authentication
    token.
    """

    @abstractmethod
    def aquire(self) -> td.CharToken:
        """Attempt to retrieve an auth token."""


class SupportsSerialize(Protocol[td.GT]):
    """
    An object which can transform data to/from a
    raw state (i.e. a string or byte array) and
    Python objects.
    """

    @abstractmethod
    def loads(self, data: td.StrOrBytes, *args, **kwds) -> td.GT:
        """
        Converts some raw state data into a
        Python object.
        """

    @abstractmethod
    def dumps(self, data: td.GT, *args, **kwds) -> td.StrOrBytes:
        """
        Converts some Python object into some raw
        state data.
        """


class RESTDriver(Protocol):
    """
    Handles the low-level basics of interacting
    with a RESTful `Web API`.
    """

    # Methods defined below in this protocol
    # should be treated as hooks that are then
    # used by internal methods through higher
    # objects.
    #
    # In other words, for every abstract method,
    # there will be a mirror method defined in
    # the basic driver which calls these hooks.
    @abstractmethod
    def build_authflow(self) -> OAuth2Flow:
        """
        Creates a new `OAuth2Flow` instance based
        on parameters given to the driver.
        """

    @abstractmethod
    def prepare_send_headers(self) -> td.RequestHeaders:
        """
        Prepares the headers applied to a REST
        call sent to the target `Web API`.
        """

    @abstractmethod
    def prepare_send_params(self, params: td.OptMetaData) -> td.OptMetaData:
        """
        Prepares the parameters applied to a
        REST call sent to the target `Web API`.
        """

    @abstractmethod
    def send(self,
             method: str,
             uri: str,
             *,
             params: td.OptMetaData = None,
             timeouts: td.Optional[td.Sequence[float]] = None) -> td.Response:
        """
        Sends a request to the driver's target
        host.
        """

    @classmethod
    @abstractmethod
    def build_cache_manager(cls) -> CacheManager:
        """Create a `CacheManager` object."""


class RESTClient(Protocol):
    """
    Broker object for making calls to the target
    RESTful `Web API`.
    """
