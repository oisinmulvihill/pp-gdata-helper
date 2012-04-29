# -*- coding: utf-8 -*-
"""
"""
import os
import sys
import logging
import ConfigParser
import logging.config

import cmdln

from . import access


class OAuthAdminCmds(cmdln.Cmdln):
    """Usage:
        oauth-admin -c / --config <settings.ini> SUBCOMMAND [ARGS...]
        oauth-admin help SUBCOMMAND

    ${command_list}
    ${help_list}

    """
    # The 'name' also the section name to use inside the
    # config i.e. [oauthadmin]
    name = "oauthadmin"

    # *MUST* be https to get a private data!
    SCOPES = [
        # contacts:
        "https://www.google.com/m8/feeds/",
        # calendar:
        "https://www.google.com/calendar/feeds/",
    ]

    def __init__(self, *args, **kwargs):
        cmdln.Cmdln.__init__(self, *args, **kwargs)
        self.log = logging.getLogger("pp.gdata.helper.oauthadmin.OAuthAdminCmds")
        # Set up by postoptparse()
        self.oasa = None

    def get_optparser(self):
        """Parser for global options (that are not specific to a subcommand).
        """
        optparser = cmdln.CmdlnOptionParser(self)

        optparser.add_option('-c', '--config', action='store',
            dest="config_filename",
            default="config.ini",
            help='The global config file %default'
        )

        return optparser

    def log_to_console(self, log):
        """Set up the root logger to log all output to."""
        hdlr = logging.StreamHandler()
        fmt = '%(asctime)s %(name)s %(levelname)s %(message)s'
        formatter = logging.Formatter(fmt)
        hdlr.setFormatter(formatter)
        log.addHandler(hdlr)
        log.setLevel(logging.DEBUG)
        log.propagate = False

    def postoptparse(self):
        """Set up logging form the config file after options have been parsed.
        """
        # Set up the root logger:
        log = logging.getLogger()
        cfg_file = self.options.config_filename

        if not os.path.isfile(cfg_file):
            sys.stderr.write((
                "The config file '%s' was not found! "
                "Please specify with -c/--config." % cfg_file
            ))
            # don't exit to allow help to be printed.
            #sys.exit(1)

        else:
            try:
                logging.config.fileConfig(cfg_file)
            except ConfigParser.NoSectionError:
                self.log_to_console(log)
                log.warn("No logging in configuration. Using console.")

            config = ConfigParser.ConfigParser()
            self.log.debug("recovering config from <%s>" % cfg_file)
            config.read(cfg_file)
            cfg = dict(config.items(self.name))

            def strip(i):
                """Strip \" and \' around config strings."""
                return i.replace('"', '').replace("'", "")

            self.config = dict(
                consumer_key=strip(cfg['consumer_key']),
                consumer_secret=strip(cfg['consumer_secret']),
            )

            self.oasa = access.OAuthServiceAccess(
                self.SCOPES,
                self.config['consumer_key'],
                self.config['consumer_secret'],
            )

    def do_request_access(self, subcmd, opts):
        """${cmd_name}: Generate the request_token and auth URI.

        ${cmd_usage}
        ${cmd_option_list}

        """
        request_token, url = self.oasa.generate_auth_url()

        print """
Authorisation Request Generated.

Scopes:
%s

Request Token:
\"%s\"

Authorisation URL (Go Here to grant access within 30 minutes):
%s
        """ % (self.SCOPES, request_token, url)

    def do_gain_access_token(self, subcmd, opts, request_token):
        """${cmd_name}: Exchange a request token for an access_token.

        The google user must have gone to the Authorisation URL and granted
        access for this to work. If not the exchange will fail.

        ${cmd_usage}
        ${cmd_option_list}

        """
        access_token = self.oasa.gain_access_token(request_token)

        print """
The Request Token has been exchanged for Access Token OK.

Access Token:
\"%s\"

        """ % (access_token)

    def do_list_contacts(self, subcmd, opts, access_token):
        """${cmd_name}: List the google users contacts.

        The given access_token must be authorised to access the google user's
        contact data. If not access will be denied.

        ${cmd_usage}
        ${cmd_option_list}

        """
        from .contacts import Contacts

        contacts = Contacts(
            self.config['consumer_key'],
            self.config['consumer_secret'],
            access_token,
        )

        print "\n".join(contacts.all_to_vcards())

    def do_list_calendars(self, subcmd, opts, access_token):
        """${cmd_name}: List the google user's personal.

        The given access_token must be authorised to access the google user's
        contact data. If not access will be denied.

        ${cmd_usage}
        ${cmd_option_list}

        """
        from .calendar import Calendar

        cal = Calendar(
            self.config['consumer_key'],
            self.config['consumer_secret'],
            access_token,
        )

        print "\n".join(cal.all_to_vcal())
