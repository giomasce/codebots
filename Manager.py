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
    turn_num = 0

    main_lock = ReadWriteLock()
    request_lock = threading.RLock() # Maybe not necessary
    simulation_sync = threading.Condition()

    requests = []
    last_differential = None
    last_differential_turn = None

    def __init__(self, simulator):
        self.simulator = simulator

    def add_request(self, team, turn, actions):
        if team < 0:
            logging.info("Rejecting add_request() from team %d" % (team))
            return False
        # Fix numbers in the request
        actions = dict(map(lambda (x, y): (int(x), y), actions.iteritems()))
        request_time = time.time()
        self.main_lock.acquireRead()
        obtain_time = time.time()
        logging.debug("Obtained read lock after %.3f seconds" % (obtain_time - request_time))
        self.request_lock.acquire()
        request_obtain_time = time.time()
        logging.debug("Obtained request lock after %.3f seconds" % (request_obtain_time - obtain_time))
        try:
            # Store the request
            if turn == self.turn_num:
                self.requests.append((team, actions))
                return True
            else:
                logging.debug("Received request with mismatching turn number %d while at turn %d" % (turn, self.turn_num))
                return False
        finally:
            finish_time = time.time()
            logging.debug("Write request took %.3f seconds" % (finish_time - request_obtain_time))
            self.request_lock.release()
            self.main_lock.release()

    def get_info(self, team):
        request_time = time.time()
        self.main_lock.acquireRead()
        obtain_time = time.time()
        logging.debug("Obtained read lock after %.3f seconds" % (obtain_time - request_time))
        try:
            # Read structures and return sensible information
            return {'turn_num': self.turn_num, 'status': self.simulator.get_external_status()}
        finally:
            finish_time = time.time()
            logging.debug("Read request took %.3f seconds" % (finish_time - obtain_time))
            self.main_lock.release()

    def get_short_info(self, team):
        request_time = time.time()
        self.main_lock.acquireRead()
        obtain_time = time.time()
        logging.debug("Obtained read lock after %.3f seconds" % (obtain_time - request_time))
        try:
            # Read structures and return sensible information
            return {'turn_num': self.turn_num}
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
            self.last_differential = self.simulator.calculate_differential(self.requests)
            self.simulator.integrate(self.last_differential)
            self.requests = []
            self.last_differential_turn = self.turn_num
        finally:
            finish_time = time.time()
            logging.debug("Simulation for turn %d took %.3f seconds" % (self.turn_num, finish_time - obtain_time))
            self.state = self.STATE_WAITING
            self.turn_num += 1
            self.main_lock.release()
            with self.simulation_sync:
                self.simulation_sync.notifyAll()

    def get_differential(self, turn):
        request_time = time.time()
        self.main_lock.acquireWrite()
        obtain_time = time.time()
        logging.debug("Obtained write read after %.3f seconds" % (obtain_time - request_time))
        try:
            if turn == self.last_differential_turn:
                return self.last_differential
            else:
                return None
        finally:
            finish_time = time.time()
            logging.debug("Differential request took %.3f seconds" % (finish_time - obtain_time))
            self.main_lock.release()

    def wait_for_simulation(self, team):
        with self.simulation_sync:
            self.simulation_sync.wait()
        return True

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
