package codebots;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
import java.awt.geom.Point2D;
import java.util.HashMap;
import java.util.Map;

import javax.swing.JComponent;

public class FieldViewer extends JComponent
implements MouseListener, MouseMotionListener, MouseWheelListener {

	private static final long serialVersionUID = 1L;

	private static final double SMALL_ZOOM_THRESHOLD = 5.0;
	private static final double ZOOM_FACTOR = 1.1;

	private Point relativePosition = new Point(0, 0);
	private double squareSide = 10.0;
	private Map<Point, Color> data = new HashMap<Point, Color>();
	
	private Point selectedPoint = null;
	
	public FieldViewer() {
		/*data.put(new Point(0, 0), Color.GREEN);
		data.put(new Point(0, 1), Color.RED);
		data.put(new Point(10, 10), Color.BLUE);
		data.put(new Point(10, 11), Color.CYAN);
		data.put(new Point(11, 10), Color.ORANGE);*/
		this.addMouseListener(this);
		this.addMouseMotionListener(this);
		this.addMouseWheelListener(this);
	}
	
	@SuppressWarnings("unused")
	private void drawSquareWithBorder(Graphics g, Point square) {
		Point base = this.realToView(this.squareToReal(square));
		Point ll = base;
		Point lr = new Point(base.x + (int) this.squareSide - 2, base.y);
		Point ul = new Point(base.x, base.y + (int) this.squareSide - 2);
		Point ur = new Point(base.x + (int) this.squareSide - 2, base.y + (int) this.squareSide - 2);
		g.setColor(Color.BLACK);
		g.drawLine(ll.x, ll.y, lr.x, lr.y);
		g.drawLine(ll.x, ll.y, ul.x, ul.y);
		g.drawLine(ur.x, ur.y, ul.x, ul.y);
		g.drawLine(ur.x, ur.y, lr.x, lr.y);
		if (data.containsKey(square)) {
			g.setColor(data.get(square));
			g.fillRect(base.x + 1, base.y + 1, (int) this.squareSide - 3, (int) this.squareSide - 3);
		}
	}
	
	private void drawSquare(Graphics g, Point square) {
		Point base = this.realToView(this.squareToReal(square));
		Point ll = base;
		Point lr = new Point(base.x + (int) this.squareSide, base.y);
		Point ul = new Point(base.x, base.y + (int) this.squareSide);
		g.setColor(Color.BLACK);
		g.drawLine(ll.x, ll.y, lr.x, lr.y);
		g.drawLine(ll.x, ll.y, ul.x, ul.y);
		if (data.containsKey(square)) {
			g.setColor(data.get(square));
			g.fillRect(base.x + 1, base.y + 1, (int) this.squareSide - 1, (int) this.squareSide - 1);
		}
	}

	public synchronized void paint(Graphics g) {
		int width = this.getWidth();
		int height = this.getHeight();
		int squareNumX = width / (2 * (int) this.squareSide) + 2;
		int squareNumY = height / (2 * (int) this.squareSide) + 2;
		/*int squareNumX = 2;
		int squareNumY = 2;*/
		Point centralSquare = this.realToSquare(this.viewToReal(new Point(width/2, height/2)));
		for (int x = centralSquare.x - squareNumX; x <= centralSquare.x + squareNumX; x++) {
			for (int y = centralSquare.y - squareNumY; y <= centralSquare.y + squareNumY; y++) {
				this.drawSquare(g, new Point(x, y));
			}
		}
	}
	
	public synchronized void setData(Map<Point, Color> data) {
		this.data = data;
		this.repaint();
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
				p.x / (int) this.squareSide, p.y >= 0 ?
				-(p.y / (int) this.squareSide) :
				((-p.y-1) / (int) this.squareSide) + 1);
	}
	
	public Point2D.Double realToSquareDouble(Point p) {
		Point square = this.realToSquare(p);
		Point base = this.squareToReal(square);
		//System.err.println("square " + square);
		//System.err.println("base " + base);
		double offsetX = p.x - base.x;
		double offsetY = p.y - base.y;
		return new Point2D.Double(square.x + offsetX / (int) this.squareSide,
				square.y + 1 - offsetY / (int) this.squareSide);
	}
	
	public Point squareToReal(Point p) {
		return new Point(p.x * (int) this.squareSide, -p.y * (int) this.squareSide);
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
	public void mouseMoved(MouseEvent e) {
		//System.err.println("position " + this.realToSquareDouble(this.viewToReal(e.getPoint())));
	}

	@Override
	public void mouseWheelMoved(MouseWheelEvent e) {
		double oldSquareSide = this.squareSide;
		if (this.squareSide < SMALL_ZOOM_THRESHOLD) {
			this.squareSide -= e.getWheelRotation();
		} else {
			this.squareSide *= Math.pow(ZOOM_FACTOR, (double) -e.getWheelRotation());
		}
		if (this.squareSide < 1.1) {
			this.squareSide = 1.1;
		}
		double lambda = this.squareSide / oldSquareSide;
		Point2D.Double mouseSquare = this.realToSquareDouble(this.viewToReal(e.getPoint()));
		Point2D.Double posSquare = this.realToSquareDouble(this.relativePosition);
		//System.err.println("mouseSquare " + mouseSquare);
		//System.err.println("posSquare " + posSquare);
		Point newPosSquare = new Point((int) (1 / lambda * (posSquare.x - mouseSquare.x) + mouseSquare.x),
				(int) (1 / lambda * (posSquare.y - mouseSquare.y) + mouseSquare.y));
		this.relativePosition = this.squareToReal(newPosSquare);
		this.repaint();
	}

}
