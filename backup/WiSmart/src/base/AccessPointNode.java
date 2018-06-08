/*
AccessPointNode.java:
Version: 1.0
dependencies:
Authors: Franco Minucci
emails: {name.surname}@esat.kuleuven.be
*/

package base;

import java.util.HashSet;


public class AccessPointNode extends Node implements AccessPoint {
    char ssid[];
    HashSet<StationNode> stations;

    public AccessPointNode(Long id, char[] ssid, double x, double y){
        this.ID = id;
        this.x = x;
        this.y = y;
        this.batteryLevel = 100.0;
        if(ssid.length > 32) {
            this.ssid = new char[32];
            System.arraycopy(ssid, 0, this.ssid, 0, 32);
            System.out.println("WARNING: SSID truncated to 32 characters");
        }
        else {
        	this.ssid = ssid;
        }
        
        stations = new HashSet<>();

    }

    /**constructs an AccessPoint from another Node
     * @param n The node that should become an AP
     * @param ssid A 32 char[] representing the SSID for the AP
     * WARNING:!! SSID longer than 32 characters are automatically truncated !! 
     * */
    public AccessPointNode(Node n, char[] ssid) {
      
        this.ID = n.ID;
        this.x = n.x;
        this.y = n.y;
        this.batteryLevel = n.batteryLevel;
        if(ssid.length > 32) {
            this.ssid = new char[32];
            System.arraycopy(ssid, 0, this.ssid, 0, 32);
            System.out.println("WARNING: SSID truncated to 32 characters");
        }
        else {
        	this.ssid = ssid;
        }
        stations = new HashSet<>();
    }

    public void associate(StationNode sn){
        stations.add(sn);
    }

    public void setSSID(char[] ssid){
    	if(ssid.length > 32) {
            this.ssid = new char[32];
            System.arraycopy(ssid, 0, this.ssid, 0, 32);
            System.out.println("WARNING: SSID truncated to 32 characters");
        }
        else {
        	this.ssid = ssid;
        }    }

    public char[] getSsid(){
        return ssid;
    }

    public void broadcast(String message){
        //method stub
    }

    @Override
    public String toString() {
        return "AccessPointNode{" +
                "ID=" + ID +
                ", ssid='" + String.copyValueOf(ssid) + '\'' +
                "Connected nodes= ["+stations+"]"+
                '}';
    }
}
