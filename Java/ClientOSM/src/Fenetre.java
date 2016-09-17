import javax.swing.JFrame;

/**
 *
 * This class can generate a window, size, and edit it, it's an extend of JFrame .
 * @author Anthony Borghi
 * @version 1.0
 */
public class Fenetre extends JFrame {
   /**
    * basic constructor
    */ 
   Fenetre(){}
   
   /**
    * True constructor with title
    * @param Titre the String who will be the window's title
    */
   Fenetre(String Titre){
        this.setTitle(Titre);
        this.setSize(850, 480);
        this.setLocationRelativeTo(null);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

}


}