package base;

public interface AccessPoint{
  //SSID must be shorter than 32 characters
  public void setSSID(char[] ssid) throws Exception;
  public void associate(StationNode sn);
  public char[] getSsid();
  public void broadcast(String message);

}
