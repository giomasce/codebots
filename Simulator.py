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

MAX_SHOOT_DIST = 10
MOVE_COORDS = {MOVE_UP: (0,1), MOVE_DOWN: (0,-1), MOVE_LEFT: (-1,0), MOVE_RIGHT: (1,0)}
FIELD_DIM = (15, 15)

def dist1(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Simulator:
    def __init__(self, status):
        self.status = status
        self._build_position()
        self.new_tank = len(self.status)

    def _build_position(self):
        self.position = dict()
        for k in self.status:
            if self.status[k] in self.position:
                raise ValueError("Two units in the same position!")
            self.position[self.status[k]] = [k]

    def destroy_tank(self, t):
        where = self.position[self.status[t]]
        del where[where.index(t)]
        del self.status[t]

    def create_tank(self, pos, t = None):
        if t == None:
            t = self.new_tank
            self.new_tank += 1
        if pos not in self.position:
            self.position[pos] = list()
        self.position[pos].append(t)
        self.status[t] = pos
        return t

    def move_tank(self, t, move):
        newpos = (self.status[t][0] + MOVE_COORDS[move][0], self.status[t][1] + MOVE_COORDS[move][1])
        self.destroy_tank(t)
        self.create_tank(newpos, t)

    def integrate_shoots(self, differential):
        dead = list()
        for t in differential:
            if t in self.status and ACTION_SHOOT in differential[t]:
                target = differential[t][ACTION_SHOOT]
                if dist1(self.status[t], target) <= MAX_SHOOT_DIST and target in self.position:
                    [enemy] = self.position[target]
                    dead.append(enemy)
        for t in dead:
            self.destroy_tank(t)

    def clean_position(self):
        self.position = dict(filter(lambda (x, y): len(y) > 0, self.position.iteritems()))

    def detect_collisions(self):
        self.position = dict(filter(lambda (x, y): len(y) <= 1, self.position.iteritems()))

    def integrate_movements(self, differential):
        for t in differential:
            if t in self.status and ACTION_MOVE in differential[t]:
                self.move_tank(t, differential[t][ACTION_MOVE])
        self.detect_collisions()
        self.clean_position()

    def integrate(self, differential):
        self.integrate_shoots(differential)
        self.integrate_movements(differential)

    def print_field(self):
        for y in reversed(range(FIELD_DIM[1])):
            for x in range(FIELD_DIM[0]):
                if (x,y) in self.position:
                    [unit] = self.position[(x,y)]
                    print "%2d" % (unit),
                else:
                    print " .",
            print
