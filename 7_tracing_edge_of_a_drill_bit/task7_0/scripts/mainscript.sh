#!/usr/bin/bash
source ../../../devel/setup.bash
echo "========================================================="
echo "==============Currently Running Setup===================="
echo "========================================================="
echo ""

echo ""
echo ""
echo -e "NS (no. of samples per rotation): \c"
read NS
echo ""
echo ""

echo ""
echo ""
echo -e "N (no. of rotations): \c"
read N
echo ""
echo ""

echo ""
echo ""
echo -e "Z offset (in mm): \c"
read z_o
echo ""
echo ""


echo ""
echo ""
echo -e "Diameter of Spherial Object (in mm): \c"
read D
echo ""
echo ""

echo ""
echo ""
echo -e "L (Length of Spindle in mm) : \c"
read L
echo ""
echo ""

echo ""
echo ""
echo -e "Diameter of Outer Shell (in mm): \c"
read D_O
echo ""
echo ""

R=$(bc <<< "scale=13;$D/2/1000")
echo $(bc <<< "$R * 1000")

Z_O=$(bc <<< "scale=13;$z_o / 1000")
C0=$(bc <<< "scale=13;$Z_O + $R")
echo $C0

R_O=$(bc <<< "scale=13;$D_O/2")

sed "s!sphere radius='0.05'!sphere radius='$R'!g" ../description/task6_0.urdf > ../description/temp0.urdf
sed "s!origin xyz='0 0 0.075'!origin xyz='0 0 $C0'!g" ../description/temp0.urdf > ../description/modified.urdf
rm ../description/temp0.urdf
./dataTransfer.py $NS $N $z_o $D $(bc <<< "scale=13;$D/2") $L $D_O $R_O

# echo ""
# echo "=======Asking for Planar Co-ordinates of Obstacle========"
# echo ""

# echo -e "The X of Obstacle : \c"
# read x_offset
# echo -e "The Y of obstacle : \c"
# read y_offset
# echo -e "The Shape of Obstacle : \c"
# read shape

# if [ $shape == "cylinder" ] ; then
#         echo "performing cylinder routine"
#         echo -e "The radius of Cylinder : \c"
#         read rad
#         echo -e "The length of Cylinder : \c"
#         read len
#         z_offset=$(bc <<< "scale=2;$len/2.0")
#         sed "s!cylinder radius='2.0' length='1.0'!cylinder radius='$rad' length='$len'!g" ../description/original.urdf > ../description/temp1.urdf
#         sed "s!1.0 1.0 0.25!$x_offset $y_offset $z_offset!g" ../description/temp1.urdf > ../description/modified.urdf
#         rm ../description/temp1.urdf
#         ./transfer_data.py $x1 $y1 $x2 $y2 $z $rad $len 0.0 $x_offset $y_offset
#         roslaunch collision_0 slider_gui.launch
        

# elif [ $shape == "box" ] ; then
#         echo "performing box routine"
#         echo -e "The Length  ( along x ) : \c"
#         read l_x
#         echo -e "The Breadth ( along y ) : \c"
#         read l_y
#         echo -e "The Height  ( along z ) : \c"
#         read l_z
#         z_offset=$(bc <<< "scale=2;$l_z/2.0")

#         sed "s!cylinder radius='2.0' length='1.0'!box size = '$l_x $l_y $l_z'!g" ../description/original.urdf > ../description/temp1.urdf
#         sed "s!1.0 1.0 0.25!$x_offset $y_offset $z_offset!g" ../description/temp1.urdf > ../description/modified.urdf


# else
#         echo "Not Valid : returning"
# fi