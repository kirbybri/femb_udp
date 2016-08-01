import os
import importlib
import sys
import numpy as np
import time
from subprocess import call
import ROOT
config_type = os.environ["CONFIG_TYPE"]
mod = "femb_config_" + config_type
config = importlib.import_module(mod)
femb_config = config.FEMB_CONFIG()

serial_num = str(sys.argv[1])
date = str(sys.argv[2])

#files = ROOT.TList()

#d = 0 
#while d < 4:
#       filename = "/home/jack/workshop/femb_udp/slope_hists/slope_"+str(d)+".root"
#       f = ROOT.TFile(filename, "READ")
#       files.Add(f)

        #h = ROOT.hadd

        #OT.TFile(filename, "READ")
        #t = f.Get("slopes")
        #t.Draw("")

#       d += 1
#files.Print()
all_slopes = open("slope_hists/all_slopes.root", "w")
all_chi2 = open("chi2_hists/all_chi2.root", "w")
#hadd all_slopes.root files

call(['bash','hadd_script.sh', serial_num])
print "..."
c1 = ROOT.TCanvas()
f = ROOT.TFile("slope_hists/all_slopes.root", "READ")
t = f.Get("Slopes")
t.SetTitle("Slopes of 16 channels after multiple runs")
t.GetXaxis().SetTitle("Slope")
t.SetLineWidth(2)
t.Draw()
c2 = ROOT.TCanvas()
f1 = ROOT.TFile("chi2_hists/all_chi2.root", "READ")
t1 = f1.Get("Chi2")
t1.SetTitle("Chi2 of linear fit for 16 channels after multiple runs")
t1.SetLineWidth(2)
t1.Draw()

time.sleep(5)

