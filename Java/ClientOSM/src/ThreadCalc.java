import java.awt.Color;
import java.io.IOException;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.openstreetmap.gui.jmapviewer.Coordinate;
import org.openstreetmap.gui.jmapviewer.JMapViewer;
import org.openstreetmap.gui.jmapviewer.MapMarkerDot;

/**
 * This class can generate a thread tocalcul drone position  and send PUT request.
 * @author Anthony Borghi
 * @version 1.0
 */
public class ThreadCalc extends Thread{
    
    private JMapViewer Map;
    private Calcul Calc;
    private List<Coordinate> route;
    private MapMarkerDot Drone;
    private int id;
    private HTTPUse HTTP;
    
    /**
     * Basic constructor
     */
    ThreadCalc(){}
    
    /**
     * True Constructor
     * @param Map Map where the drone is drawn 
     * @param Calc All Calcul necessary to draw
     * @param L List of coordiante for the ride
     * @param i ID of autofetch
     * @param Crep HTTP use in OngDraw to sen PUT request to Server
     */
    ThreadCalc(JMapViewer Map, Calcul Calc, List L, int i, HTTPUse Crep){
        this.Map = Map;
        this.Calc = Calc;
        this.route = L;
        this.id = i;
        this.HTTP = Crep;
    }
    
    /**
     * Method who is execute when thread start
     */
    public void run(){
        double PTecoule;
        double PSegment;
        double PMemSeg;
        int j, i;
        double Segment = 0;
        double MemSeg = 0;
        double TEco;
        double TSec;
                    
        i = 0;

        System.out.println(i);
        Calc.StartTime();

        TEco = System.currentTimeMillis() - Calc.GetStartTime() ;
        TSec = Calc.getTimeSec()*60 ;
        PTecoule = 0;
        PMemSeg = 0;
        PSegment = 1;
        Drone = new MapMarkerDot("D1",route.get(0));
        Drone.setColor(Color.green);
        Drone.setBackColor(Color.green);
        Map.addMapMarker(Drone);
        Map.repaint();
        while(((System.currentTimeMillis() - Calc.GetStartTime())/1000 < TSec && i < Calc.getPOI())||((PTecoule-PMemSeg)/PSegment)<1){
            
            try {
                if(PTecoule > (MemSeg+Segment)/Calc.getDistance()){
                    i++;
                    //System.out.println("I'm in pause as Marseillais");
                    
                    System.out.println(TEco);
                    //Thread.sleep(30000);
                    //System.out.println("Pause terminated");
                }
                            //this.Map.repaint();
                PTecoule = TEco/TSec;
                MemSeg = 0;
                for(j = 0 ; j <= i ; j++){
                    Segment = Calc.CalcDist(route.get(j), route.get(j+1));
                    if(j < i) MemSeg = MemSeg + Segment;
                }
                PSegment = Segment / Calc.getDistance();
                PMemSeg = MemSeg / Calc.getDistance();
                TEco = ((System.currentTimeMillis() - Calc.GetStartTime()/*- (30000*i)*/)/1000) ;
                Thread.sleep(500);

                Map.removeMapMarker(Drone);
                Drone = new MapMarkerDot("D1",Calc.getCoorDrone(route.get(i), route.get(i+1), (PTecoule-PMemSeg)/PSegment));
                HTTP.putPos(Drone.getCoordinate(), this.id);
                Map.addMapMarker(Drone);
                /*Drone.setLat(Calc.getCoorDrone(route.get(i), route.get(i+1), (PTecoule-PMemSeg)/PSegment).getLat());
                Drone.setLon(Calc.getCoorDrone(route.get(i), route.get(i+1), (PTecoule-PMemSeg)/PSegment).getLon());
                */
                Drone.setColor(Color.green);
                Drone.setBackColor(Color.green);
                Map.repaint();
                
                

            } catch (InterruptedException ex) {   
                    Logger.getLogger(OngDraw.class.getName()).log(Level.SEVERE, null, ex);
            } catch (IOException ex) {
                Logger.getLogger(ThreadCalc.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        System.out.println("Work terminated");
    }
}
