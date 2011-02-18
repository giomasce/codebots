package codebots;

import java.awt.Color;
import java.awt.Point;
import java.util.HashMap;
import java.util.Map;

import codebots.protobuf.Codebots.CodebotsService;
import codebots.protobuf.Codebots.FieldStatus;
import codebots.protobuf.Codebots.LoginRequest;
import codebots.protobuf.Codebots.LoginResponse;
import codebots.protobuf.Codebots.StatusRequest;
import codebots.protobuf.Codebots.StatusResponse;
import codebots.protobuf.Codebots.Tank;
import codebots.protobuf.Codebots.WaitForSimulationRequest;
import codebots.protobuf.Codebots.WaitForSimulationResponse;

import com.googlecode.protobuf.socketrpc.SocketRpcChannel;
import com.googlecode.protobuf.socketrpc.SocketRpcController;

public class Communicator extends Thread {

	private int team;
	private String password;
	private String host;
	private int port;
	
	private FieldViewer fieldViewer;
	
	private String session = null;
	
	private SocketRpcChannel channel;
	private SocketRpcController controller;
	private CodebotsServiceWrapper service;

	public Communicator(int team, String password, String host, int port, FieldViewer fieldViewer) {
		this.team = team;
		this.password = password;
		this.host = host;
		this.port = port;
		this.fieldViewer = fieldViewer;
	}
	
	public void run() {
		this.connect();
		if (this.login()) {
			this.getStatus();
			while (true) {
				// Request the status
				Map<Point, Color> data = this.getStatus();
				this.fieldViewer.setData(data);
				this.waitForSimulation();
			}
		} else {
			System.err.println("Couldn't login, aborting...");
		}
	}
	
	protected void connect() {
		this.channel = new SocketRpcChannel(this.host, this.port);
		this.controller = channel.newRpcController();
		this.service = new CodebotsServiceWrapper(CodebotsService.newStub(channel), this.controller);
	}
	
	protected boolean login() {
		LoginRequest.Builder reqBuilder = LoginRequest.newBuilder();
		reqBuilder.setTeam(this.team);
		reqBuilder.setPassword(this.password);
		LoginResponse res = this.service.login(reqBuilder.build());
		this.session = res.getSession();
		//System.err.println("session " + this.session);
		if (this.session == "") {
			this.session = null;
			return false;
		}
		return true;
	}
	
	protected Map<Point, Color> getStatus() {
		StatusRequest.Builder reqBuilder = StatusRequest.newBuilder();
		reqBuilder.setSession(this.session);
		StatusResponse res = this.service.getStatus(reqBuilder.build());
		//System.err.println("status " + res);
		if (res.getSuccess()) {
			FieldStatus field = res.getFieldStatus();
			HashMap<Point, Color> data = new HashMap<Point, Color>();
			for (Tank tank: field.getTanksList()) {
				data.put(new Point(tank.getPosx(), tank.getPosy()), tank.getTeam() == 0 ? Color.RED : Color.GREEN);
			}
			return data;
		} else {
			return null;
		}
	}
	
	protected void waitForSimulation() {
		WaitForSimulationRequest.Builder reqBuilder = WaitForSimulationRequest.newBuilder();
		reqBuilder.setSession(this.session);
		@SuppressWarnings("unused")
		WaitForSimulationResponse res = this.service.waitForSimulation(reqBuilder.build());
		return;
	}
}
