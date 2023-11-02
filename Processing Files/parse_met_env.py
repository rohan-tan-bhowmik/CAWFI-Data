###FILE FOR PARSING THE METEOROLOGICAL AND ENVIRONMENTAL DATA FILES FROM THIS REPOSITORY###
import datetime
import concurrent.futures

MAX_THREADS = 50
verbose = 0 ###SET TO 1 TO PRINT DEBUG/CHECKPOINTS###

lines = []
names = []  ###INCLUDE NAMES OF ALL FILES OF SIMILAR FACTOR TYPE TO PARSE###

for name in names:
    file = open("daily_TEMP/" + name) ###CHANGE TO ROOT DIRECTORY OF DESIRED MET./ENV. FACTOR###
    for line in file.readlines():
        lines.append(line)

print("begin")
cdate = datetime.datetime(2012,1,1)            ###SET TO EARLIEST DATE WITHIN DATA###
while cdate <= datetime.datetime(2022,12,31):  ###SET TO LATEST DATE WITHIN DATA###
    file = open("firedata/{}-temp.csv".format(cdate.strftime("%Y-%m-%d")), "w") ###CHANGE TO ROOT DIRECTORY OF DESIRED MET./ENV. FACTOR. KEEP {} FOR THE DATE###
    file.close()
    cdate += datetime.timedelta(days=1)

print("done")
i = 0

coords = []

def doit(line):
    choices = line.split(",")
    if "24" in choices[14]:
        file = open("firedata/{}-temp.csv".format(choices[11][1:-1]), "a") ###CHANGE TO ROOT DIRECTORY OF DESIRED MET./ENV. FACTOR. KEEP {} FOR THE DATE###
        file.write("{},{},{}\n".format(choices[5],choices[6],choices[16]))
        file.close()
        if (choices[5],choices[6]) not in coords:
            coords.append((choices[5],choices[6]))
            if verbose > 0:
                print((choices[5],choices[6]))
    if int(choices[11][1:-1].split("-")[2]) == 1 and verbose > 0:
        print(choices[11][1:-1])

print(coords)
threads = min(50, len(lines))

with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    executor.map(doit, lines)