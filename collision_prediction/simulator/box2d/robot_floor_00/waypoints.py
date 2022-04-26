import numpy as np
import matplotlib.pyplot as plt

sze=25
dist=10

waypoints=np.zeros([sze,sze,3])

waypoints[:,0,2]=-dist*((sze-1)/2.0);
waypoints[0,:,1]=-dist*((sze-1)/2.0);

for i in np.arange(1,sze):
    waypoints[:,i,2]=waypoints[:,i-1,2]+dist;
    waypoints[i,:,1]=waypoints[i-1,:,1]+dist;
cnt=0
for i in np.arange(sze):
    for j in np.arange(sze):
        waypoints[i,j,0]=cnt
        cnt+=1        
# cnt=0
with open('waypoints.txt', 'w') as f:
    for i in np.arange(sze):
        for j in np.arange(sze):
            v=waypoints[i,j,0]
            edges=[]
            if i==0:
                edges.append(waypoints[i+1,j,0])
            elif i==sze-1:
                edges.append(waypoints[i-1,j,0])
            else:
                edges.append(waypoints[i-1,j,0])
                edges.append(waypoints[i+1,j,0])

            if j==0:
                edges.append(waypoints[i,j+1,0])
            elif j==sze-1:
                edges.append(waypoints[i,j-1,0])
            else:
                edges.append(waypoints[i,j-1,0])
                edges.append(waypoints[i,j+1,0])

            line=str(int(v))+' '+str(waypoints[i,j,1])+' '+str(waypoints[i,j,2])
            for e in edges:
                line+=' '+str(int(e))
            # cnt+=1
            f.write(line+'\n')

# for i in np.arange(sze):
#   for j in np.arange(sze):
