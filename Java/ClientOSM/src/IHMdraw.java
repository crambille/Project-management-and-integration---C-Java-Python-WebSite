import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

/**
 *
 * This class can draw in window and manage TabbedPane with OngDraw return.
 * @author Anthony Borghi
 * @version 1.0
 */
public class IHMdraw{
    
    private    JTabbedPane Onglet;
    private    JButton Close;
    
    /**
     * Basic constructor
     */
    IHMdraw(){}

    /**
     * True Constructor
     * @param F The window create in main and put in the tabbedpane
     */
    IHMdraw(Fenetre F){
        JPanel TMP = new JPanel();
        
        /*----Initialisation barre d'onglet----*/       
        TMP.add(new OngDraw().IHM());
        this.Onglet = new JTabbedPane(JTabbedPane.TOP,JTabbedPane.SCROLL_TAB_LAYOUT);
        /*----Ajout du listener sur onglet pour l'ajout d'onglet----*/
        Onglet.addChangeListener(new ChangeListener() {
            public void stateChanged(ChangeEvent e) {
                System.out.println("Tab=" + Onglet.getSelectedIndex());
                if(Onglet.getTitleAt(Onglet.getSelectedIndex()).equals("+")){

                    Onglet.addTab("New Onglet",new OngDraw().IHM());
                    Onglet.remove(Onglet.getSelectedIndex());
                    Onglet.addTab("+",new JPanel());
                } 
            }
        });
        /*----Insertion de l'interface dans un onglet----*/
        Onglet.addTab("New Onglet",new OngDraw().IHM());
        Onglet.addTab("+",new JPanel());
        /*----Mise en place de la barre d'onglet dans la fenêtre----*/
        F.add(Onglet,BorderLayout.NORTH); 
    }    
}
