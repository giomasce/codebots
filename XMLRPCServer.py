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
from threading import Thread

class XMLRPCServer(Thread):
    def __init__(self, manager):
        Thread.__init__(self)
        self.daemon = True
        self.manager = manager
        self.rpcserver = SimpleXMLRPCServer(("localhost", 8080),
                                            allow_none = True)
        self.rpcserver.register_introspection_functions()
        self.rpcserver.register_function(self.manager.add_request)
        self.rpcserver.register_function(self.manager.get_info)
        self.rpcserver.register_function(self.manager.wait_for_simulation)

    def run(self):
        self.rpcserver.serve_forever()

if __name__ == "__main__":
    manager = Manager()
    s = XMLRPCServer()
