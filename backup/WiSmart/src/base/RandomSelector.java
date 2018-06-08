package base;

import java.util.List;

/**
 * RandomSelector class
 * @author fminucci
 * 
 * 
 *
 */
public class RandomSelector implements SelectStrategy {

    @Override
    public AccessPointNode selectAP(List<Node> nodes) {

        long id = Math.round((nodes.size()-1)*Math.random());
        char ssid[] = Long.toString(id).toCharArray();
        for(Node n:nodes){

            if(n.getID() == id){
              AccessPointNode apn;
              try{
                if(ssid.length > 32){
                  char truncated [] = new char[32];
                  for(int i=0;i<32;i++){
                    truncated[i]=ssid[i];

                  }//for (; ; ) {
                  ssid = truncated;
                }
                apn = new AccessPointNode(n,ssid);
                return apn;
              }

              catch(Exception e){


              }//catch (Exception e) {

              }//if

            }//for
            return null;
      }//method
  }
