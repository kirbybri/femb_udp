//compile independently with: g++ -std=c++11 -o summaryAnalysis summaryAnalysis.cxx `root-config --cflags --glibs`
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
#include "TGraphErrors.h"
#include "TProfile2D.h"
#include "TF1.h"

using namespace std;

//global TApplication object declared here for simplicity
TApplication *theApp;

class Analyze {
	public:
	Analyze(std::string fileName);
	int processFileName(std::string inputFileName, std::string &baseFileName);
	void processInputFiles();
	void doAnalysis();
	void doAnalysisSingleFile();
	void outputResults();

	std::string inputFileName;
	TFile *inputFile;
	TFile *gOut;

	//metadata tree
	TTree *tr_metadata;

	//Constants
	//const int maxNumChan = 16;// SINGLE ASIC
	const int maxNumChan = 128;// FEMB

	TCanvas* c0;
	TGraph *gCh;
};

Analyze::Analyze(std::string fileName){

	inputFileName = fileName;

	//make output file
  	std::string outputFileName = "output_summaryAnalysis.root";
	if( processFileName( inputFileName, outputFileName ) )
		outputFileName = "output_summaryAnalysis_" + outputFileName + ".root";
  	gOut = new TFile(outputFileName.c_str() , "RECREATE");

  	//initialize canvas
  	c0 = new TCanvas("c0", "c0",1400,800);

	//initialize graphs
	gCh = new TGraph();
}

int Analyze::processFileName(std::string inputFileName, std::string &baseFileName){
        //check if filename is empty
        if( inputFileName.size() == 0 ){
                std::cout << "processFileName : Invalid filename " << std::endl;
                return 0;
        }

        //remove path from name
        size_t pos = 0;
        std::string delimiter = "/";
        while ((pos = inputFileName.find(delimiter)) != std::string::npos)
                inputFileName.erase(0, pos + delimiter.length());

	if( inputFileName.size() == 0 ){
                std::cout << "processFileName : Invalid filename " << std::endl;
                return 0;
        }

        //replace / with _
        std::replace( inputFileName.begin(), inputFileName.end(), '/', '_'); // replace all 'x' to 'y'
        std::replace( inputFileName.begin(), inputFileName.end(), '-', '_'); // replace all 'x' to 'y'

	baseFileName = inputFileName;
	
	return 1;
}

void Analyze::processInputFiles(){
	std::cout << inputFileName << std::endl;

	std::ifstream ifs(inputFileName);
	std::string line;

	while(std::getline(ifs, line))
	{
		//try to open rootfile
		inputFile = NULL;
		inputFile = TFile::Open( line.c_str() );

		if( !inputFile ){
			std::cout << "Error opening input file" << std::endl;
			gSystem->Exit(0);
		}

		if (inputFile->IsZombie()) {
			std::cout << "Error opening input file" << std::endl;
			gSystem->Exit(0);
		}

		if( !inputFile->IsOpen() ){
			std::cerr << "summaryAnalysis: getInputFiles - Could not open input file. Continue. " << line << std::endl;
			gSystem->Exit(0);
  		}
		
		doAnalysisSingleFile();
		inputFile->Close();
	}
}

void Analyze::doAnalysisSingleFile(){
	
	//sample vs chan histogram
	//TH2F *h1 = (TH2F*)inputFile->Get("hPulseHeightVsChan");
	TH2F *h1 = (TH2F*)inputFile->Get("hSampVsChan");
	if( !h1 ){
  		std::cout << "summaryAnalysis: doAnalysis - Could not find requested histogram, exiting" << std::endl;
		gSystem->Exit(0);
  	}

	//metadata
	TTree *t = (TTree*)inputFile->Get("metadata");
	if( !t ){
		std::cout << "summaryAnalysis: doAnalysis - Could not find metadata tree, exiting" << std::endl;
		gSystem->Exit(0);
  	}
	if( t->GetEntries() == 0 ){
		std::cout << "summaryAnalysis: doAnalysis - Metadata hhas no entries, exiting" << std::endl;
		gSystem->Exit(0);
	}
	//should test for branch names here

	//get metadata - note variable content depends on test setup
	ULong64_t subrun = -1;
	double volt = 0;
	t->SetBranchAddress("subrun", &subrun);
	t->SetBranchAddress("par1", &volt);
	t->GetEntry(0);

	//loop through channels 
	for(int ch = 0 ; ch < maxNumChan ; ch++ ){
		TH2F *h = h1;
		//get slice for channel
		char name[200];
		memset(name,0,sizeof(char)*100 );
        	sprintf(name,"hChan_%.3i",ch);
		TH1D *hChan = h->ProjectionY(name,ch+1,ch+1);
		if( hChan->GetEntries() < 10 )
			continue;

		//do channel specific measurements
		if(1){
			std::cout << volt << std::endl;
			c0->Clear();
			hChan->Draw();
			c0->Update();
			std::cout << "PRESS ANY KEY + ENTER TO CONTINUE" << std::endl;
			char cf;
			std::cin >> cf;
		}
	} //end loop over channels
}

void Analyze::outputResults(){
	gOut->cd("");
  	gOut->Close();
}

void summaryAnalysis(std::string inputFileName) {

  //Initialize analysis class
  Analyze ana(inputFileName);
  ana.processInputFiles();
  ana.outputResults();

  return;
}

int main(int argc, char *argv[]){
  if(argc!=2){
    cout<<"Usage: summaryAnalysis [filelist]"<<endl;
    return 0;
  }

  std::string inputFileName = argv[1];
  std::cout << "Input filelist " << inputFileName << std::endl;

  //define ROOT application object
  theApp = new TApplication("App", &argc, argv);
  summaryAnalysis(inputFileName); 

  //return 1;
  gSystem->Exit(0);
}
