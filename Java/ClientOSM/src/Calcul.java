
import java.util.List;
import org.openstreetmap.gui.jmapviewer.Coordinate;

/**
 * This class can calculate distance, coordinate and more.
 *
 * @author Anthony Borghi
 * @version 1.0
 */
public class Calcul {

    private int Distance;
    private Coordinate Drone;
    private long TimeStart;
    private long TimeEstimate;
    private int NbPOI;
    private int Speed;
    private List<Coordinate> Transport;
    private boolean OnPOI;
    private Coordinate Dep = null;
    private Coordinate Arr = null;
    private int Segment;
    private int PSeg;
    private int TimeEcoul;
    private int TimeSeg;
    private int PTimeSeg;

    /**
     * Basic Constructor
     */
    public Calcul() {
        this.TimeStart = System.currentTimeMillis();
        this.NbPOI = 0;
        this.Distance = 0;
        this.OnPOI = false;
    }

    /**
     * True Constructor
     *
     * @param L a list of coordinate
     * @param Speed a string with speed data of IHM
     */
    public Calcul(List L, String Speed) {
        int i;
        this.Transport = L;
        this.Speed = Integer.parseInt(Speed);
        this.NbPOI = L.size();
        this.Distance = 0;
        //System.out.println(NbPOI);
        for (i = 0; i < L.size() - 1; i++) {
            Dep = (Coordinate) L.get(i);
            Arr = (Coordinate) L.get(i + 1);
            Distance = (int) (Distance + this.CalcDist(Dep, Arr));
        }
        this.TimeEstimate = (Distance * 60) / this.Speed;
        Drone = (Coordinate) L.get(0);
    }

    /**
     * Return the distance of a ride
     *
     * @return Distance value
     */
    public int getDistance() {
        return Distance;
    }

    /**
     * Return the number of POI on a ride
     *
     * @return NbPOI the number of POI on a ride
     */
    public int getPOI() {
        return NbPOI;
    }

    /**
     * Return a string with time at format Hours/minutes
     *
     * @return Time hour value and minute value
     */
    public String getTime() {
        int hour = (int) (TimeEstimate / 60);
        int min = (int) (TimeEstimate - hour * 60);
        return hour + " H " + min + "Min";
    }

    /**
     * Return the coordinates of a drone
     *
     * @return Drone Latitude and Longitude of the drone
     */
    public Coordinate getposDrone() {
        return Drone;
    }

    /**
     * keep the moment of simulation's start at now
     */
    public void StartTime() {
        this.TimeStart = System.currentTimeMillis();
    }

    /**
     * return the moment of start
     *
     * @return TimeStart Moment of start
     */
    public long GetStartTime() {
        return TimeStart;
    }

    /**
     * Calcul the distance between two points with their coordinates
     *
     * @param Dep Coordinate of start
     * @param Arr Coordinate of end
     * @return Distance between two points
     */
    public int CalcDist(Coordinate Dep, Coordinate Arr) {
        return (int) (6371 * Math.acos(Math.sin(Math.toRadians(Dep.getLat())) * Math.sin(Math.toRadians(Arr.getLat())) + Math.cos(Math.toRadians(Dep.getLat())) * Math.cos(Math.toRadians(Arr.getLat())) * Math.cos(Math.toRadians(Dep.getLon() - Arr.getLon()))));
    }

    /**
     * Return the estimated time to do all the ride
     *
     * @return TimeEstimate Estimated time value
     */
    public double getTimeSec() {
        return TimeEstimate;
    }

    /**
     * Return a coordinate of Drone with a scaling of ride's distance
     *
     * @param Dep Start of a segment
     * @param Arr End of a Segment
     * @param PSeg Ratio for the scaling on vector
     * @return D Coordinate of the drone [AB(End-Start) AD(AB*PSeg) D(AD+Start)]
     */
    public Coordinate getCoorDrone(Coordinate Dep, Coordinate Arr, double PSeg) {
        if (PSeg > 1) {
            PSeg = 1;
        }
        Coordinate AB = new Coordinate(Arr.getLat() - Dep.getLat(), Arr.getLon() - Dep.getLon());
        Coordinate AD = new Coordinate(AB.getLat() * PSeg, AB.getLon() * PSeg);
        Coordinate D = new Coordinate(AD.getLat() + Dep.getLat(), AD.getLon() + Dep.getLon());
        return D;
    }
}
