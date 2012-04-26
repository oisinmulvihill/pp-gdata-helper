# -*- coding: utf-8 -*-
#
# Based on the OAuthSample in the gdata-x.y.z/samples/oauth/oauth_example.py
#
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
    """Uses OAuth to gain access one or many google services.

    This is used to recover the access_token needed use private data, for
    one or more google service. The service to request access to is given
    in the scope.

    """
    def __init__(self, scopes, consumer_key, consumer_secret):
        """
        :param scopes: The services to request / gain access to.

        :param consumer_key: string Domain identifying third_party web application.

        :param consumer_secret: string Secret generated during registration.

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

    def generate_auth_url(self):
        """Use OAuth to get a request token and the authorisation URL.

        :returns: (Request Token String, Auth URL)

        """
        self.log.debug('Fetch OAuth Request token.')
        request_token = self.services.FetchOAuthRequestToken(self.scopes)

        self.log.debug('Set the fetched OAuth token.')
        self.services.SetOAuthToken(request_token)

        self.log.debug('Generate OAuth authorization URL.')
        auth_url = self.services.GenerateOAuthAuthorizationURL()

        self.log.info("URL <%s>" % auth_url)

        return (str(request_token), auth_url)

    def gain_access_token(self, request_token):
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
        # "oauth_token_secret=GP4xmW9dQzBKBWcm0dYJxiIU&oauth_token=4%2FgvYvD2N8q4N8iJRQBLF5qRVDLHEN"
        #
        self.log.debug(
            "Upgrade to access token for request_token <%s>." % request_token
        )

        # Set the request_token before attempting to upgrade:
        self.set_token(request_token)

        self.services.UpgradeToOAuthAccessToken()
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


import gdata.contacts.client


class Contacts(object):
    """A light wrapper around google's Contact service.
    """
    def __init__(self, consumer_key, consumer_secret, access_token):
        """
        :param access_token:  The authorised OAuth access token.
        """
        self.log = get_log("Contacts")

        self.log.debug('Set OAuth input parameters for contact service.')
        self.client = gdata.contacts.client.ContactsClient()
        self.client.SetOAuthInputParameters(
            gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
            consumer_key,
            consumer_secret=consumer_secret,
        )

        token = gdata.auth.OAuthToken(
            oauth_input_params=self.client.GetOAuthInputParameters()
        )
        token.set_token_string(access_token)

        self.client.SetOAuthToken(token)

    def all(self):
        """Retrieves the 'all contacts' feed."""
        return self.client.GetContacts()

    def print_contacts_feed(self, feed):
        # copied and hacked from google contacts example:
        if not feed.entry:
            print '\nNo contacts in feed.\n'
            return 0

        for i, entry in enumerate(feed.entry):
            print "Contact:"
            if not entry.name is None:
                family_name = entry.name.family_name is None and " " or entry.name.family_name.text
                print family_name
                full_name = entry.name.full_name is None and " " or entry.name.full_name.text
                print full_name
                given_name = entry.name.given_name is None and " " or entry.name.given_name.text
                print given_name

            if entry.content:
                print '        %s' % (entry.content.text)

            for p in entry.structured_postal_address:
                print '        %s' % (p.formatted_address.text)

            # Display the group id which can be used to query the contacts feed.
            print '        Group ID: %s' % entry.id.text

            # Display extended properties.
            for extended_property in entry.extended_property:
                if extended_property.value:
                    value = extended_property.value
                else:
                    value = extended_property.GetXmlBlob()
                print '        Extended Property %s: %s' % (extended_property.name, value)

            for user_defined_field in entry.user_defined_field:
                print '        User Defined Field %s: %s' % (user_defined_field.key, user_defined_field.value)
