import os, time
import tempfile

import dotenv, pytest

from ampyr import cache
from ampyr.cache.managers import SimpleCacheManager

from ampyr import oauth2
from ampyr.oauth2.base import SimpleOAuth2Flow
from ampyr.oauth2.flows import _make_search_key

# Ensure secrets are loaded from '.env' file.
assert dotenv.load_dotenv(), "could not load environment variables!"


@pytest.fixture(scope="module", params=[
    oauth2.NullFlow,
    oauth2.AuthorizationFlow,
    oauth2.CredentialsFlow,
    oauth2.PKCEFlow])
def oauth_flow_class(request):
    """
    Returns one of the different `OAuth2Flow`
    classes.
    """

    yield request.param


@pytest.fixture(scope="module")
def oauth_flow_kwds():
    """
    Returns a mapping of values to pass to an
    `OAuth2Flow` constructor.
    """

    oauth_url = os.getenv("TEST_URL_FOR_OAUTH")

    kwds = dict(
        client_id=os.getenv("TEST_CLIENT_ID"),
        client_secret=os.getenv("TEST_CLIENT_SECRET"),
        client_userid=os.getenv("TEST_CLIENT_USERID"),
        url_for_oauth=f"{oauth_url}/{os.getenv('TEST_OAUTH_ENDPOINT')}",
        url_for_token=f"{oauth_url}/{os.getenv('TEST_TOKEN_ENDPOINT')}",
        url_for_redirect="http://localhost:9090",
        scope="user-library-read")

    yield kwds


@pytest.fixture
def oauth_flow_object(
    oauth_flow_class: type[SimpleOAuth2Flow],
    oauth_flow_kwds: dict):
    """
    Constructs an `OAuth2Flow` object.
    """

    yield oauth_flow_class(**oauth_flow_kwds)


@pytest.fixture
def oauth_flow_object_expired_token(oauth_flow_object: SimpleOAuth2Flow):
    """
    Forces the `OAuth2Flow` object to hold a
    token which is expired.
    """

    oauth_flow_object.aquire()

    key = _make_search_key(oauth_flow_object.auth_config)
    token_data = oauth_flow_object.cache_manager.find(key)
    if token_data:
        token_data["expires_at"] = int(time.time())
    oauth_flow_object.cache_manager.save(key, token_data)

    yield oauth_flow_object


@pytest.fixture(scope="module", params=[
    cache.MemoryCacheManager,
    cache.FileCacheManager,
    cache.ShelfCacheManager])
def cache_manager_class(request):
    """
    Returns one of the different `CacheManager`
    classes.
    """

    yield request.param


@pytest.fixture(scope="module")
def cache_manager_kwds():
    """
    Returns a mapping of values to pass to an
    `CacheManager` constructor.
    """

    kwds = dict()

    yield kwds


@pytest.fixture
def cache_manager_object(
    cache_manager_class: type[SimpleCacheManager],
    cache_manager_kwds: dict):
    """Constructs a `CacheManager` object."""

    olddir = os.curdir
    with tempfile.TemporaryDirectory() as dir:
        os.chdir(dir)
        yield cache_manager_class(**cache_manager_kwds)
        os.chdir(olddir)


@pytest.fixture(scope="module", params=[
    [314, 4280, 1738],
    "cacheable_string",
    {"name": "cacheable_dict", "token": "d3adb33f"}])
def cacheable_object(request):
    """
    Responds with some object that should be
    cacheable.
    """

    yield request.param
