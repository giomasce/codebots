package codebots;

import codebots.protobuf.Codebots.CodebotsService;
import codebots.protobuf.Codebots.LoginRequest;
import codebots.protobuf.Codebots.LoginResponse;
import codebots.protobuf.Codebots.LogoutRequest;
import codebots.protobuf.Codebots.LogoutResponse;
import codebots.protobuf.Codebots.StatusRequest;
import codebots.protobuf.Codebots.StatusResponse;
import codebots.protobuf.Codebots.WaitForSimulationRequest;
import codebots.protobuf.Codebots.WaitForSimulationResponse;

import com.googlecode.protobuf.socketrpc.SocketRpcChannel;
import com.googlecode.protobuf.socketrpc.SocketRpcController;

public class Communicator extends Thread {

	private int team;
	private String password;
	private String host;
	private int port;
	
	private ViewerPanel panel;
	
	private String session = null;
	private boolean terminating = false;
	
	private SocketRpcChannel channel;
	private SocketRpcController controller;
	private CodebotsServiceWrapper service;

	public Communicator(int team, String password, String host, int port, ViewerPanel panel) {
		this.team = team;
		this.password = password;
		this.host = host;
		this.port = port;
		this.panel = panel;
	}
	
	public void run() {
		this.connect();
		if (this.login()) {
			while (!this.terminating) {
				this.panel.setStatus(this.getStatus());
				this.waitForSimulation();
			}
		} else {
			System.err.println("Couldn't login, aborting...");
		}
	}
	
	public void terminate() {
		this.terminating = true;
		this.logout();
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
	
	protected StatusResponse getStatus() {
		StatusRequest.Builder reqBuilder = StatusRequest.newBuilder();
		reqBuilder.setSession(this.session);
		StatusResponse res = this.service.getStatus(reqBuilder.build());
		//System.err.println("status " + res);
		if (res.getSuccess()) {
			return res;
		} else {
			return null;
		}
	}
	
	protected int waitForSimulation() {
		WaitForSimulationRequest.Builder reqBuilder = WaitForSimulationRequest.newBuilder();
		reqBuilder.setSession(this.session);
		WaitForSimulationResponse res = this.service.waitForSimulation(reqBuilder.build());
		return res.getTurnNum();
	}
	
	protected boolean logout() {
		if (this.session == null) {
			return true;
		}
		LogoutRequest.Builder reqBuilder = LogoutRequest.newBuilder();
		reqBuilder.setSession(this.session);
		LogoutResponse res = this.service.logout(reqBuilder.build());
		return res.getSuccess();
	}
}
