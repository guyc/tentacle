include <generated.scad>

small = 0.1;
AlignHoleX = 12;
AlignHoleY = 16;
AlignHoleDX = 3;
AlignHoleDY = 3;
AlignHoleDZ = 4;

AlignPegX = AlignHoleX;
AlignPegY = AlignHoleY;
AlignPegDX = AlignHoleDX - 0.5;
AlignPegDY = AlignHoleDY - 0.5;
AlignPegDZ = AlignHoleDZ - 0.5;

module AlignPeg()
{
    translate([0,-ArcRadius,0]) {
      rotate(a=[ArcAngle,0,0]) {
        translate([0,ArcRadius,0]) {

  translate([AlignPegX, AlignPegY, AlignPegDZ/2]) 
  {
    cube(size=[AlignPegDX,AlignPegDY,AlignPegDZ], center=true);
  }
  translate([-AlignPegX, AlignPegY, AlignPegDZ/2]) 
  {
    cube(size=[AlignPegDX,AlignPegDY,AlignPegDZ], center=true);
  }
  
  }
}
}
}

module AlignHoleNegative()
{
  translate([AlignHoleX, AlignHoleY, AlignHoleDZ/2-small]) 
  {
    cube(size=[AlignHoleDX,AlignHoleDY,AlignHoleDZ+small], center=true);
  }
  translate([-AlignHoleX, AlignHoleY, AlignHoleDZ/2-small]) 
  {
    cube(size=[AlignHoleDX,AlignHoleDY,AlignHoleDZ+small], center=true);
  }
}

difference()
{
  object();
  AlignHoleNegative();
}
AlignPeg();

