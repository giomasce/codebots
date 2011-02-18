package codebots;

import com.google.protobuf.RpcCallback;
import com.google.protobuf.RpcController;

import codebots.protobuf.Codebots.CodebotsService;
import codebots.protobuf.Codebots.LoginRequest;
import codebots.protobuf.Codebots.LoginResponse;
import codebots.protobuf.Codebots.LogoutRequest;
import codebots.protobuf.Codebots.LogoutResponse;
import codebots.protobuf.Codebots.StatusRequest;
import codebots.protobuf.Codebots.StatusResponse;
import codebots.protobuf.Codebots.WaitForSimulationRequest;
import codebots.protobuf.Codebots.WaitForSimulationResponse;

public class CodebotsServiceWrapper {
	
	private CodebotsService service;
	private RpcController controller;
	
	public CodebotsServiceWrapper(CodebotsService service,
			RpcController controller) {
		this.service = service;
		this.controller = controller;
	}

	class CallbackWrapper<K> implements RpcCallback<K> {

		K res;
		
		@Override
		public void run(K res) {
			this.res = res;
		}
		
		public K getRes() {
			return this.res;
		}
		
	}

	public StatusResponse getStatus(StatusRequest request) {
		CallbackWrapper<StatusResponse> callback = new CallbackWrapper<StatusResponse>();
		this.service.getStatus(this.controller, request, callback);
		return callback.getRes();
	}

	public LoginResponse login(LoginRequest request) {
		CallbackWrapper<LoginResponse> callback = new CallbackWrapper<LoginResponse>();
		this.service.login(this.controller, request, callback);
		return callback.getRes();
	}

	public LogoutResponse logout(LogoutRequest request) {
		CallbackWrapper<LogoutResponse> callback = new CallbackWrapper<LogoutResponse>();
		this.service.logout(this.controller, request, callback);
		return callback.getRes();
	}

	public WaitForSimulationResponse waitForSimulation(WaitForSimulationRequest request) {
		CallbackWrapper<WaitForSimulationResponse> callback = new CallbackWrapper<WaitForSimulationResponse>();
		this.service.waitForSimulation(this.controller, request, callback);
		return callback.getRes();
	}

}
