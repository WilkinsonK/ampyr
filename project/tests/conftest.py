import os

import dotenv, pytest

from ampyr import oauth2
from ampyr.oauth2 import base

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
        url_for_redirect="http://localhost:9090")

    yield kwds


@pytest.fixture
def oauth_flow_object(
    oauth_flow_class: type[base.SimpleOAuth2Flow],
    oauth_flow_kwds: dict):
    """
    Constructs an `OAuth2Flow` object.
    """

    yield oauth_flow_class(**oauth_flow_kwds)
