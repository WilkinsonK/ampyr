import pytest

from ampyr import protocols as pt, typedefs as td


def test_oauth_flow_can_init(oauth_flow_object: pt.OAuth2Flow):
    """
    Dummy test that forces the target fixture to
    construct an `OAuth2Flow` object. Naturally
    fails if object cannot construct properly.
    """

    assert True


def test_oauth_flow_can_aquire_token(oauth_flow_object: pt.OAuth2Flow):
    """
    Validates that the target `OAuth2Flow` object
    can safely aquire a token from the host.
    """

    token = oauth_flow_object.aquire()

    assert isinstance(token, (str, td.CharToken)), "returned a non-token object!"


def test_oauth_flow_can_refresh_token(
    oauth_flow_object_expired_token: pt.OAuth2Flow):
    """
    In the event of a token being expired. The
    mechanism which aquires new tokens is
    expected to request a new auth token.
    """

    # Aquire initial token data.
    token = oauth_flow_object_expired_token.aquire()

    assert isinstance(token, (str, td.CharToken)), "returned a non-token object!"
