rm slope_hists/all_slopes.root
hadd slope_hists/all_slopes.root slope_hists/slope_*"$1".root

rm chi2_hists/all_chi2.root
hadd chi2_hists/all_chi2.root chi2_hists/chi2_*"$1".root

