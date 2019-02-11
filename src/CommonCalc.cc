/*
  Calculator for the most common event variables

   Author: Gena Kukartsev, 2012
*/



#include <iostream>
#include "LJMet/Com/interface/BaseCalc.h"
#include "LJMet/Com/interface/LjmetFactory.h"
#include "LJMet/Com/interface/LjmetEventContent.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 

#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"


class LjmetFactory;


class CommonCalc : public BaseCalc{
  
public:
  
  CommonCalc();
  virtual ~CommonCalc(){}

  virtual int BeginJob();
  virtual int ProduceEvent(edm::EventBase const & event, BaseEventSelector * selector);
  virtual int AnalyzeEvent(edm::EventBase const & event, BaseEventSelector * selector);
  virtual int EndJob(){return 0;}

  
private:

  edm::LumiReWeighting LumiWeights_;

};



static int reg = LjmetFactory::GetInstance()->Register(new CommonCalc(), "CommonCalc");



CommonCalc::CommonCalc(){
}



int CommonCalc::BeginJob(){
  /*
  if mPset.exists("dummy_parameter"){
    std::cout << mLegend 
          << "Example for config parameter: " 
	        << mPset.getParameter<std::string>("dummy_parameter") 
		      << std::endl;
  }
  else{
    std::cout << mLegend 
          << "Config parameter dummy_parameter is not defined" 
	        << std::endl;
  }
  */
  return 0;
}



int CommonCalc::ProduceEvent(edm::EventBase const & event,
			     BaseEventSelector * selector){
  //
  // produce and store some new data for other modules
  //

  double _val = 2.34;
  selector->SetTestValue(_val);

  return 0;
}



int CommonCalc::AnalyzeEvent(edm::EventBase const & event,
			     BaseEventSelector * selector){
  //
  // compute event variables here
  //

  //SetValue("test", 3.4);


  //
  //_____ Basic event Information _____________________
  //
  int iRun   = event.id().run();
  int iLumi  = (unsigned int)event.id().luminosityBlock();
  long long iEvent = (Long64_t)event.id().event();
  SetValue("event", iEvent);
  SetValue("lumi",  iLumi);
  SetValue("run",   iRun);
  
  //
  // _____ L1 Prefiring weights _____
  //
  edm::Handle<double> nonPrefiringProb;
  edm::Handle<double> nonPrefiringProbUp;
  edm::Handle<double> nonPrefiringProbDown;
  double L1NonPrefiringProb = 1.0;
  double L1NonPrefiringProbUp = 1.0;
  double L1NonPrefiringProbDown = 1.0;
  if(event.getByLabel(edm::InputTag("prefiringweight","NonPrefiringProb") , nonPrefiringProb)){
    L1NonPrefiringProb = *nonPrefiringProb;
  }
  if(event.getByLabel(edm::InputTag("prefiringweight","NonPrefiringProbUp") , nonPrefiringProbUp)){
    L1NonPrefiringProbUp = *nonPrefiringProbUp;
  }
  if(event.getByLabel(edm::InputTag("prefiringweight","NonPrefiringProbDown") , nonPrefiringProbDown)){
    L1NonPrefiringProbDown = *nonPrefiringProbDown;
  }

  SetValue("L1NonPrefiringProb",L1NonPrefiringProb);
  SetValue("L1NonPrefiringProbUp",L1NonPrefiringProbUp);
  SetValue("L1NonPrefiringProbDown",L1NonPrefiringProbDown);

  //
  // _____ Get objects from the selector _____________________
  //
  std::vector<edm::Ptr<pat::Jet> >      const & vSelJets = selector->GetSelectedJets();
  std::vector<edm::Ptr<pat::Jet> >      const & vSelBtagJets = selector->GetSelectedBtagJets();
  std::vector<edm::Ptr<pat::Jet> >      const & vAllJets = selector->GetAllJets();
  std::vector<edm::Ptr<pat::Muon> >     const & vSelMuons = selector->GetSelectedMuons();
  std::vector<edm::Ptr<pat::Muon> >     const & vLooseMuons = selector->GetLooseMuons();
  std::vector<edm::Ptr<pat::Electron> > const & vSelElectrons = selector->GetSelectedElectrons();
  edm::Ptr<pat::MET>                    const & pMet = selector->GetMet();
  (void)pMet; // silence warning
  
  
  //
  //_____Basic objects' info _________________________________
  //
  int _nAllJets      = (int)vAllJets.size();
  int _nSelJets      = (int)vSelJets.size();
  int _nSelBtagJets  = (int)vSelBtagJets.size();
  int _nSelMuons     = (int)vSelMuons.size();
  int _nLooseMuons   = (int)vLooseMuons.size();
  int _nSelElectrons = (int)vSelElectrons.size();
  SetValue("nAllJets",      _nAllJets);
  SetValue("nSelJets",      _nSelJets);
  SetValue("nSelBtagJets",  _nSelBtagJets);
  SetValue("nTightMuons",   _nSelMuons);
  SetValue("nLooseMuons",   _nLooseMuons);
  SetValue("nSelElectrons", _nSelElectrons);



  return 0;
}
