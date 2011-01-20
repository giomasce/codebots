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
from Simulator import Simulator, Tank
from XMLRPCServer import XMLRPCServer
from Constants import *
import logging
import time

status = dict()
differential = dict()

status[0] = Tank(0, (1, 3))
status[1] = Tank(1, (5, 6))
status[2] = Tank(1, (10, 10))
status[3] = Tank(1, (7, 3))
status[4] = Tank(0, (7, 1))
status[5] = Tank(0, (10, 3))
status[6] = Tank(1, (10, 1))

differential[1] = {ACTION_MOVE: MOVE_UP, ACTION_SHOOT: (10, 10)}
differential[2] = {ACTION_MOVE: MOVE_DOWN, ACTION_SHOOT: (1, 3)}
differential[3] = {ACTION_MOVE: MOVE_DOWN}
differential[4] = {ACTION_MOVE: MOVE_UP}
differential[5] = {ACTION_MOVE: MOVE_DOWN, ACTION_SHOOT: (10, 1)}
differential[6] = {ACTION_MOVE: MOVE_UP}

def test_rpc():
    logging.basicConfig(level = logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    simulator = Simulator(status)
    manager = Manager(simulator)
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

def test_simulator():
    simulator = Simulator(status)

    print "BEFORE"
    print simulator.position
    print simulator.status
    simulator.print_field()
    simulator.integrate(differential)
    print
    print "AFTER"
    print simulator.position
    print simulator.status
    simulator.print_field()

if __name__ == "__main__":
    test_rpc()
