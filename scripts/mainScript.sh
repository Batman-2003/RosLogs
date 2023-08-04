#!/bin/bash
source ../../../devel/setup.bash
echo "========================================================="
echo "==============Currently Running Setup===================="
echo "========================================================="
echo ""
echo "==============Asking for 2 Points in a plane============="
echo ""
echo -e "x1 : \c"
read x1
if [ $(bc <<< "$x1==0.0") -eq 1 ] ; then
        x1=0.1
fi
        
echo -e "y1 : \c"
read y1
if [ $(bc <<< "$y1==0.0") -eq 1 ] ; then
        y1=0.1
fi

echo -e "x2 : \c"
read x2
if [ $(bc <<< "$x2==0.0") -eq 1 ] ; then
        x2=0.1
fi

echo -e "y2 : \c"
read y2
if [ $(bc <<< "$y2==0.0") -eq 1 ] ; then
        y2=0.1      
fi

echo ""
echo ""
echo "====Asking for Height of plane from Default position====="
echo ""

echo -e "relative height of plane from the arm : \c"
read z

echo ""
echo ""
echo "=======Asking for Planar Co-ordinates of Obstacle========"
echo ""

echo -e "The X of Obstacle : \c"
read x_offset
echo -e "The Y of obstacle : \c"
read y_offset
echo -e "The Shape of Obstacle : \c"
read shape

if [ $shape == "cylinder" ] ; then
        echo "performing cylinder routine"
        echo -e "The radius of Cylinder : \c"
        read rad
        echo -e "The length of Cylinder : \c"
        read len
        z_offset=$(bc <<< "scale=2;$len/2.0")
        sed "s!cylinder radius='2.0' length='1.0'!cylinder radius='$rad' length='$len'!g" ../description/original.urdf > ../description/temp1.urdf
        sed "s!1.0 1.0 0.25!$x_offset $y_offset $z_offset!g" ../description/temp1.urdf > ../description/modified.urdf
        rm ../description/temp1.urdf
        ./transfer_data.py $x1 $y1 $x2 $y2 $z $rad $len 0.0 $x_offset $y_offset
        roslaunch collision_0 slider_gui.launch
        

elif [ $shape == "box" ] ; then
        echo "performing box routine"
        echo -e "The Length  ( along x ) : \c"
        read l_x
        echo -e "The Breadth ( along y ) : \c"
        read l_y
        echo -e "The Height  ( along z ) : \c"
        read l_z
        z_offset=$(bc <<< "scale=2;$l_z/2.0")

        sed "s!cylinder radius='2.0' length='1.0'!box size = '$l_x $l_y $l_z'!g" ../description/original.urdf > ../description/temp1.urdf
        sed "s!1.0 1.0 0.25!$x_offset $y_offset $z_offset!g" ../description/temp1.urdf > ../description/modified.urdf


else
        echo "Not Valid : returning to last step"
fi
