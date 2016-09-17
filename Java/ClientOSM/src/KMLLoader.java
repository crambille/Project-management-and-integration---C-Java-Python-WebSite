import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.jdom.Document;
import org.jdom.Element;
import org.jdom.JDOMException;
import org.jdom.input.SAXBuilder;
import org.jdom.xpath.XPath;
import org.openstreetmap.gui.jmapviewer.Coordinate;

/**
 *
 * This class can load a KML file parse him and extract data.
 * @author Anthony Borghi
 * @version 1.0
 */
public class KMLLoader {
    
    private boolean HT;
    private boolean Lat;
    private double pars;
    private double mem;
    private Coordinate Point;

    /**
     * Basic Constructor
     */
    KMLLoader() {
        this.HT = false;
        this.Lat = true;
    }
    
    /**
     * this method can parse a kml and return a list of coordinate who represent a ride
     * @param kmlFile KML file where are the datas of ride
     * @return route list of coordinate for draw a ride and calculate drone's position
     * @throws JDOMException Exception for DOM parsing of KML
     * @throws IOException Exception for IO File
     */
    public List readXML(File kmlFile) throws JDOMException, IOException {
        /*----Initialisation----*/
        SAXBuilder builder = new SAXBuilder();
        Document document = builder.build(kmlFile);
        List<Coordinate> route = new ArrayList<Coordinate>();
        String TMP = null;
        String Data = null;
        /*----Path for data's access----*/
        XPath Tr = XPath.newInstance("//k:kml/k:Document/k:Placemark/k:LineString/k:coordinates");        
        Tr.addNamespace("k", document.getRootElement().getNamespaceURI());
        Element node = (Element) Tr.selectSingleNode(document.getRootElement());
        TMP = node.getValue();
        /*----Parsing in double the coordinates to draw after----*/
        while(HT == false){
            if(TMP.contains(",")==true){
                if(Lat == true){
                    Data = TMP.substring(0, TMP.indexOf(','));
                    TMP = TMP.substring(TMP.indexOf(',')+1,TMP.length());
                    Lat = false;
                    pars = Double.parseDouble(Data);
                    mem = pars;
                }else{
                    Data = TMP.substring(0, TMP.indexOf(','));
                    TMP = TMP.substring(TMP.indexOf(',')+1,TMP.length());
                    Lat = true;
                    pars = Double.parseDouble(Data);
                    Point = new Coordinate(pars,mem);
                    route.add(Point);
                }
            }else{
                pars = Double.parseDouble(TMP);
                Point = new Coordinate(pars,mem);
                route.add(Point);
                HT = true;
            }
        }
        return route;
    }
}