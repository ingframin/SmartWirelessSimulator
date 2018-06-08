/*
StationNode.java:
Version: 1.0
dependencies:
Authors: Franco Minucci
emails: {name.surname}@esat.kuleuven.be
*/
package base;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class StationNode extends Node implements Station{
    private Set<Pair<Long, Double>> visibleAccessPoints;
    private AccessPointNode associatedAP;
    SelectStrategy str;
    
    public StationNode(Long id, double x, double y) {
        this.ID = id;
        this.x = x;
        this.y = y;
        this.batteryLevel = 100.0;//velue in percentage
        this.visibleAccessPoints = new HashSet<>();
        associatedAP = null;
    }



    @Override
    public String toString() {
    	String ap = "";
    	if(associatedAP != null) {
    		ap = String.copyValueOf(associatedAP.ssid);
    	}
    	
        return "StationNode{" +
                "ID=" + ID +
                ", visibleAccessPoints=" + visibleAccessPoints +
                " batteryLevel=" + batteryLevel+"% "+
                "connected to=" + ap+
                "}";
    }

    public void scanNetworks(List<Node> networks){
        for(Node n:networks){
            if(n instanceof AccessPointNode){
                Pair<Long,Double> pair = calculateRSSI((AccessPointNode)n);
                if(pair.second > 1.0 ){
                    visibleAccessPoints.add(pair);
                }
            }

        }
    }//scanNetworks

    public void connect(AccessPointNode apn){
        apn.associate(this);
        this.associatedAP = apn;

    }
}
