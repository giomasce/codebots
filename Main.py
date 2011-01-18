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

from Manager import Manager, Ticker
from XMLRPCServer import XMLRPCServer
import logging
import time

def main():
    logging.basicConfig(level = logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    manager = Manager()
    ticker = Ticker(5.0, manager)
    xmlrpcserver = XMLRPCServer(manager)

    logging.info("Starting main threads")

    ticker.start()
    xmlrpcserver.start()

    # To stop the system with Ctrl-C
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ticker.self_destruct()

if __name__ == "__main__":
    main()
