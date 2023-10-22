import glob

dirs = glob.iglob("*/*.csv")

for fname in dirs:
    print(fname)
    csv1 = fname.split(".")[0] + "_JanToJun.csv"
    csv2 = fname.split(".")[0] + "_JulToDec.csv"
    file = open(fname, 'r')
    file1 = open(csv1, 'w')
    file2 = open(csv2, 'w')
    lines = file.readlines()
    index = 0 if ("new" in fname and ("co" in fname or "no2" in fname or "pm10" in fname or "pm25" in fname)) else 11
    pos = 0 if ("new" in fname and ("co" in fname or "no2" in fname or "pm10" in fname or "pm25" in fname)) else 1
    splice = 1 if ("new" in fname and ("co" in fname or "no2" in fname or "pm10" in fname or "pm25" in fname)) else 0
    for line in lines[1:]:
        month = (int(line.split(",")[index].split("-")[pos][splice:]))
        if month <= 6:
            file1.write(line)
        else:
            file2.write(line)