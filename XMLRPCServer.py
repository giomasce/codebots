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
import random
import time
import logging

INACTIVITY_TIMEOUT = 600.0

passwords = {0: "abc", 1: "xyz"}

class XMLRPCServer(Thread):
    sessions = dict()

    def __init__(self, manager):
        Thread.__init__(self)
        self.daemon = True
        self.manager = manager
        self.rpcserver = SimpleXMLRPCServer(("localhost", 8080),
                                            allow_none = True)
        self.rpcserver.register_introspection_functions()
        self.rpcserver.register_function(self.add_request)
        self.rpcserver.register_function(self.get_info)
        self.rpcserver.register_function(self.wait_for_simulation)
        self.rpcserver.register_function(self.login)
        self.rpcserver.register_function(self.logout)

    def run(self):
        self.rpcserver.serve_forever()

    def login(self, team, password):
        if team not in passwords:
            return None
        if password != passwords[team]:
            return None
        session = reduce(lambda x, y: x+y, map(lambda x: random.choice('qwertyuiopasdfghjklzxcvbnm1234567890'), range(40)))
        timestamp = time.time()
        self.sessions[session] = (team, timestamp)
        logging.debug("Team %d started new session %s" % (team, session))
        return session

    def logout(self, session):
        try:
            del self.sessions[session]
            logging.debug("Session %s closed" % (session))
            return True
        except:
            return False

    def verify_session(self, session):
        try:
            data = self.sessions[session]
        except:
            return None
        (team, timestamp) = data
        diff = time.time() - timestamp
        if diff >= 0 and diff <= INACTIVITY_TIMEOUT:
            return team
        else:
            logging.debug("Session %s has expired" % (session))
            self.logout(session)
            return None

    def add_request(self, session):
        team = self.verify_session(session)
        if team == None:
            return None
        return self.manager.add_request(team)

    def get_info(self, session):
        team = self.verify_session(session)
        if team == None:
            return None
        return self.manager.get_info(team)

    def wait_for_simulation(self, session):
        team = self.verify_session(session)
        if team == None:
            return None
        return self.manager.wait_for_simulation(team)

if __name__ == "__main__":
    manager = Manager()
    s = XMLRPCServer()
