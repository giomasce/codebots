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

import codebots_pb2

def invert_dict(x):
    y = dict()
    for k, v in x.iteritems():
        y[v] = k
    return y

ACTION_MOVE, ACTION_SHOOT = 'move', 'shoot'
MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT = 'up', 'down', 'left', 'right'
TO_PROTOBUF_COORDS = { MOVE_UP: codebots_pb2.UP,
                       MOVE_DOWN: codebots_pb2.DOWN,
                       MOVE_RIGHT: codebots_pb2.RIGHT,
                       MOVE_LEFT: codebots_pb2.LEFT }
FROM_PROTOBUF_COORDS = invert_dict(TO_PROTOBUF_COORDS)
