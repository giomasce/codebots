package codebots;

import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JFrame;

public class Viewer {

	public static void main(String[] args) {
		JFrame frame = new JFrame("Codebots viewer");
		frame.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent we) {
				System.exit(0);
			}
		});
		frame.setSize(500, 400);
		FieldViewer fieldViewer = new FieldViewer();
		frame.setContentPane(fieldViewer);
		frame.setVisible(true);
		Communicator comm = new Communicator(-1, "def", "localhost", 12345, fieldViewer);
		comm.start();
	}

}
