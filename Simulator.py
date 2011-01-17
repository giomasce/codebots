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

MAX_SHOOT_DIST = 10
ACTION_MOVE, ACTION_SHOOT = 'move', 'shoot'
MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT = 'up', 'down', 'left', 'right'
MOVE_COORDS = {MOVE_UP: (0,1), MOVE_DOWN: (0,-1), MOVE_LEFT: (-1,0), MOVE_RIGHT: (1,0)}
FIELD_DIM = (15, 15)

status = dict()
differential = dict()

status[0] = (1, 3)
status[1] = (5, 6)
status[2] = (10, 10)
status[3] = (7, 3)
status[4] = (7, 1)
status[5] = (10, 3)
status[6] = (10, 1)
new_tank = 7

differential[1] = {ACTION_MOVE: MOVE_UP, ACTION_SHOOT: (10, 10)}
differential[2] = {ACTION_MOVE: MOVE_DOWN, ACTION_SHOOT: (1, 3)}
differential[3] = {ACTION_MOVE: MOVE_DOWN}
differential[4] = {ACTION_MOVE: MOVE_UP}
differential[5] = {ACTION_MOVE: MOVE_DOWN, ACTION_SHOOT: (10, 1)}
differential[6] = {ACTION_MOVE: MOVE_UP}

def build_position(status):
    position = dict()
    for k in status:
        if status[k] in position:
            raise ValueError("Two units in the same position!")
        position[status[k]] = [k]
    return position

position = build_position(status)

def dist1(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def destroy_tank(t):
    where = position[status[t]]
    del where[where.index(t)]
    del status[t]

def create_tank(pos, t = None):
    if t == None:
        t = new_tank
        new_tank += 1
    if pos not in position:
        position[pos] = list()
    position[pos].append(t)
    status[t] = pos
    return t

def move_tank(t, move):
    newpos = (status[t][0] + MOVE_COORDS[move][0], status[t][1] + MOVE_COORDS[move][1])
    destroy_tank(t)
    create_tank(newpos, t)

def integrate_shoots():
    dead = list()
    for t in differential:
        if t in status and ACTION_SHOOT in differential[t]:
            target = differential[t][ACTION_SHOOT]
            if dist1(status[t], target) <= MAX_SHOOT_DIST and target in position:
                [enemy] = position[target]
                dead.append(enemy)
    for t in dead:
        destroy_tank(t)

def clean_position():
    global position
    position = dict(filter(lambda (x, y): len(y) > 0, position.iteritems()))

def detect_collisions():
    global position
    position = dict(filter(lambda (x, y): len(y) <= 1, position.iteritems()))

def integrate_movements():
    for t in differential:
        if t in status and ACTION_MOVE in differential[t]:
            move_tank(t, differential[t][ACTION_MOVE])
    detect_collisions()
    clean_position()

def integrate():
    integrate_shoots()
    integrate_movements()

def print_field():
    for y in reversed(range(FIELD_DIM[1])):
        for x in range(FIELD_DIM[0]):
            if (x,y) in position:
                print "%2d" % (position[(x,y)][0]),
            else:
                print " .",
        print

print "BEFORE"
print position
print status
print_field()
integrate()
print "AFTER"
print position
print status
print_field()
