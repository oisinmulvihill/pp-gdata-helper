# -*- coding: utf-8 -*-
"""
"""
import logging

import gdata.calendar.client


def get_log(extra=None):
    m = "pp.gdata.helper.calendar"
    if extra:
        m = "%s.%s" % (m, extra)
    return logging.getLogger(m)


class Calendar(object):
    """A light wrapper around google's Calendar service.
    """
    def __init__(self, consumer_key, consumer_secret, access_token):
        """
        :param access_token: The authorised access token string to use.

        The access_token must be valid and not the request_token.

        """
        self.log = get_log("Calendar")

        # Convert the access_token string into one I can used with the
        # contacts client.
        tk = gdata.auth.OAuthToken()
        tk.set_token_string(access_token)

        access_token = gdata.gauth.OAuthHmacToken(
            consumer_key,
            consumer_secret,
            tk.key,
            tk.secret,
            gdata.gauth.ACCESS_TOKEN
        )

        self.client = gdata.calendar.client.CalendarClient(
            auth_token=access_token
        )

    def print_own_calendars(self):
        """Retrieves the list of calendars to which the authenticated user
        owns --
        Although we are only printing the title of the
        calendar in this case, other information, including the color of the
        calendar, the timezone, and more.
        .
        """
        feed = self.client.GetOwnCalendarsFeed()
        print 'Printing owncalendars: %s' % feed.title.text
        for i, a_calendar in zip(xrange(len(feed.entry)), feed.entry):
            print '\t%s. %s' % (i, a_calendar.title.text,)
