import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

speed=int(sys.argv[1])

pos_rbt=np.loadtxt('rbt.txt')
pos_cldr=np.loadtxt('cldr.txt')
TT=len(pos_rbt)
# pos_rbt=np.reshape(np.loadtxt('rbt.txt'),[TT,3])
# pos_cldr=np.reshape(np.loadtxt('cldr.txt'),[TT,3])

fig=plt.figure()
ax_sim=fig.add_subplot(111)
ax_sim.set_xlim([-10, 10])
ax_sim.set_ylim([-1, 10])

ax_sim.set_aspect('equal')

r_radius=0.5
c_radius=0.5

rbt=plt.Circle(pos_rbt[0,0:2], radius=r_radius, fc=np.array([0,0,1]), alpha=1.0)
rbt=ax_sim.add_patch(rbt)

rbt_angle=(pos_rbt[0,2]*np.pi/180.0)
rbt_lnx=(pos_rbt[0,0]+1.2*r_radius)*np.cos(pos_rbt[0,2]*np.pi/180.0)
rbt_lny=(pos_rbt[0,0]+1.2*r_radius)*np.sin(pos_rbt[0,2]*np.pi/180.0)
rbt_ln,=ax_sim.plot([pos_rbt[0,0],rbt_lnx], [pos_rbt[0,1], rbt_lny], linewidth=2.0, c=[0,0,0])

cldr=plt.Circle(pos_cldr[0,0:2], radius=c_radius, fc=np.array([1,0,0]), alpha=1.0)
ax_sim.add_patch(cldr)
cldr_angle=(pos_cldr[0,2]*np.pi/180.0)
cldr_lnx=(1.2*c_radius)*np.cos(pos_cldr[0,2]*np.pi/180.0)
cldr_lny=(1.2*c_radius)*np.sin(pos_cldr[0,2]*np.pi/180.0)
cldr_ln,=ax_sim.plot([pos_cldr[0,0],pos_cldr[0,0]+cldr_lnx], [pos_cldr[0,1], pos_cldr[0,1]+cldr_lny], linewidth=2.0, c=[0,0,0])

def animate(t):
    if t==0:
        plt.waitforbuttonpress()
    if t*speed%100==0:
        print(t*speed)

    rbt.center=pos_rbt[speed*t,0],pos_rbt[speed*t,1]
    print(pos_rbt[t,0:2])

    pt_x=(1.2*r_radius)*np.cos(pos_rbt[speed*t,2]*np.pi/180.0)
    pt_y=(1.2*r_radius)*np.sin(pos_rbt[speed*t,2]*np.pi/180.0)
    rbt_ln.set_data([pos_rbt[speed*t,0], pos_rbt[speed*t,0]+pt_x], [pos_rbt[speed*t,1], pos_rbt[speed*t,1]+pt_y])
    
    cldr.center=pos_cldr[speed*t,0],pos_cldr[speed*t,1]
    pt_x=(1.2*c_radius)*np.cos(pos_cldr[speed*t,2]*np.pi/180.0)
    pt_y=(1.2*c_radius)*np.sin(pos_cldr[speed*t,2]*np.pi/180.0)
    cldr_ln.set_data([pos_cldr[speed*t,0], pos_cldr[speed*t,0]+pt_x], [pos_cldr[speed*t,1], pos_cldr[speed*t,1]+pt_y])

    # for i in np.arange(len(agents)):
    #     agents[i].center=pos[speed*t,i,0],pos[speed*t,i,1]
    #     # print du_min, du_max, pos[speed*t,i,2]
    #     c=(pos[speed*t,i,2]-du_min)/(du_max-du_min+0.001)
    #     agents[i].set_fc((0,c,c))
    # return rbt_ln,

line_ani = animation.FuncAnimation(fig, animate, frames=int(TT/speed), interval=5, blit=False, repeat=False)

plt.show()