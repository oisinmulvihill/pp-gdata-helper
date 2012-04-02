import os
import codecs
import logging
import ConfigParser

import cmdln

from . import access


class DemoCmds(cmdln.Cmdln):
    """Usage:
        smsdemo -c / --config <settings.ini> SUBCOMMAND [ARGS...]
        smsdemo help SUBCOMMAND

    ${command_list}
    ${help_list}

    """
    name = "smsdemo"

    def __init__(self, *args, **kwargs):
        cmdln.Cmdln.__init__(self, *args, **kwargs)
        self.log = logging.getLogger("pp.gdata.helper.demoadmin.DemoCmds")


        self.access = access.OAuthServiceAccess

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

    def postoptparse(self):
        """runs after parsing global options"""

    @property
    def config(self):
        """Return a config instance when called.

        Implement file change and reloading here?

        """
        cfg_filename = self.options.config_filename
        config = ConfigParser.ConfigParser()
        self.log.debug("config: recovering config from <%s>" % cfg_filename)
        config.read(cfg_filename)
        return dict(config.items(self.name))

    def do_load(self, subcmd, opts, org_id, resource_file):
        """${cmd_name}: load an organisation from the given resource file

        ${cmd_usage}
        ${cmd_option_list}

        """
        cfg = self.config

        self.log.debug("load: resource file <%s>" % resource_file)
        resource_file = resource_file.strip()
        if not os.path.isfile(resource_file):
            self.log.error("load: could not find the resource file <%s>" % resource_file)
            return

        self.log.debug("load: organisation id <%s>" % org_id)
        org_id = org_id.strip()

        #self.log.debug("load: cfg <%s>" % cfg)

        # Test the frontend is running and then read and load the data:
        uri = cfg['bookingsys_uri']
        org = restclient.resource.init(uri)
        org = restclient.resource.Organisation()

        if not org.is_running():
            self.log.error("load: the server <%s> is not running!" % uri)
            return

        with codecs.open(resource_file, 'r', encoding='utf-8') as fd:
            json_data = fd.read()
            org.load(org_id, json_data)
