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

from RWLock import ReadWriteLock
import threading
import time
import logging

class Manager:
    STATE_WAITING, STATE_SIMULATING = range(2)

    state = STATE_WAITING
    main_lock = ReadWriteLock()
    diff_lock = threading.RLock()

    def add_request(self):
        request_time = time.time()
        self.main_lock.acquireRead()
        obtain_time = time.time()
        logging.debug("Obtained read lock after %.3f seconds" % (obtain_time - request_time))
        self.diff_lock.acquire()
        diff_obtain_time = time.time()
        logging.debug("Obtain differential lock after %.3f seconds" % (diff_obtain_time - obtain_time))
        try:
            pass
        finally:
            finish_time = time.time()
            logging.debug("Write request took %.3f seconds" % (finish_time - diff_obtain_time))
            self.diff_lock.release()
            self.main_lock.release()

    def get_info(self):
        request_time = time.time()
        self.main_lock.acquireRead()
        obtain_time = time.time()
        logging.debug("Obtained read lock after %.3f seconds" % (obtain_time - request_time))
        try:
            # Read structures and return sensible information
            pass
        finally:
            finish_time = time.time()
            logging.debug("Read request took %.3f seconds" % (finish_time - obtain_time))
            self.main_lock.release()

    def simulate(self):
        request_time = time.time()
        self.main_lock.acquireWrite()
        obtain_time = time.time()
        logging.debug("Obtained write lock after %.3f seconds" % (obtain_time - request_time))
        self.state = self.STATE_SIMULATING
        try:
            # Execute a simulation step
            pass
        finally:
            finish_time = time.time()
            logging.debug("Simulation took %.3f seconds" % (finish_time - obtain_time))
            self.state = self.STATE_WAITING
            self.main_lock.release()

class Ticker(threading.Thread):
    def __init__(self, time, manager):
        threading.Thread.__init__(self)
        self.time = time
        self.manager = manager
        self.again = True
        self.waiter = threading.Condition()

    def run(self):
        with self.waiter:
            while (self.again):
                logging.debug("Spawning simulation call")
                threading.Thread(target = self.manager.simulate).start()
                self.waiter.wait(self.time)
        logging.info("Terminating")

    def self_destruct(self):
        logging.info("Scheduling termination")
        self.again = False
        with self.waiter:
            self.waiter.notifyAll()

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    manager = Manager()
    ticker = Ticker(5.0, manager)
    ticker.start()

    # To stop the system with Ctrl-C
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ticker.self_destruct()
