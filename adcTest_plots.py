#!/usr/bin/env python33
import ROOT
from array import array
import sys
import time
from subprocess import call
import numpy as np

chi_list = []
slope_list = []


chan_num = 0
date = str(sys.argv[1])
#date = 11
serial_num = str(sys.argv[2])

volt_list = []
adc_list = []

while chan_num < 16:

    volt_list = []
    adc_list = []

    filenum = 0
    while filenum < 50:

        name = "data_adctest/output_adcTest_extPulser_DCscan_run_" + str(date) + "_subrun_" + str(filenum) + "_chan_num_" + str(chan_num) + "_asic_serial_num_" + serial_num + ".root"
        file = ROOT.TFile(name, "READ")
	if file.IsZombie():
		print "There is no data. Please check that the power supply is on."
		sys.exit()
        t = file.Get("femb_wfdata")
        t.Draw("wf>>hdum")
	#t.Draw()
        hwf = ROOT.gDirectory.FindObject("hdum")
        mean_tmp = hwf.GetMean()
	#mean_tmp = t.GetMean()
        print filenum, mean_tmp
        hwf.Delete()
        filenum += 1
        voltage = filenum*20
        volt_list.append(voltage)
        adc_list.append(mean_tmp)

    n = len(volt_list)
    volt_list = array('d', volt_list)
    adc_list = array('d', adc_list)

    answer = ROOT.TGraph(n, volt_list, adc_list)
    c1 = ROOT.TCanvas()
    answer.SetMarkerStyle(20)
    answer.SetTitle("ADC test analysis")
    answer.GetXaxis().SetTitle("Voltage")
    answer.GetYaxis().SetTitle("ADC value")
    answer.Fit("pol1","","",100,1020)
    f = answer.GetFunction("pol1")
    slope = f.GetParameter(1)
    ch2 = f.GetChisquare()
    #dof = f.GetNdf()
    #48 is the number of degrees of freedom
    x = ch2/48
    #slope = float(slope)
    #iprint type(slope)
    #print x
    slope_list.append(slope)
    chi_list.append(x)
    answer.Draw("A*")
    #c1.Close()
    #answer.SaveAs("plotzatt/Channel_" + str(chan_num) + "_" + str(date) + ".txt")
    #answer.savefig('Channel_' + chan_num + '.pdf')
    #raw_input()
    time.sleep(1)
    f.Delete()
    answer.Delete()
    #c1.Close()
    chan_num = chan_num + 1

#print slope_list
#print chi_list

c1 = ROOT.TCanvas()
h1 = ROOT.TH1F("Slopes","Slopes",100,1.30,1.40)
#h1 = Hist(16,0, 4.0)
#h1.fill_array(slope_list)

for i in range(0,16,1):
        h1.Fill(slope_list[i])
        print "Slope list", slope_list[i]
#h1.Fit()
h1.SetTitle("Histogram of slopes for all channels")
h1.GetXaxis().SetTitle("Slope")
h1.SetLineWidth(3)
h1.Draw()
h1.SaveAs("slope_hists/slope_"+str(date)+"_"+ serial_num +".root")
c1.Update()
time.sleep(2)

h2 = ROOT.TH1F("Chi2","Chi2",100,0,300)
for i in range(0,16,1):
        h2.Fill(chi_list[i])
        print "Chi squared", chi_list[i]
h2.SetTitle("Histogram of Chi squared for all channels")
h2.GetXaxis().SetTitle("Chi squared from linear fit")
h2.SetLineWidth(3)
h2.Draw()
h2.SaveAs("chi2_hists/chi2_"+str(date)+ "_"+serial_num +".root")
c1.Update()
time.sleep(2)

peak = h1.GetMean()


good_chi2 = 0
good_slope = 0
for i in range(0,16,1):
	#print i
	if (slope_list[i]>1.2 and slope_list[i]<1.4):
        	good_slope += 1
		#print good_slope
	if (chi_list[i]>1 and chi_list[i]<20):
		good_chi2 += 1
		#print good_chi2
		
if (good_slope == 16 and good_chi2 == 16):
	print "This ASIC is good."
        print "Peak is: ", str(peak)

else:
        	#for i in range(0,len(slope_list),1):
               		#print "Slope of channel", i, "is: ", points[i]
        print "This ASIC is bad."
        print "Peak is: ", str(peak)
        print "This is out of range for a good ASIC. The slopes and chi2 for each channel are:"
	print " Channel #: ",str(i), " Slope:", str(slope_list[i]), "Chi2:" ,str(chi_list[i])

		#else:
                	#for i in range(0,len(slope_list),1):
                       	#print "Slope of channel", i, "is: ", points[i]
                 #       print "This ASIC is bad."
                #        	print "Peak is: ", str(peak)
                #        	print "This is out of range for a good ASIC. The slopes and chi2 for each channel are: Channel #: ",str(i), " Slope:", str(slope_list[i]), "Chi2:" ,str(chi_list[i])




	#else:
        	#for i in range(0,len(slope_list),1):
        #        	#print "Slope of channel", i, "is: ", points[i]
        #        print "This ASIC is bad."
        #        	print "Peak is: ", str(peak)
        #        	print "This is out of range for a good ASIC. The slopes and chi2 for each channel are: Channel #: ",str(i), " Slope:", str(slope_list[i]), "Chi2:" ,str(chi_list[i])



