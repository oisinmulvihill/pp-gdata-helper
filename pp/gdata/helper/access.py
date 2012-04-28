# -*- coding: utf-8 -*-
"""
"""
import logging

import gdata
import gdata.auth
import gdata.docs.service


def get_log(extra=None):
    m = "pp.gdata.helper.access"
    if extra:
        m = "%s.%s" % (m, extra)
    return logging.getLogger(m)


class OAuthServiceAccess(object):
    """Facilitates the '3 Legged' OAuth process to gain access one or many
    google services.

    The services are specified via the scopes passed in to the constructor.

    This is used to recover the access_token needed use private data, for
    one or more google service. The service to request access to is given
    in the scope.

    """
    def __init__(self, scopes, consumer_key, consumer_secret):
        """
        :param scopes: The services to request / gain access to.

        :param consumer_key: the domain identifying 3rd party web application.

        :param consumer_secret: the secret generated during registration.

        """
        self.log = get_log("OAuthServiceAccess")
        self.scopes = scopes
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.services = gdata.service.GDataService()
        self.log.debug('Set OAuth input parameters.')
        self.services.SetOAuthInputParameters(
            gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
            self.consumer_key,
            consumer_secret=self.consumer_secret,
        )

    def generate_auth_url(self, **kwargs):
        """Use OAuth to get a request token and the authorisation URL.

        :returns: (Request Token String, Auth URL)

        """
        self.log.debug('Fetch OAuth Request token.')

        if "scopes" not in kwargs:
            self.log.debug('Adding scopes to Fetch OAuth Request.')
            kwargs["scopes"] = self.scopes

        request_token = self.services.FetchOAuthRequestToken(**kwargs)

        self.log.debug('Set the fetched OAuth token.')
        self.services.SetOAuthToken(request_token)

        self.log.debug('Generate OAuth authorization URL.')
        auth_url = self.services.GenerateOAuthAuthorizationURL()

        self.log.info("URL <%s>" % auth_url)

        return (str(request_token), auth_url)

    def gain_access_token(self, request_token, oauth_verifier=""):
        """Called at some point after the Customer has given permission for out
        access.

        We now need to exchange the request_token for an access_token. Once we
        have the access_token, we should be able to access contact and calendar
        data. The access_token can be stored and used with all future calls.

        The Customer, who's account we are accessing, can deny access. This
        will mean the access_token will be invalidated.

        :param request_token: The request_token string to be upgraded.

        :returns: The access token string which replaces the request_token.

        """
        # request_token e.g:
        # "oauth_token_secret=GP4xmW9dQzBKBWcm0dYJxiIU \
        #        & \
        #        oauth_token=4%2FgvYvD2N8q4N8iJRQBLF5qRVDLHEN"
        #
        self.log.debug(
            "Upgrade to access token for request_token <%s>." % request_token
        )

        # Set the request_token before attempting to upgrade:
        self.set_token(request_token)

        self.services.UpgradeToOAuthAccessToken(oauth_verifier=oauth_verifier)
        access_token = self.services.token_store.find_token(
            self.services.current_token.scopes[0]
        )
        access_token = str(access_token)

        # Should this get logged at all?
        self.log.debug('Success, the access_token is <%s>' % access_token)

        return access_token

    @classmethod
    def oath_token(cls, scopes, oauth_input_params, token_str):
        """Convert the given token string into a gdata.auth.OAuth instance.
        """
        token = gdata.auth.OAuthToken(
            scopes=scopes,
            oauth_input_params=oauth_input_params
        )
        token.set_token_string(token_str)

        return token

    def set_token(self, token_str):
        """Set the request or access token for communication.

        :param token_str: The Request or Access token string.

        :returns: None.

        """
        token = self.oath_token(
            self.scopes,
            self.services.GetOAuthInputParameters(),
            token_str,
        )
        self.services.SetOAuthToken(token)

    def get_token(self):
        """Return the current gdata.auth.OAuthToken instance."""
        return self.services.current_token
