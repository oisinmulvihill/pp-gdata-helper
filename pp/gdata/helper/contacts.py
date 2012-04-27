# -*- coding: utf-8 -*-
"""
"""
import logging

import gdata.contacts.client


def get_log(extra=None):
    m = "pp.gdata.helper.contacts"
    if extra:
        m = "%s.%s" % (m, extra)
    return logging.getLogger(m)


class Contacts(object):
    """A light wrapper around google's Contact service.
    """
    def __init__(self, consumer_key, consumer_secret, access_token):
        """
        :param access_token: The authorised access token string to use.

        The access_token must be valid and not the request_token.

        """
        self.log = get_log("Contacts")

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

        self.client = gdata.contacts.client.ContactsClient(
            auth_token=access_token
        )

    def all(self):
        """Retrieves the 'all contacts' feed."""
        return self.client.get_contacts()

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
