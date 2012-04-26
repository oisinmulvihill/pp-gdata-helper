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

    # upgrade to access token opts:
    parser.add_option('-l', '--list_contacts', action='store_true',
        dest='list_contacts',
        help='List all contacts using the access_token',
    )

    options, args = parser.parse_args()

    CONSUMER_KEY = "604493538420.apps.googleusercontent.com"
    CONSUMER_SECRET = "n8Efb8PUtnBWZGL2YMLileOY"

    SCOPES = [
        # contacts:
        "https://www.google.com/m8/feeds/",
        # calendar:
        "https://www.google.com/calendar/feeds/",
    ]

    log.info("Scopes: %s " % ",".join(SCOPES))

    from pp.gdata.helper import access

    # Gain access to calendar and contacts
    #
    if options.gen_auth:
        # Request Access to services:
        #
        oasa = access.OAuthServiceAccess(
            SCOPES,
            CONSUMER_KEY,
            CONSUMER_SECRET,
        )

        request_token, url = oasa.generate_auth_url()

        print """
Authorisation Request Generated.

URL:
%s

Request Token:
%s
        """ % (url, request_token)

    # Upgrade to an access_token after authorising the consumer's access:
    elif options.exchange_token:
        # Sometime later, before google expires the request (<30min), recover the
        # request token and upgrade to an access token. The end user will have gone
        # to the authorisation URL and granted the requested permissions. If not
        # the gain_access_token will fail
        #
        request_token = options.token

        oasa2 = access.OAuthServiceAccess(
            SCOPES,
            CONSUMER_KEY,
            CONSUMER_SECRET,
        )

        access_token = oasa2.gain_access_token(request_token)

        print """
Exchange Request for Access token Successful.

Access Token:
%s
        """ % (access_token)

    elif options.list_contacts:
        access_token = options.token

        contacts = access.Contacts(
            CONSUMER_KEY,
            CONSUMER_SECRET,
            access_token
        )

        contacts.print_contacts_feed(contacts.all())

    return

    # while True:
    #     try:
    #         app = DemoCmds()
    #         sys.exit(app.main())

    #     except KeyboardInterrupt:
    #         log.info("Exit time.")
    #         break


if __name__ == '__main__':
    main()



# http://www.bubblefoundry.com/blog/2009/05/openid-and-oauth-on-app-engine/
# http://www.bubblefoundry.com/blog/2009/05/oauth-on-app-engine-part-2/
# http://drdobbs.com/web-development/231600390
#

# hybrid auth openid+oauth
#
# signed_request_token = gdata.auth.OAuthToken(key=args['openid.ext2.request_token'], secret="")
# gdata_service = gdata.service.GDataService()
# gdata_service.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, settings.GOOGLE_CONSUMER_KEY, settings.GOOGLE_CONSUMER_SECRET)
# access_token = gdata_service.UpgradeToOAuthAccessToken(signed_request_token)
# person.accessToken = str(access_token)

# from gdata.contacts.service import ContactsService
# client = ContactsService()
# client.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
# # the token key and secret should be recalled from your database
# tk_str = 'oauth_token_secret=JW-BQWzfmOnVWh0HXD5iLdTV&oauth_token=1%2F7sTMpTmhWfdc6vy6S4iItv4eeAXALcomOwroVHrM5rI'
# tk = gdata.auth.OAuthToken(oauth_input_params=client.GetOAuthInputParameters())
# tk.set_token_string(tk_str)
# client.SetOAuthToken(tk)
# feed = client.GetContactsFeed()
# for entry in feed.entry:
#     print entry.title.text
