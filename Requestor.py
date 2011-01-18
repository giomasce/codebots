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
import logging

def main():
    logging.basicConfig(level = logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    proxy = ServerProxy("http://localhost:8080")
    logging.info("Sending add_request()")
    proxy.add_request()
    logging.info("Sending get_info()")
    proxy.get_info()
    logging.info("Sending wait_for_simulation()")
    proxy.wait_for_simulation()
    logging.info("Finished!")

if __name__ == "__main__":
    main()
