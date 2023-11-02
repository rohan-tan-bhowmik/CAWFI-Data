###FILE FOR CONVERTING METEOROLOGICAL AND ENVIRONMENTAL DATA FILES FROM THIS REPOSITORY INTO HEATMAPS###
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import datetime
import numpy as np
from scipy.interpolate import griddata
import cv2

display = False ###SET TO FALSE TO PREVENT SHOWING THE HEATMAP###

length = 1500 ##THE X AND Y SIZE OF THE FINAL HEATMAP, IN PIXELS###

###date IS THE DATE OF THE DATA FILE TO PROCESS, factor IS THE METEOROLOGICAL OR ENVIRONMENTAL FACTOR###
def getimg(date, factor):
    file = open("firedata/{0}-{1}.csv".format(date.strftime("%Y-%m-%d"), factor), "r") ###READ THE DATA FILE### ###CHANGE TO ROOT DIRECTORY OF DESIRED MET./ENV. FACTOR. KEEP {} FOR THE DATE###
    lines = file.readlines()[1:]
    latdata = []
    londata = []
    measure = []

    for line in lines:
        data = line.split(",")
        if len(data) < 3:
            continue
        if float(data[1]) > -128 and float(data[0]) < 52 and float(data[0]) > 25: ###GET LATITUDE, LONGITUDE, AND FACTOR DATA PER SENSOR###
            latdata.append(float(data[0]))
            londata.append(float(data[1]))
            measure.append(float(data[2]))

    THRESHOLD = 100000 ###THE HIGHEST ACCEPTED FACTOR DATA POINT, TO PREVENT FAULTY SENSOR READINGS###
    measure = [0 if float(i) < 0 else THRESHOLD if float(i) > THRESHOLD else float(i) for i in measure]

    londata = np.array(londata)
    latdata = np.array(latdata)
    measure = np.array(measure)
    idx = np.argsort(measure) ###SORT LATITUDE, LONGITUDE, AND FACTOR DATA TOGETHER IN ORDER ACCORDING TO THE FACTOR DATA###
    londata = londata[idx]
    latdata = latdata[idx]
    measure = measure[idx]

    ###CREATE AN INTERPOLATION MESH ACROSS CALIFORNIA'S MAXIMUM LONGITUDES AND LATITUDES (length BY length POINTS)###
    xmesh = np.linspace(-124.48201686,-114.13122248,length)
    ymesh = np.linspace(32.52883674, 42.00950827, length)
    xmesh, ymesh = np.meshgrid(xmesh, ymesh)
    interpolate = griddata((londata,latdata),measure,(xmesh,ymesh), method='linear') #method='cubic'#   ###PERFORM LINEAR/CUBIC INTERPOLATION WITH THE LONGITUDE, LATITUDE AND FACTOR DATA (DEFAULT = LINEAR)###

    interpolate = np.rot90(np.fliplr(interpolate),2)
    mask = plt.imread('wildfire-items/fill.png')[:,:,0] ###MASK CALIFORNIA'S LANDMASS AREA OVER THE INTERPOLATION TO REMOVE ANY POINTS OUTSIDE OF CALIFORNIA###
    mask = cv2.resize(mask, dsize=interpolate.shape, interpolation=cv2.INTER_CUBIC)
    interpolate = np.abs(np.nan_to_num(interpolate) * mask) + mask * 20 ###PERFORM SCALING TO INCREASE VISUAL CONTRAST BETWEEN AREAS OF HIGH/LOW/NO READINGS###

    ###SAVE IMAGE AND NUMPY ARRAYS OF THE HEATMAP###
    plt.imsave('img/{0}-{1}.png'.format(date.strftime("%Y-%m-%d"), factor), interpolate, cmap="gray", vmin=0, vmax=120) ###CHANGE TO ROOT DIRECTORY OF DESIRED MET./ENV. HEATMAPS. KEEP {0} FOR THE DATE AND {1} FOR THE FACTOR###
    
    file = open('npy/{0}-{1}.npy'.format(date.strftime("%Y-%m-%d"), factor), 'wb')                                      ###CHANGE TO ROOT DIRECTORY OF DESIRED MET./ENV. HEATMAPS. KEEP {0} FOR THE DATE AND {1} FOR THE FACTOR###
    np.save(file, np.nan_to_num(interpolate))

    if display:
        plt.imshow(interpolate, cmap='gray', vmin=0, vmax=120) ###SHOW THE HEATMAP###
        plt.show()

    file.close()
    print(date)

###EXAMPLE: GETS THE DEWPOINT (RELATIVE HUMIDITY) HEATMAP OVER CALIFORNIA FROM OCTOBER 24TH 2018###
getimg(datetime.datetime(2018,10,24), 'dewpoint')
