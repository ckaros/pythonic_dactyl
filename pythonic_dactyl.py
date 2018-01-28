print('plates')
rows=5
columns=6
plate = Keyboard_matrix(5, 6, 0, 0, 1, [0,0,10], 0,15,0, 19,19)

plate.project_rows(90)
plate.project_cols(200)

plate.ik[0][0]=True

plate.cm[1][1]=plate.cm[1][1]+3
plate.cm[2][1]=plate.cm[2][1]+6
plate.cm[3][1]=plate.cm[3][1]+4
#plate.cm[4][1]=plate.cm[4][1]+1

plate.cm[2][2]=plate.cm[2][2]-6
plate.cm[3][2]=plate.cm[3][2]-3

plate.generate()


plate2 = Keyboard_matrix(3, 3, 0, 0, 10, [-20,8,16], 15,15,0, 19,19)

plate2.ik[2][2]=True
plate2.ik[1][2]=True
plate2.ik[1][1]=True

plate2.project_rows(80)
plate2.project_cols(250)

plate2.im[0][2][1]=plate2.im[0][2][1]+9.5
plate2.im[0][1][1]=plate2.im[0][1][1]+9.5


plate2.im[0][2][3]=plate2.im[0][2][3]+5
plate2.im[0][1][3]=plate2.im[0][1][3]+5

plate2.generate()

thumbangle=12

#hulls connecting thumb and matrix
print('plate hulls')
#hull 2u key to 1u keys around them
plate2.column_hulls[0][0].disable()
conn=(plate2.sm[1][0].get_right()+plate2.sm[0][1].get_left()).hull()
conn+=(plate2.sm[1][0].get_corner('fr', 2, 3, 2, 3)+plate2.sm[0][1].get_front()).hull()
conn+=(plate2.sm[2][1].get_back()+plate2.sm[0][1].get_front()).hull()

#extend 2u keys down to make border of cluster
conn+=(plate2.sm[0][1].get_back(0.01,extrude=9.5)+\
      plate2.sm[0][2].get_back(0.01,extrude=9.5)).hull()
#hull extensions to bottom left
conn+=(plate2.sm[0][1].get_corner('bl', 0,0,0.01, 9.5)+\
       plate2.sm[1][1].get_left()+\
       plate2.sm[0][0].get_right()).hull()
#rotate cluster
conn=conn.rotate(thumbangle)


#hull right 2u key to keywell
conn+=(plate2.sm[0][2].get_right().rotate(thumbangle)+\
       plate.sm[0][1].get_left()+\
       plate.sm[0][1].get_corner('bl',0,0,0.01,0.01)).hull()
#hull top right 1u key to keywell
conn+=(plate2.sm[2][1].get_right(extrude=2).rotate(thumbangle)+\
       plate.sm[1][0].get_left(0.01,0)+\
       plate.sm[2][0].get_corner('bl',0,0,0.01,0.01)).hull()

#hull middle of cluster to keywell
conn+=(plate2.sm[0][2].get_front().rotate(thumbangle)+\
       plate2.sm[2][1].get_corner('br', 2, 3, 2, 3).rotate(thumbangle)+\
       plate2.sm[0][1].get_corner('fr', 2, 3, 2, 3).rotate(thumbangle)+\
       plate.sm[1][0].get_back()).hull()




plate.left_wall[1].disable()
plate.left_wall_hulls[0].disable()
plate.corner_hulls[0][0].disable()

print('case hulls')

#hull front of cluster case to main case
#create front wall for cluster (needs elegant solution)
largefront=((plate2.sm[0][1].get_back(0.01,extrude=12.5)+\
         plate2.sm[0][2].get_back(0.01,extrude=12.5)).hull())
smallfront=((((plate2.sm[0][1].get_back(0.01,extrude=9.5)+\
         plate2.sm[0][2].get_back(0.01,extrude=9.5)+\
        (plate2.sm[0][1].get_back(0.01,extrude=-1)+\
         plate2.sm[0][2].get_back(0.01,extrude=-1))))).hull())#.scale([1.1,1.1,1.1]))

smallfront+=((((plate2.sm[0][1].get_back(0.01,extrude=9.5)+\
         plate2.sm[0][2].get_back(0.01,extrude=9.5)+\
        (plate2.sm[0][1].get_back(0.01,extrude=-1)+\
         plate2.sm[0][2].get_back(0.01,extrude=-1))))).hull()).translate([0,0,1])

smallfront+=((((plate2.sm[0][1].get_back(0.01,extrude=9.5)+\
         plate2.sm[0][2].get_back(0.01,extrude=9.5)+\
        (plate2.sm[0][1].get_back(0.01,extrude=-1)+\
         plate2.sm[0][2].get_back(0.01,extrude=-1))))).hull()).translate([0,0,-1])
smallfront+=((((plate2.sm[0][1].get_back(0.01,extrude=9.5)+\
         plate2.sm[0][2].get_back(0.01,extrude=9.5)+\
        (plate2.sm[0][1].get_back(0.01,extrude=-1)+\
         plate2.sm[0][2].get_back(0.01,extrude=-1))))).hull()).translate([-1,0,0])
smallfront+=((((plate2.sm[0][1].get_back(0.01,extrude=9.5)+\
         plate2.sm[0][2].get_back(0.01,extrude=9.5)+\
        (plate2.sm[0][1].get_back(0.01,extrude=-1)+\
         plate2.sm[0][2].get_back(0.01,extrude=-1))))).hull()).translate([1,0,0])

caconn=project((plate2.sm[0][0].get_corner('br',0,0,0.01,3)+(largefront-smallfront)).hull())



caconn=caconn.rotate(thumbangle)

caconn+=project((plate2.sm[2][1].get_corner('fr', 2, 3, 2, 3).rotate(thumbangle)+plate.sm[2][0].get_corner('bl', 2, 3, 2, 3)).hull())


caconn+=project((plate.sm[0][1].get_corner('bl', 0, 0, 0.01,0.01)+\
               plate2.sm[0][2].get_corner('br', 0, 0, 2, 3).rotate(thumbangle)+\
               plate2.sm[0][2].get_corner('br', 0, 0, 2, 12.5).rotate(thumbangle)).hull())   

plate2.right_wall[0].disable()
plate2.right_wall_hulls[0].disable()

plate2.front_right_corner.disable()
plate2.back_right_corner.disable()

plate2.back_wall[1].disable()
plate2.back_wall[2].disable()



plate2.back_wall_hulls[1].disable()
plate2.back_wall_hulls[0].disable()


plate2.right_wall_hulls[1].disable()


print('mounts')
for c in range(columns):
    for r in range(rows):
        if c==0 and r==0:
            mount=plate.sm[r][c].get_left(thickness=0.8,extrude=False).translate([0,0,-3])
        elif c==0 and r==1:
            None
        elif c==0:
            mount+=plate.sm[r][c].get_left(thickness=0.8,extrude=False).translate([0,0,-3])
        elif c==columns-1:
            mount+=plate.sm[r][c].get_right(thickness=0.8,extrude=False).translate([0,0,-3])
        if r==0:
            mount+=plate.sm[r][c].get_back(thickness=0.8,extrude=False).translate([0,0,-3])
        elif r==rows-1:
            mount+=plate.sm[r][c].get_front(thickness=0.8,extrude=False).translate([0,0,-3])
            
for c in range(3):
    for r in range(3):
        if c==0 and r==0:
            mount2=plate2.sm[r][c].get_left(thickness=0.8,extrude=False).rotate(thumbangle).translate([0,0,-3])
            mount2+=plate2.sm[r][c].get_back(thickness=0.8,extrude=False).rotate(thumbangle).translate([0,0,-3])
        elif c==0:
            mount2+=plate2.sm[r][c].get_left(thickness=0.8,extrude=False).rotate(thumbangle).translate([0,0,-3])
        elif c>0 and r==0:
            mount2+=plate2.sm[r][c].get_back(thickness=0.8,extrude=False).translate([0,-9.5,-3]).rotate(thumbangle)
            
        elif r==3-1:
            mount2+=plate2.sm[r][c].get_front(thickness=0.8,extrude=False).rotate(thumbangle).translate([0,0,-3])            

            
print('keys')
keys=[]
for row in range(rows):
    for column in range(columns):
        if row+column>0:
        #plate.sm[row][column].get_keyswitch()
            keys.append(plate.sm[row][column].get_keycap())

keys.append(plate2.sm[0][0].get_keycap().rotate(thumbangle))   
keys.append(plate2.sm[0][1].get_keycap().rotate(thumbangle))        
keys.append(plate2.sm[0][2].get_keycap().rotate(thumbangle))        
keys.append(plate2.sm[1][0].get_keycap().rotate(thumbangle))        
keys.append(plate2.sm[2][0].get_keycap().rotate(thumbangle))        
keys.append(plate2.sm[2][1].get_keycap().rotate(thumbangle))        

cable_hole = Cylinder(30, 7, center=True).rotate([90,0,0])
cable_hole = (cable_hole + cable_hole.translate([10,0,0])).hull().translate([26,100,0]).color("Blue")

print('unions')

right_hand=plate.get_matrix()+plate2.get_matrix().rotate(thumbangle)+conn+mount2+caconn
pl=plate2.get_plate().rotate(thumbangle)+plate.get_plate()+conn

ca=plate2.get_walls().rotate(thumbangle)+plate.get_walls()+mount2+caconn
    


print('writing')
(pl).write(r"\things\pythonic_dactyl_plate.scad")
(ca-pl).write(r"\things\pythonic_dactyl_case.scad")
(right_hand).write(r"\things\pythonic_dactyl.scad")

(pl.mirror([-1,0,0])).write(r"\things\pythonic_dactyl_plate_left.scad")
((ca-pl).mirror([-1,0,0])).write(r"\things\pythonic_dactyl_case_left.scad")