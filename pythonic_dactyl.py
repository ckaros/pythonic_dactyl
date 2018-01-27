from pykeeb import *
from math import *

#main plate
rows=5
columns=6

plate = Keyboard_matrix(5, 6, 0, 0, 3, [0,0,10], 0,15,0, 19,19)


#project rows and cols
plate.project_rows(90)
plate.project_cols(200)

plate.ik[0][0]=True


#translate columns y from projected positions to achieve a staggered column setup
plate.cm[1][1]=plate.cm[1][1]+2
plate.cm[2][1]=plate.cm[2][1]+4
plate.cm[3][1]=plate.cm[3][1]+3

#drop the middle columns z from projected positions to achieve a look similar to dactyl
plate.cm[2][2]=plate.cm[2][2]-8
plate.cm[3][2]=plate.cm[3][2]-4

plate.generate()


#thumb cluster
plate2 = Keyboard_matrix(3, 3, 0, 0, 10, [-20,-5.3,16], 0,15,0, 19,19)

plate2.ik[2][2]=True
plate2.ik[1][2]=True
plate2.ik[1][1]=True

#project rows and cols
plate2.project_rows(100)
plate2.project_cols(300)

#translate 2u thumb keys up half a space
plate2.im[0][2]=[0, 9.5, 0, 0, 0, 0]
plate2.im[0][1]=[0, 9.5, 0, 0, 0, 0]

plate2.generate()

#angle by which to rotate thumb cluster
thumbangle=18


#hulls connecting thumb and matrix
conn=project((plate2.sm[2][1].get_corner('fr', 2, 3, 2, 3).rotate(thumbangle)+plate.sm[2][0].get_corner('bl', 2, 3, 2, 3)).hull())
conn+=project((plate2.sm[0][2].get_corner('br', 2, 3, 2, 3).rotate(thumbangle)+plate.sm[0][1].get_corner('bl', 2, 3, 2, 3)).hull())
conn+=(plate2.sm[2][1].get_right().rotate(thumbangle)+plate.sm[1][0].get_left(0.01,0)).hull()
conn+=(plate2.sm[1][0].get_right().rotate(thumbangle)+plate2.sm[2][1].get_back().rotate(thumbangle)+plate2.sm[0][1].get_front().rotate(thumbangle)+plate2.sm[0][2].get_front().rotate(thumbangle)+plate.sm[0][1].get_left()+plate.sm[1][0].get_back()).hull()

plate2.right_wall[0].disable()
plate2.right_wall_hulls[0].disable()
plate2.front_right_corner.disable()
plate2.back_right_corner.disable()

plate.left_wall[1].disable()
plate.left_wall_hulls[0].disable()

#keys
keys=[]
for row in range(rows):
    for column in range(columns):
        if row+column>0:
            keys.append(plate.sm[row][column].get_keycap())

keys.append(plate2.sm[0][0].get_keycap().rotate(thumbangle))   
keys.append(plate2.sm[0][1].get_keycap().rotate(thumbangle))        
keys.append(plate2.sm[0][2].get_keycap().rotate(thumbangle))        
keys.append(plate2.sm[1][0].get_keycap().rotate(thumbangle))        
keys.append(plate2.sm[2][0].get_keycap().rotate(thumbangle))        
keys.append(plate2.sm[2][1].get_keycap().rotate(thumbangle))        

#hole for cable
cable_hole = Cylinder(30, 7, center=True).rotate([90,0,0])
cable_hole = (cable_hole + cable_hole.translate([10,0,0])).hull().translate([26,100,0]).color("Blue")

right_hand=plate.get_matrix()+plate2.get_matrix().rotate(thumbangle)+conn-cable_hole#+keys


(right_hand).write("things/pythonic_dactyl.scad")