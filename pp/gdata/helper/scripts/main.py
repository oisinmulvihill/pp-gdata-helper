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

    print '\nSTEP 1: Set OAuth input parameters.'
    gdata_service.SetOAuthInputParameters(
            gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
            CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET
    )

    print '\nSTEP 2: Fetch OAuth Request token.'
    request_token = gdata_service.FetchOAuthRequestToken(scopes)

    print 'Request Token fetched: %s' % request_token
    print '\nSTEP 3: Set the fetched OAuth token.'
    gdata_service.SetOAuthToken(request_token)

    print 'OAuth request token set.'
    print '\nSTEP 4: Generate OAuth authorization URL.'
    auth_url = gdata_service.GenerateOAuthAuthorizationURL()

    print 'Authorization URL: %s' % auth_url
    raw_input('Manually go to the above URL and authenticate.'
              'Press a key after authorization.')

    print '\nSTEP 5: Upgrade to an OAuth access token.'

    gdata_service2 = gdata.service.GDataService()

    gdata_service2.SetOAuthInputParameters(
            gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
            CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET
    )

#    request_token = "oauth_token_secret=GGec6wTANGyXs0tPMhLkFmje&oauth_token=4%2FEMtxEHuTR-m1ia7Hk_iozF08LYxX"

    from gdata.oauth import OAuthToken

    print "1. request_token: ", request_token.__dict__, type(request_token)

    request_token2 = OAuthToken.from_string(str(request_token))
    request_token2.scopes = scopes
    request_token2.oauth_input_params = gdata_service2.GetOAuthInputParameters()

    print "2. request_token2: ", request_token2.__dict__, type(request_token2)

    gdata_service2.current_token = request_token2
    gdata_service2.SetOAuthToken(request_token2)

    gdata_service2.UpgradeToOAuthAccessToken()

    print 'Access Token: %s == %s' % (
        gdata_service.token_store.find_token(request_token.scopes[0]),
        gdata_service.current_token
    )

    import pdb ; pdb.set_trace()

    return

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

#        import gdata
        from gdata.oauth import OAuthToken

        rt = OAuthToken(key=request_token_str, secret=CONSUMER_SECRET)
        rt.oauth_input_params = gdata_service.GetOAuthInputParameters()

        # rt = OAuthToken(CONSUMER_KEY, CONSUMER_SECRET)
        # rt.oauth_input_params = gdata_service.GetOAuthInputParameters()
        # rt.from_string(request_token_str)
        # gdata_service.SetOAuthToken(rt)
        # gdata_service.token_store.add_token(rt)
        # print "oauth token?> ", gdata_service.current_token
        # print ">>", isinstance(gdata_service.current_token, OAuthToken)

        #gdata_service.UpgradeToOAuthAccessToken(authorized_request_token=rt)
        #gdata_service.UpgradeToOAuthAccessToken()

        access_token = gdata_service.UpgradeToOAuthAccessToken()
        if access_token:
            gdata_service.current_token = access_token
            gdata_service.SetOAuthToken(access_token)

#        access_token = gdata_service.token_store.find_token(request_token.scopes[0])

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
