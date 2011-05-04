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
from Simulator import Simulator, Tank, Differential
from protobuf.socketrpc import RpcService
from protobuf.socketrpc.channel import SocketRpcChannel
import logging
import codebots_pb2
import time
import random
import sys

def main():
    logging.basicConfig(level = logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    team = int(sys.argv[1])
    password = sys.argv[2]
    logging.info("Logging in with team %s and password %s" % (team, password))
    service = RpcService(codebots_pb2.CodebotsService_Stub, 12345, "localhost")
    res = service.login(codebots_pb2.LoginRequest(team = team, password = password))
    session = res.session
    logging.info("Initiated session %s" % (session))
    try:
        while True:
            # Getting the status (a bit stupid, but I need testing)
            res = service.getShortStatus(codebots_pb2.ShortStatusRequest(session = session))
            turn = res.turnNum
            res = service.getStatus(codebots_pb2.StatusRequest(session = session))
            fieldStatus = res.fieldStatus
            print "TURN %d" % (turn)

            # Getting last differential
            res = service.getDifferential(codebots_pb2.GetDifferentialRequest(session = session, turn = turn-1))
            print Differential.from_protobuf(res)

            # Performing a random request
            req = codebots_pb2.AddRequestsRequest(session = session, turn = turn)
            for tank in fieldStatus.tanks:
                tankReq = req.requests.add()
                tankReq.id = tank.id
                tankReq.move = random.randint(0, 3)
            res = service.addRequests(req)
            print res

            # Waiting for next step
            res = service.waitForSimulation(codebots_pb2.WaitForSimulationRequest(session = session))
            
            print
    except KeyboardInterrupt:
        logging.info("Shutting down")
    finally:
        logging.info("Logging out")
        res = service.logout(codebots_pb2.LogoutRequest(session = session))
        logging.info("Finished!")        

if __name__ == "__main__":
    main()
