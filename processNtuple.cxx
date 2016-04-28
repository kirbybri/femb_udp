//compile independently with: g++ -std=c++11 -o processNtuple processNtuple.cxx `root-config --cflags --glibs`
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
using namespace std;

#include "TROOT.h"
#include "TMath.h"
#include "TApplication.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1.h"
#include "TH2.h"
#include "TString.h"
#include "TCanvas.h"
#include "TSystem.h"
#include "TGraph.h"
#include "TProfile2D.h"

using namespace std;

//global TApplication object declared here for simplicity
TApplication *theApp;

class Analyze {
	public:
	Analyze(std::string inputFileName);
	void doAnalysis();
	void analyzeChannel();

	//Files
	TFile* inputFile;
	TFile *gOut;

	//ROI tr_rawdata variables
	TTree *tr_rawdata;
	unsigned int chan, num;
	unsigned short wf[512];

	//metadata tree
	TTree *tr_metadata;
	TTree *tr_outmetadata;

	//Constants
	const int numChan = 128;// 35t

	//data objects
	TCanvas* c0;
	TGraph *gCh;

	//histograms
	TH2F *hSampVsChan;
	TProfile *pSampVsChan;
	TH2F *hMeanVsChan;
	TProfile *pMeanVsChan;
	TH2F *hRmsVsChan;
	TProfile *pRmsVsChan;
	TProfile *pFracStuckVsChan;
};

Analyze::Analyze(std::string inputFileName){

	//get input file
	if( inputFileName.empty() ){
		std::cout << "Error invalid file name" << std::endl;
		gSystem->Exit(0);
	}

	inputFile = new TFile(inputFileName.c_str());
	if (inputFile->IsZombie()) {
		std::cout << "Error opening input file" << std::endl;
		gSystem->Exit(0);
	}

	if( !inputFile ){
		std::cout << "Error opening input file" << std::endl;
		gSystem->Exit(0);
	}

	//initialize tr_rawdata branches
  	tr_rawdata = (TTree*) inputFile->Get("femb_wfdata");
  	if( !tr_rawdata ){
		std::cout << "Error opening input file tree" << std::endl;
		gSystem->Exit(0);
  	}
	tr_rawdata->SetBranchAddress("chan", &chan);
  	tr_rawdata->SetBranchAddress("num", &num);
  	tr_rawdata->SetBranchAddress("wf", &wf);

	//get metadata
	tr_metadata = (TTree*) inputFile->Get("metadata");
  	if( !tr_metadata ){
		std::cout << "Error opening input file tree" << std::endl;
		gSystem->Exit(0);
  	}
	//copy metadata tree
	tr_outmetadata = tr_metadata->CloneTree();

	//make output file
  	std::string outputFileName = "output_processNtuple_" + inputFileName;
  	gOut = new TFile(outputFileName.c_str() , "RECREATE");

  	//initialize canvas
  	c0 = new TCanvas("c0", "c0",1400,800);

	//initialize graphs
	gCh = new TGraph();

  	//output histograms, data objects
  	hSampVsChan = new TH2F("hSampVsChan","",numChan,0-0.5,numChan-0.5,4096,-0.5,4096-0.5);
 	pSampVsChan = new TProfile("pSampVsChan","",numChan,0-0.5,numChan-0.5);
  	hMeanVsChan = new TH2F("hMeanVsChan","",numChan,0-0.5,numChan-0.5,4096,-0.5,4096-0.5);
	pMeanVsChan = new TProfile("pMeanVsChan","",numChan,0-0.5,numChan-0.5);
  	hRmsVsChan = new TH2F("hRmsVsChan","",numChan,0-0.5,numChan-0.5,300,0,300.);
  	pRmsVsChan = new TProfile("pRmsVsChan","",numChan,0-0.5,numChan-0.5);
	pFracStuckVsChan = new TProfile("pFracStuckVsChan","",numChan,0-0.5,numChan-0.5);
}

void Analyze::doAnalysis(){
  	//loop over tr_rawdata entries
  	Long64_t nEntries(tr_rawdata->GetEntries());

	tr_rawdata->GetEntry(0);
	//loop over pulse waveform
	for(Long64_t entry(0); entry<nEntries; ++entry) { 
		tr_rawdata->GetEntry(entry);
		//analyze current entry - 1 channel
    		analyzeChannel();
  	}//entries

    	gOut->Cd("");
	tr_outmetadata->Write();
  	hSampVsChan->Write();
	pSampVsChan->Write();
  	hMeanVsChan->Write();
	pMeanVsChan->Write();
  	hRmsVsChan->Write();
  	pRmsVsChan->Write();
	pFracStuckVsChan->Write();
  	gOut->Close();
}

void Analyze::analyzeChannel(){

	 //skip known bad channels here

	//calculate mean
	double mean = 0;
	int count = 0;
	for( int s = 0 ; s < num ; s++ ){
		if(  wf[s] < 10 ) continue;
		if( (wf[s] & 0x3F ) == 0x0 || (wf[s] & 0x3F ) == 0x3F ) continue;
		double value = wf[s];
		mean += value;
		count++;
	}
	if( count > 0 )
		mean = mean / (double) count;

	//calculate rms
	double rms = 0;
	count = 0;
	for( int s = 0 ; s < num ; s++ ){
		if(  wf[s] < 10 ) continue;
		if( (wf[s] & 0x3F ) == 0x0 || (wf[s] & 0x3F ) == 0x3F ) continue;
		double value = wf[s];
		rms += (value-mean)*(value-mean);
		count++;
	}	
	if( count > 1 )
		rms = TMath::Sqrt( rms / (double)( count - 1 ) );

	//fill channel waveform hists
	for( int s = 0 ; s < num ; s++ ){
		hSampVsChan->Fill( chan, wf[s]);

		//measure stuck code fraction
		if( (wf[s] & 0x3F ) == 0x0 || (wf[s] & 0x3F ) == 0x3F )
			pFracStuckVsChan->Fill(chan, 1);
		else
			pFracStuckVsChan->Fill(chan, 0);
	}

	hMeanVsChan->Fill( chan, mean );
	pMeanVsChan->Fill( chan, mean );
	hRmsVsChan->Fill(chan, rms);
	pRmsVsChan->Fill(chan, rms);

	//draw waveform if wanted
	if( 0 ){
		gCh->Set(0);
		for( int s = 0 ; s < num ; s++ )
			gCh->SetPoint(gCh->GetN() , gCh->GetN() , wf[s] );
		std::cout << "Channel " << chan << std::endl;
		c0->Clear();
		std::string title = "Channel " + to_string( chan );
		gCh->SetTitle( title.c_str() );
		gCh->GetXaxis()->SetTitle("Sample Number");
		gCh->GetYaxis()->SetTitle("Sample Value (ADC counts)");
		//gCh->GetXaxis()->SetRangeUser(0,128);
		//gCh->GetYaxis()->SetRangeUser(500,1000);
		gCh->Draw("ALP");
		c0->Update();
		char ct;
		std::cin >> ct;
	}
}

void processNtuple(std::string inputFileName) {

  Analyze ana(inputFileName);
  ana.doAnalysis();

  return;
}

int main(int argc, char *argv[]){
  if(argc!=2){
    cout<<"Usage: processNtuple [inputFilename]"<<endl;
    return 0;
  }

  std::string inputFileName = argv[1];
  std::cout << "inputFileName " << inputFileName << std::endl;

  //define ROOT application object
  theApp = new TApplication("App", &argc, argv);
  processNtuple(inputFileName); 

  //return 1;
  gSystem->Exit(0);
}
