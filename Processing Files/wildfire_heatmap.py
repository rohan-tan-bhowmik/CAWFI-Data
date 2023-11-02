import numpy as np
import datetime
import matplotlib.pyplot as plt

display = False ###SET TO FALSE TO PREVENT SHOWING THE HEATMAP###

cdate = datetime.datetime(2012,1,1)           ###SET TO EARLIEST DATE WITHIN DATA###
length = 1500                                 ##THE X AND Y SIZE OF THE FINAL HEATMAP, IN PIXELS###
dates = []

allsizes = []
while cdate <= datetime.datetime(2018,12,31): ###SET TO LATEST DATE WITHIN DATA###
    dates.append(cdate)
    cdate += datetime.timedelta(days=1)
    ###FOR EACH DAY...###
    try:
        ###READ ALL WILDFIRE ACTIVITY IN THE FORM OF ABNORMAL FRP READINGS###
        file = open("daily_wildfire/{}-locations.csv".format(cdate.strftime("%Y-%m-%d")), "r")
        for line in file.readlines():
            allsizes.append(float(line.split(",")[2]))
    except FileNotFoundError:
        pass

globalmax = np.asarray(allsizes).max() ###THE OVERALL LARGEST FRP READING###
globalmin = np.asarray(allsizes).min() ###THE OVERALL SMALLEST FRP READING (NOT USED)###

###date IS THE DATE OF THE DATA FILE TO PROCESS###
def getimg(date):
    try:
        file = open("daily_wildfire/{}-locations.csv".format(date.strftime("%Y-%m-%d")), "r") ###CHANGE TO ROOT DIRECTORY OF WILDFIRE DATA. KEEP {} FOR THE DATE###

        lonbounds = [-124.48201686, -114.13122248] ###THE LONGITUDE RANGE OF THE BOX CONTAINING CALIFORNIA###
        latbounds = [32.52883674, 42.00950827]     ###THE LATITUDE RANGE OF THE BOX CONTAINING CALIFORNIA###
        space = np.zeros((length,length))
        
        sizes = []
        lons = []
        lats = []
        for line in file.readlines(): ###GET THE LONGITUDE, LATITUDE, AND FRP READING FOR EACH INSTANCE OF WILDFIRE ACTIVITY ON date###
            split = line.split(",")
            lons.append(float(split[0]))
            lats.append(float(split[1]))
            sizes.append(float(split[2]))
        
        sizes = np.asarray(sizes)
        sizes = (sizes / globalmax) ** 0.25 ###RAISE TO THE FOURTH ROOT (CONVERTING POWER-LINEAR DATA TO TEMPERATURE-LINEAR DATA BY STEFAN-BOLTZMANN)###

        lons = np.asarray(lons)
        lats = np.asarray(lats)
        
        for i in range(sizes.shape[0]):
            ###SET lon, lat TO THE CORRESPONDING ROW AND COLUMN OF THE CENTER PIXEL OF THE WILDFIRE HEATMAP###
            lon = (int(length * (lons[i] - lonbounds[0]) / (lonbounds[1] - lonbounds[0])))
            lat = (int(length * (lats[i] - latbounds[0]) / (latbounds[1] - latbounds[0])))
            size = int(30 * sizes[i])
            if size >= 7: ###IF THE FRP ACTIVITY IS ABOVE SOME THRESHOLD IN POWER...###
                for i in range(-size,size):
                    for j in range(-int((size**2-i**2)**0.5),int((size**2-i**2)**0.5)): ###DRAW A CIRCLE (RADIUS SCALING WITH TEMPERATURE) ON THE MAP CENTERED AT lon, lat###
                        if 0 <= (lon + i) < length and 0 <= (lat + j) < length:
                            space[lon + i][lat + j] = 1

        plt.imsave('img/{}-wildfire.png'.format(date.strftime("%Y-%m-%d")), space, cmap="gray")                         ###CHANGE TO ROOT DIRECTORY OF WILDFIRE HEATMAPS. KEEP {} FOR THE DATE###
        file = open('npy/{}-wildfire.npy'.format(date.strftime("%Y-%m-%d")), 'wb') ###SAVE THE FILE AS A NUMPY ARRAY### ###CHANGE TO ROOT DIRECTORY OF WILDFIRE HEATMAPS. KEEP {} FOR THE DATE###

        if display:
            plt.imshow(space)
            plt.show()

        np.save(file, space)
        file.close()
    except FileNotFoundError:
        pass

    date += datetime.timedelta(days=1)

###EXAMPLE: GETS THE WILDFIRE HEATMAP OVER CALIFORNIA FROM OCTOBER 24TH 2018###
getimg(datetime.datetime(2018,10,24))
