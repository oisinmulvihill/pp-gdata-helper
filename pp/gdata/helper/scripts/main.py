# -*- coding: utf-8 -*-
"""
"""
import sys
import logging
from optparse import OptionParser

from ..demoadmin import DemoCmds


def main():
    """smsdemo main script as set up in the 'setup.py'."""
    log = logging.getLogger()
    hdlr = logging.StreamHandler()
    f = '%(asctime)s %(name)s %(levelname)s %(message)s'
    formatter = logging.Formatter(f)
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG)
    log.propagate = False

    parser = OptionParser()
    #     description=description,
    #     usage='Usage: %prog CONFIG_PATH',
    # )

    parser.add_option('-t', '--token', action='store',
        dest='token',
        help='The request or access token depending on context.',
    )

    # Request access opts:
    parser.add_option('-g', '--gen-auth', action='store_true', dest='gen_auth',
        help='gen_auth url asking for access to service',
    )

    # upgrade to access token opts:
    parser.add_option('-e', '--exchange-token', action='store_true',
        dest='exchange_token',
        help='Exchange the request_token for an access_token',
    )

    options, args = parser.parse_args()

    # sample = OAuthSample(consumer_key, consumer_secret)
    # sample.Run()

    # contacts = gdata.contacts.service.ContactsService()
    # calendar = gdata.calendar.client.CalendarClient()

    # def dump_feed(self, feed):
    #     """Prints out the contents of a feed to the console.

    #     Args:
    #         feed: A gdata.docs.<Something>ListFeed instance.
    #     """
    #     if not feed.entry:
    #         self.log.debug('No entries in feed.')

    #     docs_list = list(enumerate(feed.entry, start=1))
    #     for i, entry in docs_list:
    #         self.log.debug('%d. %s\n' % (i, entry.title.text.encode('UTF-8')))

    #    print '\nYour Documents:\n'
    #     self._ListAllDocuments()
    #     print 'STEP 6: Revoke the OAuth access token after use.'
    #     self.gd_client.RevokeOAuthToken()
    #     print 'OAuth access token revoked.'

    # def _ListAllDocuments(self):
    #     """Retrieves a list of all of a user's documents and displays them."""
    #     feed = self.gd_client.GetDocumentListFeed()
    #     self._PrintFeed(feed)

    import gdata
    import gdata.auth
    import gdata.docs.service

    # http://www.bubblefoundry.com/blog/2009/05/openid-and-oauth-on-app-engine/
    # http://www.bubblefoundry.com/blog/2009/05/oauth-on-app-engine-part-2/
    # http://drdobbs.com/web-development/231600390
    #

    CONSUMER_KEY = "604493538420.apps.googleusercontent.com"
    CONSUMER_SECRET = "n8Efb8PUtnBWZGL2YMLileOY"

    scopes = [
        # contacts:
        "https://www.google.com/m8/feeds/",
        # calendar:
        "https://www.google.com/calendar/feeds/",
    ]

    log.info("Scopes: %s " % ",".join(scopes))

    # hybrid auth openid+oauth
    #
    # signed_request_token = gdata.auth.OAuthToken(key=args['openid.ext2.request_token'], secret="")
    # gdata_service = gdata.service.GDataService()
    # gdata_service.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, settings.GOOGLE_CONSUMER_KEY, settings.GOOGLE_CONSUMER_SECRET)
    # access_token = gdata_service.UpgradeToOAuthAccessToken(signed_request_token)
    # person.accessToken = str(access_token)

    gdata_service = gdata.service.GDataService()

    gdata_service.SetOAuthInputParameters(
            gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
            CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET
    )

    # Gain access to calendar and contacts
    #
    if options.gen_auth:
        log.debug('STEP 2: Fetch OAuth Request token.')
        request_token = gdata_service.FetchOAuthRequestToken(scopes=scopes)
        log.debug('Request Token fetched: %s' % str(request_token))
        print "dir(request_token): ", dir(request_token)
        print "request_token: <%s>" % str(request_token)

        log.debug('STEP 3: Set the fetched OAuth token.')
        gdata_service.SetOAuthToken(request_token)

        log.debug('STEP 4: Generate OAuth authorization URL.')
        auth_url = gdata_service.GenerateOAuthAuthorizationURL()
        print "auth_url: ", auth_url

    # Upgrade to an access_token after authorising the consumer's access:
    #
    elif options.exchange_token:
        request_token_str = options.token
        if not request_token_str:
            log.error("Please specify the request token to use!")
            sys.exit(1)

        log.debug("STEP 5: Upgrade to an OAuth access token using request_token <%s>." % request_token_str)

        from gdata.oauth import OAuthToken

        token = OAuthToken(CONSUMER_KEY, CONSUMER_SECRET)
        token.from_string(request_token_str)
        # rt.set_token_string(request_token_str)
        gdata_service.SetOAuthToken(token)
        gdata_service.UpgradeToOAuthAccessToken()
        access_token = gdata_service.token_store.find_token(request_token.scopes[0])
        log.info('Success, the access_token is <%s>' % str(access_token))


    # oauth_input_params = gdata.auth.OAuthInputParams(
    #     gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
    #     CONSUMER_KEY,
    #     CONSUMER_SECRET
    # )

    # access_token = gdata.auth.OAuthToken(
    #     scopes=scopes, oauth_input_params=oauth_input_params
    # )
    # access_token.set_token_string(person.accessToken)
    # gdata_service.current_token = access_token

    # request feed
    #feed = data_service.GetFeed(settings.GOOGLE_ANALYTICS_ACCOUNT_URI)

    #feed is a GDataFeed object which can easily be iterated over, like so:

    # for entry in feed.entry:
    #     print entry.title.text

    return

    while True:
        try:
            app = DemoCmds()
            sys.exit(app.main())

        except KeyboardInterrupt:
            log.info("Exit time.")
            break


if __name__ == '__main__':
    main()
