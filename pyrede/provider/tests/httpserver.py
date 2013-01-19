# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Basic httpserver usefull for testing

"""
import SimpleHTTPServer
import SocketServer
import threading


class PyPiHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    Basic handler, serve a basic JSON answer
    """
    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write('''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN" 
"http://my.netscape.com/publish/formats/rss-0.91.dtd">
<rss version="0.91">
 <channel>
  <title>PyPI recent updates</title>
  <link>http://pypi.python.org/pypi</link>
  <description>Updates to the Python Package Index</description>
  <language>en</language>

  <item>
    <title>django-webtest 1.5.5</title>
    <link>http://pypi.python.org/pypi/django-webtest/1.5.5</link>
    <description>Instant integration of Ian Bicking's WebTest
(http://webtest.pythonpaste.org/).</description>
    <pubDate>14 Jan 2013 11:49:57 GMT</pubDate>
   </item>

  <item>
    <title>python-dikbm-adapter 0.1.5</title>
    <link>http://pypi.python.org/pypi/python-dikbm-adapter/0.1.5</link>
    <description>DiKBM adapter to send request to RSA web service</description>
    <pubDate>14 Jan 2013 11:48:47 GMT</pubDate>
   </item>

 </channel>
</rss>''')


class TestServer(threading.Thread):
    """
    Basic http server to serve datas one shot
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.port = 1024
        connected = False
        while not connected and self.port < 2048:
            try:
                self.httpd = SocketServer.TCPServer(("", self.port),
                                                    PyPiHandler)
                self.httpd.timeout = 30
                connected = True
            except:
                self.port = self.port + 1

    def run(self):
        print "serving at port", self.port
        self.httpd.handle_request()
