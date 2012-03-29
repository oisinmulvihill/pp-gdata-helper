# -*- coding: utf-8 -*-
#
# Based on the OAuthSample in the gdata-x.y.z/samples/oauth/oauth_example.py
#
import logging
from optparse import OptionParser

import gdata.auth
import gdata.docs.service


def get_log(extra=None):
    m = "pp.gdata.helper.access"
    if extra:
        m = "%s.%s" % (m, extra)
    return logging.getLogger(m)


class OAuthCalendarContactAccess(object):
    """Uses OAuth to gain access to calendar and contact data.

    Based on the sample class demonstrating the three-legged OAuth process.

    """
    log = get_log("OAuthCalendarContactAccess")

    def __init__(self, google_service, consumer_key, consumer_secret):
        """
        :param google_service: ContactsService(), CalendarClient(), etc...

        :param consumer_key: string Domain identifying third_party web application.

        :param consumer_secret: string Secret generated during registration.

        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.gd_client = google_service

    def dump_feed(self, feed):
        """Prints out the contents of a feed to the console.

        Args:
            feed: A gdata.docs.DocumentListFeed instance.
        """
        if not feed.entry:
            self.log.debug('No entries in feed.')

        docs_list = list(enumerate(feed.entry, start=1))
        for i, entry in docs_list:
            self.log.debug('%d. %s\n' % (i, entry.title.text.encode('UTF-8')))

    def generate_auth_url(self):
        """Uses OAuth to get a request token and then returns a URL.

        The URL should be used to allow access

        """
        self.log.debug('STEP 1: Set OAuth input parameters.')
        self.gd_client.SetOAuthInputParameters(
                gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
                self.consumer_key,
                consumer_secret=self.consumer_secret
        )

        self.log.debug('STEP 2: Fetch OAuth Request token.')
        request_token = self.gd_client.FetchOAuthRequestToken()
        self.log.debug('Request Token fetched: %s' % request_token)

        self.log.debug('STEP 3: Set the fetched OAuth token.')
        self.gd_client.SetOAuthToken(request_token)

        self.log.debug('STEP 4: Generate OAuth authorization URL.')
        auth_url = self.gd_client.GenerateOAuthAuthorizationURL()

        self.log.info("URL <%s>" % auth_url)

        return auth_url

    def gain_access_token(self, request_token):
        """Called at some point after the Customer has given permission for out
        access.

        We now need to exchange the request_token for an access_token. Once we
        have the access_token, we should be able to access contact and calendar
        data. The access_token can be stored and used with all future calls.

        The Customer, who's account we are accessing, can deny access. This
        will mean the access_token will be invalidated.

        :returns: The access token which now replaces the request_token.

        """
        self.log.debug("STEP 5: Upgrade to an OAuth access token using request_token <%s>." % request_token)
        self.gd_client.SetOAuthToken()
        self.gd_client.UpgradeToOAuthAccessToken()
        access_token = self.gd_client.token_store.find_token(request_token.scopes[0])
        self.log.info('Success, the access_token is <%s>' % access_token)

        return access_token


def main():
    """Demonstrates usage of OAuth authentication mode.

    Prints a list of documents. This demo uses HMAC-SHA1 signature method.
    """

    # sample = OAuthSample(consumer_key, consumer_secret)
    # sample.Run()

    # contacts = gdata.contacts.service.ContactsService()
    # calendar = gdata.calendar.client.CalendarClient()

    #    print '\nYour Documents:\n'
    #     self._ListAllDocuments()
    #     print 'STEP 6: Revoke the OAuth access token after use.'
    #     self.gd_client.RevokeOAuthToken()
    #     print 'OAuth access token revoked.'

    # def _ListAllDocuments(self):
    #     """Retrieves a list of all of a user's documents and displays them."""
    #     feed = self.gd_client.GetDocumentListFeed()
    #     self._PrintFeed(feed)


if __name__ == '__main__':
    main()
