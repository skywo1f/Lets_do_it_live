import numpy as np
import matplotlib.pyplot as plt
import magpylib as magpy


numSegments = 20

def createCoilMultiplex(idx,dxs,dys,deltaX,deltaY,topOrBot):
    # create a Magpylib collection of Loop Sources that form a coil
 #   coil = magpy.Collection()
    trajectory = []
    radius = 5
    firstPoint = 1
    for i in range(numSegments):        #loop over the segments getting created
    #    thisSegment = [radius*np.cos(2*np.pi*i/numSegments),radius*np.sin(2*np.pi*i/numSegments),z]
    #    trajectory.append(thisSegment)
        if (i == idx):
            x = 0.75*radius*np.sin(2*np.pi*i/numSegments) + dxs[i] + deltaX
            y = 0.75*radius*np.cos(2*np.pi*i/numSegments) + dys[i]  + deltaY
            if x > radius: x = radius
            if x < -radius: x = -radius
            if y > radius: y = radius
            if y < -radius: y = -radius
        else:
            x = 0.75*radius*np.sin(2*np.pi*i/numSegments) + dxs[i]
            y = 0.75*radius*np.cos(2*np.pi*i/numSegments) + dys[i]
            if x > radius: x = radius
            if x < -radius: x = -radius
            if y > radius: y = radius
            if y < -radius: y = -radius
        if topOrBot:
            z = -np.sqrt(radius*radius-x*x)
        else:
            z = np.sqrt(radius*radius-x*x)
        thisSegment = [x,y,z]
        trajectory.append(thisSegment)
        if firstPoint:
            fp = thisSegment
            firstPoint = 0
    trajectory.append(fp)
    coil = magpy.current.Line(1,trajectory)
    return coil

def showPlots(thisCoil,grid,amp,Bin):
    # create figure using Matplotlib
    fig = plt.figure(figsize=(8,4))
    ax1 = fig.add_subplot(121, projection='3d')  # 3D-axis
    ax2 = fig.add_subplot(122,)                  # 2D-axis
    # display the coil on ax1
    thisCoil.show(canvas=ax1)
    # display field in figure with matplotlib
    ax2.streamplot(grid[:,:,0], grid[:,:,2], Bin[:,:,0], Bin[:,:,2],
        density=2, color=np.log(amp), linewidth=1, cmap='autumn')

    plt.tight_layout()
    plt.show()

def findOffField(tB):
    totalOff = 0
    for i in range(tB.shape[0]):
        for j in range(tB.shape[1]):
            totalOff = totalOff + tB[i,j,0]*tB[i,j,0]
    return totalOff


if __name__ == "__main__":
    dxs = [0]*numSegments
#    dxs[0:5] = [3,3,3,3,3]
    dys = [0]*numSegments
    firstStep = 1
    finalOff = 999
    nOpts = 10
    delta = 0.2
    for opt in range(nOpts):            #loop over optimization steps
        for i in range(numSegments):    #loop over which segment gets moved
            finalOff = 999
            coil1 = createCoilMultiplex(i,dxs,dys,0,0,0) #create the two coils
            coil2 = createCoilMultiplex(i,dxs,dys,0,0,1)
            coll = magpy.Collection(coil1,coil2, style_label='coll')
            ts = np.linspace(-3,3,30)
            grid = np.array([[(x,0,z) for x in ts] for z in ts])
            tB = magpy.getB(coll,grid)
            tAmp =  np.linalg.norm(tB, axis=2)
            totalOff1 = findOffField(tB)
            if firstStep:
                firstStep = 0
                startOff = totalOff1
            if totalOff1 < finalOff :
                finalOff = totalOff1
                thisDelta = [0,0]
                finalColl = coll
                finalTAmp = tAmp
                finalTb = tB


            coil1 = createCoilMultiplex(i,dxs,dys,delta,0,0)
            coil2 = createCoilMultiplex(i,dxs,dys,delta,0,1)
            coll = magpy.Collection(coil1,coil2, style_label='coll')
            tB = magpy.getB(coll,grid)
            tAmp =  np.linalg.norm(tB, axis=2)
            totalOff2 = findOffField(tB)
            if totalOff2 < finalOff :
                finalOff = totalOff2
                thisDelta = [delta,0]
                finalColl = coll
                finalTAmp = tAmp
                finalTb = tB
            coil1 = createCoilMultiplex(i,dxs,dys,0,delta,0)
            coil2 = createCoilMultiplex(i,dxs,dys,0,delta,1)
            coll = magpy.Collection(coil1,coil2, style_label='coll')
            tB = magpy.getB(coll,grid)
            tAmp =  np.linalg.norm(tB, axis=2)
            totalOff3 = findOffField(tB)
            if totalOff3 < finalOff :
                finalOff = totalOff3
                thisDelta =  [0,delta]
                finalColl = coll
                finalTAmp = tAmp
                finalTb = tB

            coil1 = createCoilMultiplex(i,dxs,dys,-delta,0,0)
            coil2 = createCoilMultiplex(i,dxs,dys,-delta,0,1)
            coll = magpy.Collection(coil1,coil2, style_label='coll')
            tB = magpy.getB(coll,grid)
            tAmp =  np.linalg.norm(tB, axis=2)
            totalOff4 = findOffField(tB)
            if totalOff4 < finalOff :
                finalOff = totalOff4
                thisDelta =  [-delta,0]
                finalColl = coll
                finalTAmp = tAmp
                finalTb = tB

            coil1 = createCoilMultiplex(i,dxs,dys,0,-delta,0)
            coil2 = createCoilMultiplex(i,dxs,dys,0,-delta,1)
            coll = magpy.Collection(coil1,coil2, style_label='coll')
            tB = magpy.getB(coll,grid)
            tAmp =  np.linalg.norm(tB, axis=2)
            totalOff5 = findOffField(tB)
            if totalOff5 < finalOff :
                finalOff = totalOff5
                thisDelta =  [0,-delta]
                finalColl = coll
                finalTAmp = tAmp
                finalTb = tB

            dxs[i] = dxs[i] + thisDelta[0]
            dys[i] = dys[i] + thisDelta[1]
#            print(dxs,dys)

 #       print(finalOff)
    print(startOff)
    print(finalOff)

    showPlots(finalColl,grid,finalTAmp,finalTb)
