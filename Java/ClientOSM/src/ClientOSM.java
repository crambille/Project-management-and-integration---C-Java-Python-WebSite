/**
 *
 * This class is the main Class.
 * @author Anthony
 * @version 1.0
 */
public class ClientOSM {

    /**
     * Main Class it's run on start of app
     * @param args the command line arguments
     */
    public static void main(String[] args) {
       Fenetre F = new Fenetre("Client Java OpenStreetMap");
       IHMdraw IHM1 = new IHMdraw(F);
       F.setVisible(true);
    }
    
}
