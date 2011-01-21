#!/usr/bin/python
# -*- coding: utf-8 -*-

# CodeBots
# Copyright (C) 2011 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SessionServer import SessionServer

class XMLRPCServer(SessionServer):

    def __init__(self, manager, host = "localhost", port = 8080):
        SessionServer.__init__(self, manager)
        self.rpcserver = SimpleXMLRPCServer((host, port), allow_none = True)
        self.rpcserver.register_introspection_functions()
        self.rpcserver.register_function(self.add_request)
        self.rpcserver.register_function(self.get_info)
        self.rpcserver.register_function(self.wait_for_simulation)
        self.rpcserver.register_function(self.login)
        self.rpcserver.register_function(self.logout)

    def run(self):
        self.rpcserver.serve_forever()
