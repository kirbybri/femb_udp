import ROOT

c = ROOT.TCanvas("c", "Channel", 600, 600)

for g in range(4):
        for s in range(4):
                for b in range(2):
                        for i in range(128):
                                f = ROOT.TFile("output_femb_rootdata_"+str(g)+"_"+str(s)+"_"+str(b)+".root")
                                t = f.Get("femb_wfdata")
                                
                                t.Draw("wf","chan == "+str(i))

                                c.Modified()
                                c.Print("~/validation_plots/gain"+str(g)+"/shape"+str(s)+"/base"+str(b)+"/channel"+str(i)+".pdf","pdf")
