// arc is defined by the inner radius 

small = 1;
large = 1000;
//$fs = 5;
$fa = 2.5;

segmentInnerRadius = 300;
segmentArc = 10; // degrees

segmentWidth = 40;
segmentDepth = 20;
bulgeRadius  = 60;
segmentOuterRadius = segmentInnerRadius+segmentDepth;

tunnelInset =  8;
tunnelRadius = 4;

rimDepth = 5.0;
rimWidth = segmentWidth;
rimInnerRadius = segmentInnerRadius - rimDepth;

trackInnerRadius = segmentInnerRadius + 0;
trackDepth = 1.5;
trackWidth = 14.5;
trackOverhang = 1.0;
trackOverhangDepth = 1.0;

diffuserInnerRadius = rimInnerRadius + 1.2;
diffuserDepth = 1.0;
diffuserWidth = 25;
diffuserOverhang = 2.0;

innerRadius = rimInnerRadius;


module rim(innerRadius,width,depth)
{
  difference()
  {
    cylinder(r=innerRadius+depth, h=width, center=true);
    cylinder(r=innerRadius, h=width+small, center=true);
  }
}


module segment()
{
  translate([0,-segmentInnerRadius,0])
  {
    rotate(a=[0,90,0])
    {
      difference()
      {
        intersection() 
        {
          envelope();
          bulgeEnvelope();
        }
        cylinder(r=innerRadius, h=large, center=true);
        torus(segmentInnerRadius+tunnelInset, tunnelRadius);
        trackNegative();
      }
    }
  }
}

// r1 is donut radius, r2 is crosssectional radius
module torus(r1, r2)
{
  rotate_extrude(convexity = 10)
  {
    translate([r1, 0, 0]) 
    {
      circle(r = r2);
    }
  }
}

module tunnel()
{
  rotate(a=[0,90,0])
  {
    torus(segmentInnerRadius+tunnelInset, tunnelRadius);
  }
}

module bulgeEnvelope()
{
  ax = segmentWidth/2;
  ay = 0;
  bx = 0;
  by = segmentDepth;
  dab = sqrt(ax*ax+by*by);
  angleab = atan(by/ax);
  angleabc = acos(dab/2/bulgeRadius);
  angleac = angleabc - angleab;
  cx = ax - bulgeRadius * cos(angleac);
  cy = ay - bulgeRadius * sin(angleac);

    intersection() 
    {
      translate([0,0,-cx]) torus(segmentInnerRadius+cy,bulgeRadius);
      translate([0,0,+cx]) torus(segmentInnerRadius+cy,bulgeRadius);
    }
}


module trackPositive()
{
  rim(rimInnerRadius, rimWidth, rimDepth);
}

// parts that need to be excised
module trackNegative()
{
  rim(trackInnerRadius, trackWidth, trackDepth);
  rim(innerRadius, trackWidth-trackOverhang*2, trackInnerRadius-innerRadius+small);
  rim(diffuserInnerRadius, diffuserWidth, diffuserDepth);
  rim(innerRadius, diffuserWidth-diffuserOverhang*2, trackInnerRadius-innerRadius-trackOverhangDepth);
}

module track()
{
  rotate(a=[0,90,0])
  {
    difference()
    {
      rim(segmentInnerRadius-trackThickness, segmentWidth, trackThickness);  // outer body
      rim(segmentInnerRadius-trackThickness+trackClipDepth, trackWidth, trackClipDepth);
      cylinder(r=segmentInnerRadius-trackThickness+trackDepth, h=trackClipWidth, center=true);
    }
  }
}

module envelope()
{
  top = segmentOuterRadius * tan(segmentArc);

  rotate(a=[0,-90,0])
  polyhedron(
    points =
      [
        [-segmentWidth,0,0],
        [-segmentWidth,segmentOuterRadius+small,0],
        [-segmentWidth,segmentOuterRadius+small,top],

        [+segmentWidth,0,0],
        [+segmentWidth,segmentOuterRadius+small,0],
        [+segmentWidth,segmentOuterRadius+small,top],

      ],
    triangles = 
      [
        [0,1,2],
        [3,5,4],
        [0,2,5,3],
        [1,0,3,4],
        [1,4,5,2]
      ]
  );
}


segment();
