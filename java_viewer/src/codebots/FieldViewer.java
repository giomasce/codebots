package codebots;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.util.HashSet;

import javax.swing.JComponent;

public class FieldViewer extends JComponent implements MouseListener, MouseMotionListener {

	private static final long serialVersionUID = 1L;

	private Point relativePosition = new Point(0, 0);
	private int squareSide = 10;
	private HashSet<Point> data = new HashSet<Point>();
	
	private Point selectedPoint = null;
	
	public FieldViewer() {
		data.add(new Point(0, 0));
		data.add(new Point(0, 1));
		this.addMouseListener(this);
		this.addMouseMotionListener(this);
	}
	
	private void drawSquare(Graphics g, Point square) {
		Point base = this.realToView(this.squareToReal(square));
		Point ll = base;
		Point lr = new Point(base.x + this.squareSide - 2, base.y);
		Point ul = new Point(base.x, base.y + this.squareSide - 2);
		Point ur = new Point(base.x + this.squareSide - 2, base.y + this.squareSide - 2);
		g.setColor(Color.BLACK);
		g.drawLine(ll.x, ll.y, lr.x, lr.y);
		g.drawLine(ll.x, ll.y, ul.x, ul.y);
		g.drawLine(ur.x, ur.y, ul.x, ul.y);
		g.drawLine(ur.x, ur.y, lr.x, lr.y);
		if (data.contains(square)) {
			g.setColor(Color.RED);
			g.fillRect(base.x + 1, base.y + 1, this.squareSide - 3, this.squareSide - 3);
		}
	}

	public void paint(Graphics g) {
		int width = this.getWidth();
		int height = this.getHeight();
		int squareNumX = width / (2 * this.squareSide) + 2;
		int squareNumY = height / (2 * this.squareSide) + 2;
		/*int squareNumX = 2;
		int squareNumY = 2;*/
		Point centralSquare = this.realToSquare(this.viewToReal(new Point(width/2, height/2)));
		for (int x = centralSquare.x - squareNumX; x <= centralSquare.x + squareNumX; x++) {
			for (int y = centralSquare.y - squareNumY; y <= centralSquare.y + squareNumY; y++) {
				this.drawSquare(g, new Point(x, y));
			}
		}
	}
	
	public Point viewToReal(Point p) {
		return new Point(p.x + this.relativePosition.x - this.getWidth() / 2,
				p.y + this.relativePosition.y - this.getHeight() / 2);
	}
	
	public Point realToView(Point p) {
		return new Point(p.x - this.relativePosition.x + this.getWidth() / 2,
				p.y - this.relativePosition.y + this.getHeight() / 2);
	}
	
	public Point realToSquare(Point p) {
		return new Point(
				p.x / this.squareSide, p.y >= 0 ?
				-(p.y / this.squareSide) :
				((-p.y-1) / this.squareSide) + 1);
	}
	
	public Point squareToReal(Point p) {
		return new Point(p.x * this.squareSide, -p.y * this.squareSide);
	}

	@Override
	public void mouseClicked(MouseEvent e) {}

	@Override
	public void mouseEntered(MouseEvent e) {}

	@Override
	public void mouseExited(MouseEvent e) {}

	@Override
	public void mousePressed(MouseEvent e) {
		//System.err.println("press " + e);
		this.selectedPoint = e.getPoint();
	}

	@Override
	public void mouseReleased(MouseEvent e) {
		//System.err.println("release " + e);
		this.selectedPoint = null;
	}

	@Override
	public void mouseDragged(MouseEvent e) {
		//System.err.println("drag " + e);
		this.relativePosition = new Point(this.relativePosition.x + this.selectedPoint.x - e.getPoint().x,
				this.relativePosition.y + this.selectedPoint.y - e.getPoint().y);
		this.selectedPoint = e.getPoint();
		this.repaint();
	}

	@Override
	public void mouseMoved(MouseEvent e) {}

}
