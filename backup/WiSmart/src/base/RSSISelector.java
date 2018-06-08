package base;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

/**
 * This SelectorStrategy is based upon RSSI measurements.
 * All the nodes will try to connect to the AccessPointNode with the highest RSSI.
 * If no AP is present they will elect a new one depending on the RSSI.
 * Each node votes for the other node that it sees as the one with the highest RSSI.
 * In case two or more AP have the same amount of votes, the first one found is selected
 * RSSISelector does not require any special initialization and so only the default constructor is provided
 * @author fminucci
 * @version 1.0
 *
 */
public final class RSSISelector implements SelectStrategy{
	
    public AccessPointNode selectAP(List<Node> nodes){
    	double rssi = 0;
    	Pair<Long,Double> current;
    	AccessPointNode retNode = null;
    	List<Node> apns = nodes.stream().filter(n -> n instanceof AccessPointNode).collect(Collectors.toList());
    	List<Node> stations = nodes.stream().filter(n->n instanceof StationNode).collect(Collectors.toList());
    	
    	if(apns.size()>0) {
    		for(Node ref:stations) {
        		
        		for(Node n:apns) {
            		current = ref.calculateRSSI(n);
            		if(current.second>rssi) {
            			retNode = ((AccessPointNode) n);
            		}//if
            		
            	}//for loop
        	}//for loop
    	}
    	else {
    		/*If there is no AP defined, each node calculate the distance with the others
        	and votes for the closest one. The node with the highest amount of votes becomes the new AccessPoint*/
    		ArrayList<Long> votes = new ArrayList<Long>(nodes.size());
    		Long vid = null;
    		
    		/*This can be made more efficient by building a look-up table with the distances
    		 * or probably using the stream API
    		 * For the moment is O(n^2), I know it's horrbile but it works.*/
    		
    		for(Node ref:nodes) {
    			double minDistance = 0.0;
        		for(Node n: nodes) {
        			if(!n.equals(ref)) {
        				double d = ref.distance(n);
        				if(d < minDistance) {
        					minDistance = d;
        					vid = n.ID;
        				}//if
        			}//if
        		}//int for
        		votes.add(vid);
    		}//ext for
    		
    		int votesCount = 0;
    		
    		for(Long l:votes) {
    			if(Collections.frequency(votes, l) > votesCount) {
    				vid = l;
    				votesCount = Collections.frequency(votes, l);
    			}
    		}
    		for(Node n:nodes) {
    			if(n.getID()==vid) {
    				retNode = new AccessPointNode(n,Long.toString(n.getID()).toCharArray());
					
    				break;
    				
    			}
    		}

    	}
    	
    	
    	return retNode;
    }//method

}
    
