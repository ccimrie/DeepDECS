import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.animation as animation

waypoints=np.loadtxt('waypoints.txt')
pos_rbt=np.loadtxt('rbt_pos.txt')
pos_cldr=np.loadtxt('collider_pos.txt')
setup=np.loadtxt('setup.txt')
path=np.loadtxt('path.txt')
collisions=np.loadtxt('collisions.txt')

if len(np.shape(collisions))==1 and len(collisions)>0:
    collisions=np.reshape(collisions,(1,3))

objects=np.loadtxt('objects.txt')

fig, (ax_glb, ax_lc) = plt.subplots(1,2)

#add rectangle to plot
for i in objects:
    ax_glb.add_patch(Rectangle((i[0]-i[2], i[1]-i[3]), 2*i[2], 2*i[3], color=(0,0,0)))
    ax_lc.add_patch(Rectangle((i[0]-i[2], i[1]-i[3]), 2*i[2], 2*i[3], color=(0,0,0)))
ax_glb.set_xlim([-150,150])
ax_glb.set_ylim([-150,150])
ax_glb.set_aspect('equal')
ax_lc.set_aspect('equal')

s_non_path=15
s_path=60

ax_glb.scatter(waypoints[:,0],waypoints[:,1], s=s_non_path)
ax_glb.plot(np.append(setup[0,0],path[:,0]),np.append(setup[0,1],path[:,1]), zorder=-1)
ax_glb.scatter(path[:,0], path[:,1], s=s_path, c=[0.5, 0.5, 0.5], zorder=1)
ax_glb.scatter(setup[0,0],setup[0,1], s=s_path, c=[0.0, 0.7, 0.0], zorder=1)
ax_glb.scatter(setup[1,0],setup[1,1], s=s_path, c=[0.7, 0.0, 0.0], zorder=1)
ax_lc.scatter(waypoints[:,0],waypoints[:,1])
waystart=pos_rbt[0,2]
wayend=pos_rbt[0,3]

pos_start=[0,0]
pos_end=[0,0]
found=False
ind=0

r_radius=0.5

## Setting up robot for local view
rbt_lc=plt.Circle(pos_rbt[0,0:2], radius=r_radius, fc=np.array([0,0,1]), alpha=1.0)
rbt_lc=ax_lc.add_patch(rbt_lc)
rbt_angle=(pos_rbt[0,2]*np.pi/180.0)
rbt_lnx=(1.2*r_radius)*np.cos(pos_rbt[0,2]*np.pi/180.0)
rbt_lny=(1.2*r_radius)*np.sin(pos_rbt[0,2]*np.pi/180.0)

## Local line
rbt_ln,=ax_lc.plot([pos_rbt[0,0],pos_rbt[0,0]+rbt_lnx], [pos_rbt[0,1], pos_rbt[0,1]+rbt_lny], linewidth=2.0, c=[0,0,0])
## Global line
rbt_ln_glb,=ax_glb.plot([pos_rbt[0,0],pos_rbt[0,0]+rbt_lnx*10], [pos_rbt[0,1], pos_rbt[0,1]+rbt_lny*10], linewidth=4.0, c=[0,0,0])

cldr_lc=plt.Circle(pos_cldr[0,0:2], radius=r_radius, fc=np.array([1,0,0]), alpha=1.0)
cldr_lc=ax_lc.add_patch(cldr_lc)
cldr_angle=(pos_cldr[0,2]*np.pi/180.0)
cldr_lnx=(1.2*r_radius)*np.cos(pos_cldr[0,2]*np.pi/180.0)
cldr_lny=(1.2*r_radius)*np.sin(pos_cldr[0,2]*np.pi/180.0)
cldr_ln,=ax_lc.plot([pos_cldr[0,0],pos_cldr[0,0]+cldr_lnx], [pos_cldr[0,1], pos_cldr[0,1]+cldr_lny], linewidth=2.0, c=[0,0,0])

## Setting up robot for global view
rbt_glb=plt.Circle(pos_rbt[0,0:2], radius=r_radius*10, fc=np.array([0,0,1]), alpha=1.0)
rbt_glb=ax_glb.add_patch(rbt_glb)

lims=17.5
ax_lc.set_xlim([pos_rbt[0,0]-lims, pos_rbt[0,0]+lims])
ax_lc.set_ylim([pos_rbt[0,1]-lims, pos_rbt[0,1]+lims])

rbt_zoom_glb=plt.Rectangle(pos_rbt[0,0:2]-lims, 2*lims, 2*lims, ls='--', lw=1.5, fill=0)
ax_glb.add_patch(rbt_zoom_glb)

journey=0
coll_count=0;
t_avg=0

# speed=4
speed=20
# speed=100

TT=len(pos_rbt)

txt_t=plt.gcf().text(0.25, 0.05, 'Time: 0s\nAverage time: 0s', fontsize=18)
txt_c=plt.gcf().text(0.68, 0.1, 'Dangerous collisions: 0', fontsize=18)

def animate(t):
    global journey
    global coll_count
    global t_avg
    if t==0:
        plt.waitforbuttonpress()

    if len(collisions)>coll_count:
        if collisions[coll_count][2]<speed*t:
            ax_glb.scatter(collisions[coll_count,0],collisions[coll_count,1], 80, c=[0.95, 0.0, 0.0], marker='x')
            coll_count+=1

    rbt_lc.center=pos_rbt[speed*t,0],pos_rbt[speed*t,1]
    cldr_lc.center=pos_cldr[speed*t,0],pos_cldr[speed*t,1]

    ax_lc.set_xlim([pos_rbt[speed*t,0]-lims, pos_rbt[speed*t,0]+lims])
    ax_lc.set_ylim([pos_rbt[speed*t,1]-lims, pos_rbt[speed*t,1]+lims])

    pt_x=(1.2*r_radius)*np.cos(pos_rbt[speed*t,2]*np.pi/180.0)
    pt_y=(1.2*r_radius)*np.sin(pos_rbt[speed*t,2]*np.pi/180.0)
    rbt_ln.set_data([pos_rbt[speed*t,0], pos_rbt[speed*t,0]+pt_x], [pos_rbt[speed*t,1], pos_rbt[speed*t,1]+pt_y])

    rbt_glb.center=pos_rbt[speed*t,0],pos_rbt[speed*t,1]
    rbt_ln_glb.set_data([pos_rbt[speed*t,0], pos_rbt[speed*t,0]+pt_x*10], [pos_rbt[speed*t,1], pos_rbt[speed*t,1]+pt_y*10])

    pt_x=(1.2*r_radius)*np.cos(pos_cldr[speed*t,2]*np.pi/180.0)
    pt_y=(1.2*r_radius)*np.sin(pos_cldr[speed*t,2]*np.pi/180.0)
    cldr_ln.set_data([pos_cldr[speed*t,0], pos_cldr[speed*t,0]+pt_x], [pos_cldr[speed*t,1], pos_cldr[speed*t,1]+pt_y])

    rbt_zoom_glb.set_xy(pos_rbt[speed*t,0:2]-lims)

    rbt_glb.center=pos_rbt[speed*t,0],pos_rbt[speed*t,1]

    ## Check if passed waypoint
    dst=np.linalg.norm(path[journey,:]-pos_rbt[speed*t,0:2])
    journey_thresh=1.0
    if dst<journey_thresh:
        ax_glb.scatter(path[journey,0], path[journey,1], c=[0.0, 0.0, 0.8], s=s_path)
        journey+=1
        t_avg=(np.round((speed*t/60)/journey,2))

    if journey>0:
        txt_t.set_text('Time: '+str(np.round(speed*t/60))+'s\n'\
            +'Average time: '+str(t_avg)+'s')
    else:
        txt_t.set_text('Time: '+str(np.round(speed*t/60))+'s\n'\
            +'Average time: N.A.')
    txt_c.set_text('Dangerous collisions: '+str(coll_count))

line_ani = animation.FuncAnimation(fig, animate, frames=int(TT/speed), interval=16, blit=False, repeat=False)

plt.show()