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


from xmlrpclib import ServerProxy
from Simulator import Simulator
import logging

team = -1
password = "def"

def main():
    logging.basicConfig(level = logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    proxy = ServerProxy("http://localhost:8080")
    logging.info("Logging in with team %s and password %s" % (team, password))
    session = proxy.login(team, password)
    logging.info("Initiated session %s" % (session))
    try:
        while True:
            #logging.info("Sending get_info()")
            res = proxy.get_info(session)
            #logging.info("Response: %s" % (repr(res)))
            turn_num = res['turn_num']
            simulator = Simulator.from_external_status(res['status'])
            print "TURN %d" % (turn_num)
            simulator.print_field()
            print
            proxy.wait_for_simulation(session)
    finally:
        logging.info("Logging out")
        res = proxy.logout(session)
        logging.info("Response: %s" % (repr(res)))
        logging.info("Finished!")

if __name__ == "__main__":
    main()

