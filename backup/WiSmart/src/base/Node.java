/*
Node.java:
Version: 0.1
dependencies:
Authors: Franco Minucci
emails: {name.surname}@esat.kuleuven.be
Base class for sensor nodes
*/

package base;
import java.util.*;

/**
 * Class representing the basic functionality of every embedded Wi-Fi module.
 * This model is based upon the functionality provided by the ESP 8266 Wi-Fi from Espressif
 * 
 * @author ingframin
 *
 */
public abstract class Node {
	/**
	 * Unique ID for every node, also used as Node Address
	 */
    Long ID;
    
    double batteryLevel;
    //this should not be here but in the World model
    double x,y;
    /**
     * This method models the energy usage by the node
     * @param charge amount of charge lost. It must be positive. If more than 100% the module dies.
     */
    public void dischargeBattery(double charge){
      if(batteryLevel>0.0 && charge >0.0 &&charge <100.0){
        batteryLevel -= charge;
      }
      if(batteryLevel<0.0){
        batteryLevel = 0;
      }

    }

    /**
     * This method models recharging the battery
     * @param charge amount of charge absorbed during the charge operation. It must be positive. Battery charge caps at 100%.
     */
    public void chargeBattery(double charge){
      if(batteryLevel<100.0 && charge <100.0 && charge > 0){
        batteryLevel += charge;
      }
      else if(batteryLevel > 100.0){
        batteryLevel = 100.0;
      }

    }

    public double getBatteryLevel() {
        return batteryLevel;
    }
    
    /**
     * This method forces the battery level setting
     * @param l
     * @throws Exception
     */

    public void setBatteryLevel(double l) throws Exception {
        if(l>0 && l<=100){
            batteryLevel = l;
        }
        else{
            throw new Exception("Battery level must be between 0 and 100");
        }
    }


    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Node node = (Node) o;
        return Objects.equals(ID, node.ID);
    }

    @Override
    public int hashCode() {

        return Objects.hash(ID);
    }

    //This function should not be here :-/
    //This must go into the World module
    public double distance(Node n){

        return Math.sqrt((x-n.x)*(x-n.x)+(y-n.y)*(y-n.y));
    }//distance

    public Long getID() {
        return ID;
    }
    
    //convoluted, packet object needed...
    public void sendPacket(Long receiverID,byte[] data){

    }

    public byte[] receivePacket(byte[] data){

        return data;
    }

    public Pair<Long,Double> calculateRSSI(Node n){
        double d = distance(n);
        double rssi = 100.0/d;
        return new Pair<Long,Double>(n.ID, rssi);
    }//calculate RSSI

}
