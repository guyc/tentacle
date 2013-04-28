use <generated.scad>

small = 0.1;
ConnectorX = 7;
ConnectorY = 10;
ConnectorDX = 3;
ConnectorDY = 3;
ConnectorDZ = 3;

module ConnectorPositive()
{
  cube();        
}

module ConnectorNegative()
{
  translate([ConnectorX, ConnectorY, ConnectorDZ/2-small]) 
  {
    cube(size=[ConnectorDX,ConnectorDY,ConnectorDZ+small*2], center=true);
  }
  translate([-ConnectorX, ConnectorY, ConnectorDZ/2-small]) 
  {
    cube(size=[ConnectorDX,ConnectorDY,ConnectorDZ+small*2], center=true);
  }
}

difference()
{
  object();
  ConnectorNegative();
}
