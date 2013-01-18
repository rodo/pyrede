#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2007-2008  Stefano Zacchiroli <zack@debian.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import sys

default_url = 'http://packages.qa.debian.org/cgi-bin/soap-alpha.cgi'

def zsi_query(soap_url, method, **kwargs):
    from ZSI.client import NamedParamBinding as NPBinding

    ws = NPBinding(url=soap_url)# tracefile=sys.stdout)
    return getattr(ws, method)(**kwargs)

def soappy_query(soap_url, method, **kwargs):
    import SOAPpy

    ws = SOAPpy.SOAPProxy(url)
#     ws.config.dumpSOAPOut = True
#     ws.config.dumpSOAPIn = True
    return getattr(ws, method)(**kwargs)

if __name__ == '__main__':
    url = default_url
    try:
        if sys.argv[1] in ['-u', '--url']:
            url = sys.argv[2]
            del(sys.argv[:2])
        method = sys.argv[1]
        args = dict(map(lambda s:s.split('='), sys.argv[2:]))
    except IndexError:
        print "Usage:  soap_query.py [(-u|--url) URL] METHOD [PARAM_NAME=PARAM_VALUE ...]"
        print "  URL: URL of the target CGI queries should be submitted to"
        print "       Default:", default_url
        print "  METHOD: method to be invoked"
        print "  PARAMS: keyword argument / argument value pairs; =-separated"
        print "E.g.: ./soap_query.py latest_version source=ocaml"
        sys.exit(1)

#     print zsi_query(url, method, **args)
    print soappy_query(url, method, **args)

