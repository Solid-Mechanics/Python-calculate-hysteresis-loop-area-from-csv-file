import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#read csv data
data = np.genfromtxt('Test1.steps.tracking.csv', delimiter=',', skip_header=392,
    skip_footer=0, usecols=(1, 10, 11), names=['loopNum', 'strain', 'stress'])
dataNum = len(data['strain'])
loopEnergy = []

#compute loop energy every given number
j = 0
integ = 0.0
for i in range(dataNum - 1):
    if j >= 250:
        j = 0
        loopEnergy.append(integ)
        integ = 0.0
    j = j + 1
    integ = integ + (data['stress'][i] + data['stress'][i+1]) / 2 * (data['strain'][i+1]
            - data['strain'][i]) / 100
loopEnergy.append(integ)

#compute loop energy by loopNum
#k = 1
#integ = 0.0
#for i in range(dataNum - 1):
#    if data['loopNum'][i] == k+1:
#        k = k + 1
#        loopEnergy.append(integ)
#        integ = 0.0
#    integ = integ + (data['stress'][i] + data['stress'][i+1]) / 2 * (data['strain'][i+1]
#            - data['strain'][i]) / 100
#loopEnergy.append(integ)

#compute loop energy by loop increment column 2 in csv
#integ = 0.0
#for i in range(dataNum - 1):
#    if data['loopNum'][i] == 125:
#        loopEnergy.append(integ)
#        integ = 0.0
#    integ = integ + (data['stress'][i] + data['stress'][i+1]) / 2 * (data['strain'][i+1]
#            - data['strain'][i]) / 100
#loopEnergy.append(integ)

#write out loop number and loop energy to a csv file
loop = [i+1 for i in range(len(loopEnergy))]
rows = zip(loop, loopEnergy)
c = csv.writer(open("loopEnergy.csv", "wb"))
c.writerow(["loop", "energy"])
for row in rows:
    c.writerow(row)

#generate a figure in pdf
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111)
ax.plot(loop[1:-1], loopEnergy[1:-1], '.-', markeredgewidth=0.4, markeredgecolor = 'none',
        linewidth = 0.4, color='r' )

plt.xlabel(r'loop', fontsize= 'large')
plt.ylabel(r'loopEnergy', fontsize= 'large')
plt.grid(False)
pp = PdfPages('loopEnergy.pdf')
pp.savefig(bbox_inches='tight')
pp.close()
