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

from SessionServer import SessionServer
from protobuf.socketrpc.server import SocketRpcServer
import codebots_pb2

class PBRPCImpl(codebots_pb2.StatusService):

    def __init__(self, manager):
        codebots_pb2.StatusService.__init__(self)
        self.manager = manager

    def getStatus(self, controller, request, done):
        res = codebots_pb2.StatusResponse()
        res.turnNum = self.manager.turn_num
        for (t, tank) in self.manager.simulator.status.iteritems():
            tmp = res.fieldStatus.tanks.add()
            tmp.id = t
            tmp.team = tank.team
            (tmp.posx, tmp.posy) = tank.position
        done.run(res)

    def waitForSimulation(self, controller, request, done):
        self.manager.wait_for_simulation(0)
        res = codebots_pb2.WaitForSimulationResponse()
        done.run(res)

class PBRPCServer(SessionServer):

    def __init__(self, manager, port = 12345):
        SessionServer.__init__(self, manager)
        self.server = SocketRpcServer(port)
        self.server.registerService(PBRPCImpl(self.manager))

    def run(self):
        self.server.run()
