
/**
* <h1>WiFi_network_MAS</h1>
*
* Entry point for the simulation of smart_wireless.
* 
* @author  <a href="mailto:franco.minucci@esat.kuleuven.be">Franco Minucci</a>
* @version 1.0
* @since   09-04-2018
*/

import base.*;
import java.util.*;

/**
 * See license: <a href="./doc-files/License.txt">License.txt</a>
 * 
 * @author ingframin
 *
 */


public class WiFi_network_MAS {
	
	/**All the selectable strategies
	 */
	private enum Strategy{
		RANDOM,RSSI
	}
	
	/**This is the list of nodes used during the simulation          	 
	 */
	List<Node> nodes;
    
	/**
	 * Strategy to decide the access point:
	 * Random Selector = The AP gets chosen as a random node
     * RSSI Selector = The AP gets voted by the nodes depending on the RSSI; 
     * The AP with the highest amount of votes becomes the new access point.
	 * @param nodes the list of nodes on which the selection must be run
	 * @param str the chosen strategy
	 * @return AccessPointNode the chosen AP node
	 */
    private static AccessPointNode select(List<Node> nodes, Strategy str) {
    	
    	AccessPointNode ap = null;
    	switch(str){
    	case RANDOM:
    		RandomSelector rs = new RandomSelector();
            ap = rs.selectAP(nodes);
            break;
    	case RSSI:
    		RSSISelector rssis = new RSSISelector();
            ap = rssis.selectAP(nodes);
            
            break;
    	}//switch
    	
    	/*Substitutes the chosen ap in the list of nodes*/
    	for(Node n:nodes) {
        	if(n.getID()==ap.getID()) {
        		nodes.remove(n);
        		nodes.add(ap);
        		break;
        	}
        }
    	
    	return ap;
        
    }

    public static void main(String[] args){

        WiFi_network_MAS simulation = new WiFi_network_MAS();
        simulation.nodes = new ArrayList<>();
        for(int i=0;i<10;i++){
            simulation.nodes.add(new StationNode((long) i,i+Math.random()*100,i+Math.random()*100));
        }//for
        
        boolean running = true;
        AccessPointNode ap = null;
        while(running){

        	for(Node n:simulation.nodes) {
        		
        		if(ap != null && n instanceof StationNode) {
        			StationNode sn = (StationNode)n;
        			sn.scanNetworks(simulation.nodes);
        			sn.connect(ap);

        		}
        		if(n instanceof AccessPointNode) {
        			ap = (AccessPointNode)n;
        		}
        		System.out.println(n);
        		
        	}
        	//Perform access point selection if no access point is already present
            if(ap == null){
            	
               	ap = select(simulation.nodes,Strategy.RANDOM);
                
            }//if ()
            

          }//main loop

        }//main method

  }//class
