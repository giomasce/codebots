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

from Constants import *
from threading import RLock

MAX_SHOOT_DIST = 10
MOVE_COORDS = {MOVE_UP: (0,1), MOVE_DOWN: (0,-1), MOVE_LEFT: (-1,0), MOVE_RIGHT: (1,0)}
FIELD_DIM = (15, 15)

def dist1(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Tank:
    def __init__(self, team, position):
        self.team = team
        self.position = tuple(position)

    def clone(self):
        return Tank(self.team, self.position)

    def __repr__(self):
        return "<Tank: team %d, pos %s>" % (self.team, repr(self.position))

class Simulator:
    tank_lock = RLock()

    def __init__(self, status = dict()):
        self.status = status
        self._build_position()
        if len(self.status) >= 1:
            self.new_tank = 1 + max(self.status.keys())
        else:
            self.new_tank = 1

    def _build_position(self):
        self.position = dict()
        for t in self.status:
            tank = self.status[t]
            self.position[tank.position] = [t]

    def get_external_status(self):
        return dict(map(lambda (x, y): (repr(x), y), self.status.iteritems()))

    @staticmethod
    def from_external_status(status):
        fixed = dict(map(lambda (x, y): (int(x), Tank(**y)), status.iteritems()))
        return Simulator(fixed)

    def destroy_tank(self, t):
        where_del = self.position[self.status[t].position]
        del where_del[where_del.index(t)]
        del self.status[t]

    def create_tank(self, tank, t = None):
        if t == None:
            with self.tank_lock:
                t = self.new_tank
                self.new_tank += 1
        if tank.position not in self.position:
            self.position[tank.position] = list()
        self.position[tank.position].append(t)
        self.status[t] = tank
        return t

    def move_tank(self, t, move):
        tank = self.status[t].clone()
        tank.position = (tank.position[0] + MOVE_COORDS[move][0], tank.position[1] + MOVE_COORDS[move][1])
        self.destroy_tank(t)
        self.create_tank(tank, t)

    def integrate_shoots(self, differential):
        dead = list()
        for t in differential:
            if t in self.status and ACTION_SHOOT in differential[t]:
                target = tuple(differential[t][ACTION_SHOOT])
                if dist1(self.status[t].position, target) <= MAX_SHOOT_DIST and target in self.position:
                    [enemy] = self.position[target]
                    dead.append(enemy)
        for t in dead:
            self.destroy_tank(t)

    def clean_position(self):
        self.position = dict(filter(lambda (x, y): len(y) > 0, self.position.iteritems()))

    def detect_collisions(self):
        dead = reduce(lambda x, y: x+y, filter(lambda x: len(x) > 1, self.position.values()), [])
        for t in dead:
            self.destroy_tank(t)

    def integrate_movements(self, differential):
        for t in differential:
            if t in self.status and ACTION_MOVE in differential[t]:
                self.move_tank(t, differential[t][ACTION_MOVE])
        self.detect_collisions()
        self.clean_position()

    def integrate(self, differential):
        self.integrate_shoots(differential)
        self.integrate_movements(differential)

    def calculate_differential(self, requests):
        differential = {}
        for req in requests:
            (team, actions) = req
            for t, act in actions.iteritems():
                if t in self.status and self.status[t].team == team:
                    if t not in differential:
                        differential[t] = dict(act)
                    else:
                        differential[t].update(act)
        return differential

    def print_field(self):
        for y in reversed(range(FIELD_DIM[1])):
            for x in range(FIELD_DIM[0]):
                if (x,y) in self.position:
                    [t] = self.position[(x,y)]
                    print "%2d/%1d" % (t, self.status[t].team),
                else:
                    print "   .",
            print
