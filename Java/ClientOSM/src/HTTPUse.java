import java.io.*;
import java.net.*;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.openstreetmap.gui.jmapviewer.Coordinate;

/**
 *
 * This class can generate HTTP Request for Python Server.
 * @author Anthony Borghi
 * @version 1.0
 */
public class HTTPUse {

    private String ServIP;
    private int Port;
    private String URL;
    private String Validate;
    private String TMP;

    /**
     * basic constructor
     */
    HTTPUse() {
        this.Validate = "";
    }

    /**
     * true Constructor who generate the String URL "http://adresseIP:Port/"
     * @param ServIP IP adress from IHM
     * @param Port Port from IHM
     */
    HTTPUse(String ServIP, int Port) {
        this.ServIP = ServIP;
        this.Port = Port;
        this.URL = "http://" + ServIP + ":" + Port + "/";
        System.out.println("URL pour la requete : " + URL);
    }

    /**
     * Make autofetch request and return id of ride not simulated
     * @return Id value of ride not simulated or 0 if server send a 404 error
     */
    public int autofetch() {
        try {
            URL url;
            HttpURLConnection conn;
            String result = "";
            String line = null;

            url = new URL(URL + "transports/autofetch");
            System.out.println(url);
            System.out.println("URL pour la requete : " + url);
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            Validate = conn.getHeaderField(null);
            Validate = Validate.substring(9, 12);
            System.out.println(Validate);
            if (Validate.equals("404")) {
                return 0;
            }
            if (Validate.equals("200")) {
                BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));

                while ((line = in.readLine()) != null) {
                    result = result + line;
                }
                result = result.substring(result.indexOf(':') + 2, result.indexOf(','));
            }
            int Id = Integer.parseInt(result);
            return Id;
        } catch (MalformedURLException ex) {
            Logger.getLogger(HTTPUse.class.getName()).log(Level.SEVERE, null, ex);
        } catch (ProtocolException ex) {
            Logger.getLogger(HTTPUse.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(HTTPUse.class.getName()).log(Level.SEVERE, null, ex);
        }
        return 0;
    }

    /**
     * Make a request at server to save the KML with autofetch ID
     * @param KML File to save the result of server response
     * @param i id value to choice KML file
     */
    public void KMLsave(File KML, int i) {
        try {
            FileWriter writer;
            URL url;
            HttpURLConnection conn;
            BufferedReader rd;
            String line;
            String result = "";
            writer = new FileWriter((KML).getAbsoluteFile());
            url = new URL(URL + "transports/" + i /*1*/ + "/route");

            System.out.println("URL pour la requete : " + url);
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            Validate = conn.getHeaderField(null);
            Validate = Validate.substring(9, 12);

            rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            while ((line = rd.readLine()) != null) {
                result += line;
            }
            System.out.println(result);
            System.out.println("Validate");
            if (Validate.equals("200")) {
                BufferedWriter bw = new BufferedWriter(writer);
                bw.write(result);
                bw.close();
                System.out.println("Saved go verify");
            }
            rd.close();
            writer.close();

        } catch (IOException ex) {
            Logger.getLogger(HTTPUse.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    /**
     * Request PUT to give coordinate of the drone in JSON at server
     * @param Drone Coordinate to send 
     * @param i id of autofetch for generate URL
     * @throws IOException All IN OUT exception for KML file
     */
    public void putPos(Coordinate Drone, int i) throws IOException {
        URL url;
        HttpURLConnection conn;
        String result = "";
        url = new URL(URL + "transports/" + i);
        System.out.println("URL pour la requete : " + url);
        conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("PUT");
        conn.setDoOutput(true);
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setRequestProperty("Accept", "application/json");
        OutputStreamWriter osw = new OutputStreamWriter(conn.getOutputStream());
        result = "{\"drone_location\":{\"coord\": { \"lat\": " + Drone.getLat() + ",\"lon\": " + Drone.getLon() + "}}}";
        System.out.println(result);
        osw.write(result);
        osw.flush();
        System.out.println(conn.getResponseCode());
        osw.close();
    }
}
