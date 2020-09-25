import mhkit 

import netCDF4
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib import pylab

stn = '067'
year_date = '2011'

[data, buoytitle] = mhkit.wave.io.cdip.request_data(stn,'','',year_date)
data.head()

# mhkit.wave.graphics.plot_boxplot(data, buoytitle)

########################################################################
# Boxplot Exampe
########################################################################

# Create array of month numbers to cycle through to grab Hs data
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
         
# Create array of month-long chunks of Hs data, to be plotted as a series of 
# boxplots. Use a for-loop to cycle through the Hs variable and define 
# each month-long array using the above-specified time index numbers.
# Calculate the monthly mean (average) using each month-long chunk of data.
# Calculate the number of instances of the variable being incorporated 
# into each month-long average
box_data=[]
means=[]
monthlengths=[]
for imonth in range(len(data.index.month.unique())):
    tmp1 = data[data.index.month == imonth+1]
    tmp2 = data[data.index.month == imonth+1].mean()
    tmp3 = len(data[data.index.month == imonth+1])

    box_data.append(tmp1)
    means.append(tmp2)
    monthlengths.append(tmp3)
means = np.array(means)
meansround = means.round(2)

Jan = box_data[0].Hs
Feb = box_data[1].Hs
Mar = box_data[2].Hs
Apr = box_data[3].Hs
May = box_data[4].Hs
Jun = box_data[6].Hs
Jul = box_data[6].Hs
Aug = box_data[7].Hs
Sep = box_data[8].Hs
Oct = box_data[9].Hs
Nov = box_data[10].Hs
Dec = box_data[11].Hs

#########################
# Plot data Boxplot
#########################

# Create overall figure and specify size, and grid to specify positions of subplots
fig = plt.figure(figsize=(12,15)) 
gs = gridspec.GridSpec(2,2,height_ratios=[5,1]) 

# Create a dataset for sample 'legend' boxplot, to go underneath actual boxplot
bp_sample2 = np.random.normal(2.5,0.5,500)

# Create two subplots - actual monthly-averaged data (top) and example 'legend' boxplot (bottom)
# Subplot of monthly-averaged boxplot data
bp = plt.subplot(gs[0,:])
# bp_data = bp.boxplot(box_data) # Add 'meanlineprops' to include the above-defined properties
bp_data =bp.boxplot([Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct])  
bp.scatter(months,means,marker="_",color='g',linewidths=2.5,s=900) # Overlay monthly means as green lines using 'scatter' function.

# Subplot to show example 'legend' boxplot below actual monthly-averaged boxplot graph
bp2 = plt.subplot(gs[1,:])
bp2_example = bp2.boxplot(bp_sample2,vert=False) # Plot horizontal example boxplot with labels
bp2.scatter(2.3,1,marker="|",color='g',linewidths=2.5,s=400)


# Add values of monthly means as text
for i, txt in enumerate(meansround):
    bp.annotate(txt, (months[i],means[i]),fontsize=12,horizontalalignment='center',verticalalignment='bottom',color='g')
    
# Get positions of Median, Quartiles and Outliers to use in 'legend' text labels 
for line in bp2_example['medians']:
    xm, ym = line.get_xydata()[0] # location of Median line   
for line in bp2_example['boxes']:
    xb, yb = line.get_xydata()[0] # location of Box edges (Quartiles)
for line in bp2_example['whiskers']:
    xw, yw = line.get_xydata()[0] # location of Whisker ends (Outliers)    

# Add text labels for 'Median', Mean', '25th/75th %iles' and 'Outliers' to subplot2, to create sample 'legend' boxplot
bp2.annotate("Median",[xm,ym-0.3*ym],fontsize=14,color='r')
bp2.annotate("Mean",[2.2,0.65],fontsize=14,color='g')
bp2.annotate("25%ile",[xb-0.01*xb,yb-0.15*yb],fontsize=12)
bp2.annotate("75%ile",[xb+0.2*xb,yb-0.15*yb],fontsize=12)
bp2.annotate("Outliers",[xw+0.38*xw,yw-0.3*yw],fontsize=14,color='r')

# Set colors of box aspects for top subplot    
pylab.setp(bp_data['boxes'], color='black')
pylab.setp(bp_data['whiskers'], color='black')
pylab.setp(bp_data['fliers'], color='r')

# Set colors of box aspects for bottom (sample) subplot   
pylab.setp(bp2_example['boxes'], color='black')
pylab.setp(bp2_example['whiskers'], color='black')
pylab.setp(bp2_example['fliers'], color='r')

# Set Titles
plt.suptitle(buoytitle, fontsize=30, y=0.97) # Overall plot title using 'buoytitle' variable
bp.set_title("Significant Wave Height by month for " + year_date, fontsize=20, y=1.01) # Subtitle for top plot
bp2.set_title("Sample Boxplot", fontsize=16, y=1.02) # Subtitle for bottom plot

# Set axes labels and ticks
bp.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],fontsize=12)
bp.set_ylabel('Significant Wave Height, Hs (m)', fontsize=20)
bp.tick_params(axis='y', which='major', labelsize=12, right='off')
bp.tick_params(axis='x', which='major', labelsize=12, top='off')

# Create a second row of x-axis labels for top subplot
newax = bp.twiny()
newax.xaxis.set_ticks_position('bottom')
newax.xaxis.set_label_position('bottom')
newax.spines['bottom'].set_position(('outward',25))
newax.set_xticklabels(monthlengths,fontsize=10)

# Plot horizontal gridlines onto top subplot
bp.grid(axis='y', which='major', color='b', linestyle='-', alpha=0.25)

# Remove tickmarks from bottom subplot
bp2.axes.get_xaxis().set_visible(False)
bp2.axes.get_yaxis().set_visible(False)




########################################################################
# Compendium Exampe
########################################################################

#########################
# Historic data
#########################
# stn = '100'
# start_date = "04/01/2012" # MM/DD/YYYY
# end_date = "04/30/2012"

# stn = '179'
# start_date = "04/01/2019" # MM/DD/YYYY
# end_date = "04/30/2019"

# stn = '187'
# start_date = "08/01/2018" # MM/DD/YYYY
# end_date = "08/31/2018"

# stn = '213'
# start_date = "08/01/2018" # MM/DD/YYYY
# end_date = "08/31/2018"

# [data, buoytitle] = mhkit.wave.io.cdip.request_data(stn,start_date,end_date,'')
# data.head()

#########################
# Realtime data
#########################
# stn = '187'
# start_date = "05/01/2020" # MM/DD/YYYY
# end_date = "05/31/2020"

# [data, buoytitle] = mhkit.wave.io.cdip.request_data(stn,start_date,end_date,data_type='Realtime')
# data.head()

#########################
# Plot data Compendium
#########################
# mhkit.wave.graphics.plot_compendium(data, buoytitle)


