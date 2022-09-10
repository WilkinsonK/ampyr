"""Describes API driver mechanics."""

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

    requires_oauth: td.ClassVar[bool] = False
    """
    Determines whether or not requests sent to
    the host requires an `OAuth2.0` token.
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

    client_id: td.ClassVar[td.OptString] = None
    """
    `OAuth2.0` client identifier of your
    application.
    """

    client_secret: td.ClassVar[td.OptString] = None
    """
    `OAuth2.0` client secret token of your
    application.
    """

    client_userid: td.OptString = None
    """
    Identifier used to allow access for the
    specified data of this user.
    """

    client_scope: td.OptAuthScope = None
    """
    Series of strings-- or keywords in a string
    separated by some delimiter-- to allow access
    to varying portions of data from the target
    `Web API`.
    """

    def build_authflow(self):

        args = (
            self.client_id,
            self.client_secret,
            self.client_userid)

        kwds = {
            "scope": self.client_scope,
            "url_for_oauth": self.url_for_oauth,
            "url_for_token": self.url_for_token}

        return oauth2.NullFlow(*args, **kwds)
