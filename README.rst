pp-gdata-helper
===================================

.. contents::


Introduction
------------

This provides the namespaced package: pp.gdata.helper


Testing
-------

Activate the dev environment and change into pp-gdata-helper.

Run all tests
~~~~~~~~~~~~~

From here you can do::

    python runtests.py -s



OAuth and oauth-admin
---------------------


oauth-admin usage
~~~~~~~~~~~~~~~~~

from shell::

    # activate env and run oauth-admin to see commands
    #
    workon sms-demo

    oauth-admin -c pp-gdata-helper/config.ini

    root WARNING No logging in configuration. Using console.
    pp.gdata.helper.oauthadmin.OAuthAdminCmds DEBUG recovering config from <pp-gdata-helper/config.ini>
    pp.gdata.helper.access.OAuthServiceAccess DEBUG Set OAuth input parameters.
    Usage:
        oauth-admin -c / --config <settings.ini> SUBCOMMAND [ARGS...]
        oauth-admin help SUBCOMMAND

    Commands:
        gain_access_token
                          Exchange a request token for an access_token.
        help (?)          give detailed help on a specific sub-command
        list_calendars    List the google user's personal.
        list_contacts     List the google users contacts.
        request_access    Generate the request_token and auth URI.


get a request_token and auth URL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is done once.

from shell::

    $oauth-admin -c pp-gdata-helper/config.ini request_access
    root WARNING No logging in configuration. Using console.
    pp.gdata.helper.oauthadmin.OAuthAdminCmds DEBUG recovering config from <pp-gdata-helper/config.ini>
    pp.gdata.helper.access.OAuthServiceAccess DEBUG Set OAuth input parameters.
    pp.gdata.helper.access.OAuthServiceAccess DEBUG Fetch OAuth Request token.
    pp.gdata.helper.access.OAuthServiceAccess DEBUG Set the fetched OAuth token.
    pp.gdata.helper.access.OAuthServiceAccess DEBUG Generate OAuth authorization URL.
    pp.gdata.helper.access.OAuthServiceAccess INFO URL <https://www.google.com/accounts/OAuthAuthorizeToken?oauth_token=4%2F1CAaRZScps4uSb1nnuvafw5fJP7A>

    Authorisation Request Generated.

    Scopes:
    ['https://www.google.com/m8/feeds/', 'https://www.google.com/calendar/feeds/']

    Request Token:
    "oauth_token_secret=Sl-crNL7ZcvibK0JGZ1kEZNN&oauth_token=4%2F1CAaRZScps4uSb1nnuvafw5fJP7A"

    Authorisation URL (Go Here to grant access within 30 minutes):
    https://www.google.com/accounts/OAuthAuthorizeToken?oauth_token=4%2F1CAaRZScps4uSb1nnuvafw5fJP7A

    $

Now open the Authorisation URL to grant access.


Exchange request_token for access_token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the request_token has been authorised we can exchange it for an
access_token. This token can be used from now until its revoked. The token used
is the string used in other commands.

from shell::

    $oauth-admin -c pp-gdata-helper/config.ini gain_access_token "oauth_token_secret=Sl-crNL7ZcvibK0JGZ1kEZNN&oauth_token=4%2F1CAaRZScps4uSb1nnuvafw5fJP7A"
    root WARNING No logging in configuration. Using console.
    pp.gdata.helper.oauthadmin.OAuthAdminCmds DEBUG recovering config from <pp-gdata-helper/config.ini>
    pp.gdata.helper.access.OAuthServiceAccess DEBUG Set OAuth input parameters.
    pp.gdata.helper.access.OAuthServiceAccess DEBUG Upgrade to access token for request_token <oauth_token_secret=Sl-crNL7ZcvibK0JGZ1kEZNN&oauth_token=4%2F1CAaRZScps4uSb1nnuvafw5fJP7A>.
    2012-04-27 17:29:53,902 pp.gdata.helper.access.OAuthServiceAccess DEBUG Success, the access_token is <oauth_token_secret=vwl7-4r-fd3ftk7RynVXv_iv&oauth_token=1%2Fbb_mZFmJYgQokFFazkcC9FIqOQ_zJaqHNPFz0tuJYy0>

    The Request Token has been exchanged for Access Token OK.

    Access Token:
    "oauth_token_secret=vwl7-4r-fd3ftk7RynVXv_iv&oauth_token=1%2Fbb_mZFmJYgQokFFazkcC9FIqOQ_zJaqHNPFz0tuJYy0"

    $


List contacts or list calendars
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This now uses the access token string which has been authorised.

list contacts::

    $oauth-admin -c pp-gdata-helper/config.ini list_contacts "oauth_token_secret=vwl7-4r-fd3ftk7RynVXv_iv&oauth_token=1%2Fbb_mZFmJYgQokFFazkcC9FIqOQ_zJaqHNPFz0tuJYy0"
    root WARNING No logging in configuration. Using console.
    pp.gdata.helper.oauthadmin.OAuthAdminCmds DEBUG recovering config from <pp-gdata-helper/config.ini>
    pp.gdata.helper.access.OAuthServiceAccess DEBUG Set OAuth input parameters.
    Contact:
    :
    dump to console of contact data
    :
    $


list calendars::

    $oauth-admin -c pp-gdata-helper/config.ini list_calendars "oauth_token_secret=vwl7-4r-fd3ftk7RynVXv_iv&oauth_token=1%2Fbb_mZFmJYgQokFFazkcC9FIqOQ_zJaqHNPFz0tuJYy0"
    root WARNING No logging in configuration. Using console.
    pp.gdata.helper.oauthadmin.OAuthAdminCmds DEBUG recovering config from <pp-gdata-helper/config.ini>
    pp.gdata.helper.access.OAuthServiceAccess DEBUG Set OAuth input parameters.
    Printing owncalendars: oisin.mulvihill@gmail.com's Calendar List
        0. Oisin Mulvihill
        1. FS-Events
        2. oisin-events

    $

Success.