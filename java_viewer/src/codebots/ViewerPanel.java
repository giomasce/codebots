package codebots;

import java.awt.Color;
import java.awt.Point;
import java.util.HashMap;

import javax.swing.BoxLayout;
import javax.swing.JLabel;
import javax.swing.JPanel;

import codebots.protobuf.Codebots.FieldStatus;
import codebots.protobuf.Codebots.StatusResponse;
import codebots.protobuf.Codebots.Tank;

public class ViewerPanel extends JPanel {

	private static final long serialVersionUID = 1L;
	
	private FieldViewer fieldViewer;
	private JLabel turnLabel;
	
	public ViewerPanel() {
		this.fieldViewer = new FieldViewer();
		this.turnLabel = new JLabel("(disconnected)");
		this.setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
		this.add(this.turnLabel);
		this.add(this.fieldViewer);
		this.setVisible(true);
	}
	
	public void setStatus(StatusResponse res) {
		FieldStatus field = res.getFieldStatus();
		HashMap<Point, Color> data = new HashMap<Point, Color>();
		for (Tank tank: field.getTanksList()) {
			data.put(new Point(tank.getPosx(), tank.getPosy()), tank.getTeam() == 0 ? Color.RED : Color.GREEN);
		}
		this.fieldViewer.setData(data);
		this.turnLabel.setText("Turn num. " + res.getTurnNum());
	}

}
