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
import logging

class PBRPCImpl(codebots_pb2.CodebotsService):

    def __init__(self, manager, session_server):
        codebots_pb2.CodebotsService.__init__(self)
        self.manager = manager
        self.session_server = session_server

    def login(self, controller, request, done):
        team = request.team
        password = request.password
        session = self.session_server.login(team, password)
        if session == None:
            session = ""
        res = codebots_pb2.LoginResponse()
        res.session = session
        done.run(res)

    def logout(self, controller, request, done):
        success = self.session_server.logout(request.session)
        done.run(codebots_pb2.LogoutResponse(success = success))

    def getStatus(self, controller, request, done):
        team = self.session_server.verify_session(request.session)
        res = codebots_pb2.StatusResponse()
        if team == None:
            res.success = False
        else:
            res.turnNum = self.manager.turn_num
            for (t, tank) in self.manager.simulator.status.iteritems():
                tmp = res.fieldStatus.tanks.add()
                tmp.id = t
                tmp.team = tank.team
                (tmp.posx, tmp.posy) = tank.position
            res.success = True
        done.run(res)

    def waitForSimulation(self, controller, request, done):
        team = self.session_server.verify_session(request.session)
        res = codebots_pb2.WaitForSimulationResponse()
        if team == None:
            res.turnNum = -1
        else:
            self.manager.wait_for_simulation(team)
            res.turnNum = self.manager.turn_num
        done.run(res)

class PBRPCFilter(logging.Filter):
    def filter(self, record):
        return False

class PBRPCServer(SessionServer):

    def __init__(self, manager, port = 12345):
        SessionServer.__init__(self, manager)
        self.server = SocketRpcServer(port)
        self.server.registerService(PBRPCImpl(self.manager, self))
        logging.getLogger('protobuf.socketrpc.server').addFilter(PBRPCFilter())

    def run(self):
        self.server.run()
