import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridLayout;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.geom.Path2D;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import org.openstreetmap.gui.jmapviewer.JMapViewer;
import java.io.*;
import java.util.List;
import org.jdom.JDOMException;
import org.openstreetmap.gui.jmapviewer.Coordinate;
import org.openstreetmap.gui.jmapviewer.MapMarkerDot;
import org.openstreetmap.gui.jmapviewer.MapPolygonImpl;
import org.openstreetmap.gui.jmapviewer.interfaces.ICoordinate;

/**
 *
 * This class can draw a panel to put him int a tabbed pane.
 * @author Anthony Borghi
 * @version 1.0
 */
public class OngDraw implements ActionListener {

    private JButton Start;
    private JButton Stop;
    private JButton Load;
    private JButton Connect;
    private JButton Reini;

    private JTextField Port;
    private JTextField Serv;
    private JTextField Speed;

    private JLabel DataPOI;
    private JLabel DataDist;
    private JLabel LedConnect;
    private JLabel LedTxt;
    private JLabel SpeedTxt;
    private JLabel ServTxt;
    private JLabel PortTxt;
    private JLabel Time;

    private JPanel Z1;
    private JPanel Z2;
    private JPanel Z3;
    private JPanel Z4;
    private JPanel Z5;
    private JPanel Z6;

    private JPanel ButonBar;
    private JPanel Led;
    private JPanel LineServ;
    private JPanel LinePort;
    private JPanel LineCon;

    private JMapViewer Map;

    private Font font;

    private JPanel Ong;

    private JButton Ajout;

    private HTTPUse CReq;

    private List<Coordinate> route;
    private Calcul Calc;
    private int i;
    private int IdTr;
    private MapMarkerDot Drone;
    private File KML;
    private ThreadCalc Pos;

    /**
     * Basic Constructor generate a JPanel with IHM to put him in tabbed pane
     */
    OngDraw() {
        //throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
        double Latcenter = 42.7122595;
        double Loncenter = 2.6904300;        
        Calc = new Calcul();
        /*----Initialisation des champs----*/
        this.Serv = new JTextField("172.20.200.173"/*"www.google.fr"*/, 10);
        this.Port = new JTextField("5124"/*"80"*/, 10);
        this.Speed = new JTextField(/*"18"*/"250", 10);

        /*----Initialisation des Label----*/
        this.DataPOI = new JLabel("  POI total:  " + Calc.getPOI(), 10);
        this.DataDist = new JLabel("  Km total:  " + Calc.getDistance() + " Km", 10);
        this.LedConnect = new JLabel("          O", 10);
        this.LedTxt = new JLabel("Connected", 10);
        this.SpeedTxt = new JLabel("    Speed (km/h):", 10);
        this.ServTxt = new JLabel("        IP (ou URL) :", 10);
        this.PortTxt = new JLabel("               Port :", 10);
        this.Time = new JLabel(Calc.getTime(), 10);

        /*----Initialisation des container----*/
        this.Z1 = new JPanel();
        this.Z2 = new JPanel();
        this.Z3 = new JPanel();
        this.Z4 = new JPanel();
        this.Z5 = new JPanel();
        this.Z6 = new JPanel();

        this.ButonBar = new JPanel();
        this.Led = new JPanel();
        this.LineServ = new JPanel();
        this.LinePort = new JPanel();
        this.LineCon = new JPanel();

        this.Ong = new JPanel();

        /*----Chargement de la map OSM et redimensionnement du container----*/
        this.Map = new JMapViewer();
        Map.setPreferredSize(new Dimension(570, 400));
        
        Map.setDisplayPosition(new Coordinate(Latcenter,Loncenter),10);

        /*----Initialisation de la led de connection sur rouge----*/
        this.font = new Font("Arial", Font.BOLD, 20);
        LedConnect.setFont(font);
        LedConnect.setForeground(Color.RED);

        /*----Barre d'information sous la map----*/
        Z2.setLayout(new GridLayout(1, 2));
        Z2.add(DataPOI);
        Z2.add(DataDist);

        /*----Association Barred d'information et map OSM */
        Z1.setLayout(new BoxLayout(Z1, BoxLayout.PAGE_AXIS));
        Z1.add(Map);
        Z1.add(Z2);

        /*----Mise en place du menu de connexion----*/
        Led.setLayout(new GridLayout(1, 2));
        Led.add(LedConnect);
        Led.add(LedTxt);
        LineServ.setLayout(new GridLayout(1, 2));
        LineServ.add(ServTxt);
        LineServ.add(Serv);
        LinePort.setLayout(new GridLayout(1, 2));
        LinePort.add(PortTxt);
        LinePort.add(Port);
        LineCon.setLayout(new GridLayout(1, 2));
        LineCon.add(new JLabel("    ")); /*Label vide purement esthétique pour la mise en page du menu*/

        LineCon.add(Connect = new JButton("Gen. URL"));
        Connect.addActionListener(this);

        /*----Association des différentes parties du menu de connexion----*/
        Z4.setLayout(new BoxLayout(Z4, BoxLayout.PAGE_AXIS));
        Z4.add(new JLabel("    "));
        Z4.add(Led);
        Z4.add(new JLabel("    "));
        Z4.add(LineServ);
        Z4.add(LinePort);
        Z4.add(LineCon);
        Z4.add(new JLabel("    "));

        /*----Mise en place de la ligne de saisie de la vitesse----*/
        Z5.setLayout(new GridLayout(2, 2));
        Z5.add(SpeedTxt);
        Z5.add(Speed);
        Z5.add(new JLabel("    Estimated time : "));
        Z5.add(Time);

        /*----Mise en place des bouttons de commande pour la simulation*/
        ButonBar.setLayout(new GridLayout(1, 4));
        ButonBar.add(Start = new JButton("Start"));
        Start.addActionListener(this);
        ButonBar.add(Stop = new JButton("Stop"));
        Stop.addActionListener(this);
        ButonBar.add(Load = new JButton("Load"));
        Load.addActionListener(this);
        ButonBar.add(Reini = new JButton("Reini."));
        Reini.addActionListener(this);

        Z6.setLayout(new BoxLayout(Z6, BoxLayout.LINE_AXIS));

        /*----Association du menu complet----*/
        Z3.setLayout(new BoxLayout(Z3, BoxLayout.PAGE_AXIS));
        Z3.add(Z6);
        Z3.add(new JLabel("    "));
        Z3.add(ButonBar);
        Z3.add(new JLabel("    "));
        Z3.add(Z4);
        Z3.add(new JLabel("    "));
        Z3.add(new JLabel("    "));
        Z3.add(new JLabel("    "));
        Z3.add(new JLabel("    "));
        Z3.add(new JLabel("    "));
        Z3.add(Z5);
        Z3.add(new JLabel("    "));
        Z3.add(new JLabel("    "));

        /*----Association de la brique Map et de la brique Menu*/
        Ong.setLayout(new BoxLayout(Ong, BoxLayout.LINE_AXIS));
        Ong.add(Z1);
        Ong.add(Z3);

        Start.setEnabled(false);
        Stop.setEnabled(false);
        Load.setEnabled(false);
        Reini.setEnabled(false);
    }

    /**
     * return the Jpanel genrate by this class
     * @return Ong the JPanel with IHM drawn
     */
    JPanel IHM() {
        return Ong;
    }

    /**
    *
    * This class can draw Polyline and not just Polygon.
    * @author ???
    * @version 1.0
    */
    public static class MapPolyLine extends MapPolygonImpl {
        /**
         * Constructor who make an object polyline with a list of coordinate
         * @param points
         */
        public MapPolyLine(List<? extends ICoordinate> points) {
            super(null, null, points);
        }
        
        /**
         * Redefinition of MapPolygonImpl method
         * @param g
         * @param points
         */
        @Override
        public void paint(Graphics g, List<Point> points) {
            Graphics2D g2d = (Graphics2D) g.create();
            g2d.setColor(getColor());
            g2d.setStroke(getStroke());
            Path2D path = buildPath(points);
            g2d.draw(path);
            g2d.dispose();
        }
        
        /**
         * link the point but don't link Start with End 
         */
        private Path2D buildPath(List<Point> points) {
            Path2D path = new Path2D.Double();
            if (points != null && points.size() > 0) {
                Point firstPoint = points.get(0);
                path.moveTo(firstPoint.getX(), firstPoint.getY());
                for (Point p : points) {
                    path.lineTo(p.getX(), p.getY());
                }
            }
            return path;
        }
    }

    /*----programmation des listener----*/
    /**
     * Listeners of IHM
     * @param e all the event of press button
     */
    @Override
    public void actionPerformed(ActionEvent e) {

        if (e.getSource() == Connect) {
            System.out.println("Gen URL Pressed");
            CReq = new HTTPUse(Serv.getText(), Integer.valueOf(Port.getText()));
            LedConnect.setForeground(Color.green);
            Load.setEnabled(true);
        }
        if (e.getSource() == Start) {
            System.out.println("Start Pressed");
            Pos = new ThreadCalc(this.Map, Calc, route, IdTr, CReq);
            Start.setEnabled(false);
            Stop.setEnabled(true);
            Pos.start();
        }
        if (e.getSource() == Stop) {
            System.out.println("Stop Pressed");
            Pos.interrupt();
        }
        if (e.getSource() == Load) {
            int j;
            try {
                System.out.println("Load Pressed");
                IdTr = CReq.autofetch();
                System.out.println(IdTr);
                //IdTr = 1;
                if (IdTr != 0) {
                    KML = new File("Tr" + IdTr + ".kml");
                    //KML = new File("Tr32.kml");
                    FileWriter writer = new FileWriter((KML).getAbsoluteFile());
                    BufferedWriter bw = new BufferedWriter(writer);
                    bw.write("  ");
                    bw.close();
                    CReq.KMLsave(KML, IdTr);
                    
                    Start.setEnabled(true);
                    Stop.setEnabled(false);
                    Reini.setEnabled(true);
                    
                    KMLLoader KMLLoad = new KMLLoader();
                    route = KMLLoad.readXML(KML);
                    System.out.println("je vai print" + route);
                    Map.addMapPolygon(new MapPolyLine(route));
                    Calc = new Calcul(route, Speed.getText());
                    Speed.setEnabled(false);
                    DataPOI.setText("  POI total:  " + Calc.getPOI());
                    DataDist.setText("  Km total:  " + Calc.getDistance() + " Km");
                    Time.setText(Calc.getTime());
                    for (j = 0; j < route.size(); j++) {
                        this.Map.addMapMarker(new MapMarkerDot("POI" + j, route.get(j)));
                    }
                }
            } catch (IOException ex) {
                Logger.getLogger(OngDraw.class.getName()).log(Level.SEVERE, null, ex);
            } catch (JDOMException ex) {
                Logger.getLogger(OngDraw.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

        if (e.getSource() == Reini) {
            System.out.println("Stop Pressed");
            // faire le bordel de réinitailaisation de l'interface
            Start.setEnabled(false);
            Stop.setEnabled(false);
            Load.setEnabled(false);
            Reini.setEnabled(false);
            Connect.setEnabled(true);
            Speed.setEnabled(true);
            LedConnect.setForeground(Color.RED);
            Map.removeAllMapPolygons();
            Map.removeAllMapMarkers();
            Calc = new Calcul();
            DataPOI.setText("  POI total:  " + Calc.getPOI());
            DataDist.setText("  Km total:  " + Calc.getDistance() + " Km");
            Time.setText(Calc.getTime());
            Pos.interrupt();
        }
    }
}
