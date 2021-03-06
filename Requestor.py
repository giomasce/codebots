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
from Constants import *
import logging

team = 0
password = "abc"

def main():
    logging.basicConfig(level = logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    proxy = ServerProxy("http://localhost:8080")
    logging.info("Logging in with team %s and password %s" % (team, password))
    session = proxy.login(team, password)
    logging.info("Initiated session %s" % (session))
    #session = "lgpb1yqve5tn0ggu3rxoktmt112uthvfbgemnou8"
    try:
        res = proxy.get_info(session)
        turn_num = res['turn_num']
        logging.info("Sending add_request()")
        res = proxy.add_request(session, turn_num, {"5": {ACTION_MOVE: MOVE_DOWN}, "4": {ACTION_SHOOT: (7, 3)}})
        logging.info("Response: %s" % (repr(res)))
    finally:
        logging.info("Logging out")
        res = proxy.logout(session)
        logging.info("Response: %s" % (repr(res)))
        logging.info("Finished!")

if __name__ == "__main__":
    main()
