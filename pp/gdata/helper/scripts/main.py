# -*- coding: utf-8 -*-
"""
"""
import sys

from ..oauthadmin import OAuthAdminCmds


def main():
    """main script of oauth-admin as set up in the 'setup.py'.
    """
    app = OAuthAdminCmds()
    sys.exit(app.main())


if __name__ == '__main__':
    main()
