# -*- coding: utf-8 -*-
"""
"""
import logging
import datetime

import vobject
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

    def all(self):
        """Retrieves all the calendars."""
        return self.client.GetOwnCalendarsFeed()

    def vcalendar_for_calendars(self, cal_title, cal_event):
        """Convert and google calendars into a vCalendar string.

        :returns: This returns a single string containing the vcalendar.

        """
        cal = vobject.iCalendar()

        cal.add('vevent')

        event_title = cal_event.title.text
        cal.vevent.add('summary').value = event_title

#        import pdb ; pdb.set_trace()

        #utc = vobject.icalendar.utc
        #start = cal.vevent.add('dtstart')
        #start.value = datetime.datetime(2006, 2, 16, tzinfo = utc)

        # print '\t%s. %s' % (i, an_event.title.text,)
        # for p, a_participant in zip(xrange(len(an_event.who)), an_event.who):
        #     print '\t\t%s. %s' % (p, a_participant.email,)
        #     print '\t\t\t%s' % (a_participant.value,)
        #     if a_participant.attendee_status:
        #         print '\t\t\t%s' % (a_participant.attendee_status.value,)
        try:
            cal = cal.serialize()
            self.log.info("cal: %s" % cal)

        except UnicodeDecodeError, e:
            self.log.error("Unable to serialise due to unicode error <%s>" % e)
            cal = None

        return cal

    def all_to_vcal(self):
        """Convert all calendars into vcalendars and return this.
        """
        returned = []

        feed = self.client.GetCalendarEventFeed()
        cal_title = feed.title.text

        self.log.info('Events on Primary Calendar: <%s>' % cal_title)

        for i, cal_event in zip(xrange(len(feed.entry)), feed.entry):
            cal = self.vcalendar_for_calendars(cal_title, cal_event)
            if cal:
                returned.append(cal)

        return returned

    def print_own_calendars(self):
        """Retrieves the list of calendars to which the authenticated user
        owns --
        Although we are only printing the title of the
        calendar in this case, other information, including the color of the
        calendar, the timezone, and more.
        .
        """
        feed = self.all()

        print 'Printing owncalendars: %s' % feed.title.text
        for i, a_calendar in zip(xrange(len(feed.entry)), feed.entry):
            print '\t%s. %s' % (i, a_calendar.title.text,)
