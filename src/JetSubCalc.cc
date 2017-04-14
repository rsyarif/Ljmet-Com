/*
 Calculator for substructure variables
 
 Author: Joshua Swanson, 2014. Updated Julie Hogan, 2015. 
 */

#include <iostream>
#include <limits>   // std::numeric_limits
#include <vector>
#include <string>
#include <boost/algorithm/string.hpp>
#include "TLorentzVector.h"
#include "TFile.h"
#include "TF1.h"

#include "LJMet/Com/interface/BaseCalc.h"
#include "LJMet/Com/interface/BaseEventSelector.h"
#include "LJMet/Com/interface/LjmetFactory.h"
#include "LJMet/Com/interface/LjmetEventContent.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/PATObject.h"
#include "DataFormats/BTauReco/interface/CATopJetTagInfo.h"
#include "LJMet/Com/interface/HTTTopJetTagInfo.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"

using namespace std;

class LjmetFactory;

class JetSubCalc : public BaseCalc {
    
public:
    JetSubCalc();
    virtual ~JetSubCalc();
    virtual int BeginJob();
    virtual int AnalyzeEvent(edm::EventBase const & event, BaseEventSelector * selector);
    virtual int EndJob();
    
private:
  edm::InputTag slimmedJetColl_it;
  edm::InputTag slimmedJetsAK8Coll_it;
  edm::InputTag slimmedJetsAK8SDColl_it;
  edm::InputTag slimmedJetsAK8CTTColl_it;
  edm::InputTag selectedPatJetsCA15Coll_it;
  edm::InputTag genParticles_it;
  edm::InputTag httTagInfo_it;
  std::string bDiscriminant;
  std::string tagInfo;
  double kappa;
  bool killHF;
  bool doNewJEC;
  bool isMc;
  bool JECup;
  bool JECdn;
  bool JERup;
  bool JERdn;
  bool useL2L3Mass;
  std::string puppiCorrPath;
  std::string MCL3;
  std::string MCL2;
  std::string MCSF;
  std::string DataL3;
  std::string DataL2;
  std::string DataL2L3;
  JME::JetResolutionScaleFactor resolution_SF;
  FactorizedJetCorrector *jecak8;
  JetCorrectorParameters *L3JetParAK8MC;
  JetCorrectorParameters *L2JetParAK8MC;
  JetCorrectorParameters *ResJetParAK8MC; 
  JetCorrectorParameters *L3JetParAK8BCD;
  JetCorrectorParameters *L2JetParAK8BCD;
  JetCorrectorParameters *ResJetParAK8BCD; 
  JetCorrectorParameters *L3JetParAK8EF;
  JetCorrectorParameters *L2JetParAK8EF;
  JetCorrectorParameters *ResJetParAK8EF; 
  JetCorrectorParameters *L3JetParAK8G;
  JetCorrectorParameters *L2JetParAK8G;
  JetCorrectorParameters *ResJetParAK8G; 
  JetCorrectorParameters *L3JetParAK8H;
  JetCorrectorParameters *L2JetParAK8H;
  JetCorrectorParameters *ResJetParAK8H; 
  JetCorrectionUncertainty *jecUnc;
  std::vector<JetCorrectorParameters> vParAK8MC;
  std::vector<JetCorrectorParameters> vParAK8BCD;
  std::vector<JetCorrectorParameters> vParAK8EF;
  std::vector<JetCorrectorParameters> vParAK8G;
  std::vector<JetCorrectorParameters> vParAK8H;
  TRandom3 JERrand;
  TF1 *puppisd_corrGEN;
  TF1 *puppisd_corrRECO_cen;
  TF1 *puppisd_corrRECO_for;
};

static int reg = LjmetFactory::GetInstance()->Register(new JetSubCalc(), "JetSubCalc");

struct sortclass {
  //  bool operator() (double i,double j) { return (i>j);}
  bool operator() (pat::Jet i, pat::Jet j){ return (i.pt() > j.pt());}
} ptsorter;


JetSubCalc::JetSubCalc()
{
}

JetSubCalc::~JetSubCalc()
{
}

int JetSubCalc::BeginJob()
{
    if (mPset.exists("slimmedJetColl")){ slimmedJetColl_it = mPset.getParameter<edm::InputTag>("slimmedJetColl");}
    else slimmedJetColl_it = edm::InputTag("slimmedJets");
    
    if (mPset.exists("slimmedJetsAK8Coll")) slimmedJetsAK8Coll_it = mPset.getParameter<edm::InputTag>("slimmedJetsAK8Coll");
    else slimmedJetsAK8Coll_it = edm::InputTag("slimmedJetsAK8");

    if (mPset.exists("genParticles")) genParticles_it = mPset.getParameter<edm::InputTag>("genParticles");
    else                              genParticles_it = edm::InputTag("prunedGenParticles");

    if (mPset.exists("bDiscriminant")) bDiscriminant = mPset.getParameter<std::string>("bDiscriminant");
    else bDiscriminant = "pfCombinedInclusiveSecondaryVertexV2BJetTags";
    
    std::cout << " JetSubCalc Bdisc = " << bDiscriminant << std::endl;
    
    if (mPset.exists("tagInfo")) tagInfo = mPset.getParameter<std::string>("tagInfo");
    else tagInfo = "CATop";

    if(mPset.exists("kappa")) kappa = mPset.getParameter<double>("kappa");
    else kappa = 0.5;

    if(mPset.exists("killHF")) killHF = mPset.getParameter<bool>("killHF");
    else killHF = false;

    if(mPset.exists("doNewJEC")) doNewJEC = mPset.getParameter<bool>("doNewJEC");
    else doNewJEC = false;

    cout << "JetSubCalc: doNewJEC = " << doNewJEC << ", killHF = " << killHF << endl;

    if(mPset.exists("useL2L3Mass")) useL2L3Mass = mPset.getParameter<bool>("useL2L3Mass");
    else useL2L3Mass = false;

    if(mPset.exists("puppiCorrPath")) puppiCorrPath = mPset.getParameter<std::string>("puppiCorrPath");
    else puppiCorrPath = "CMSSW_8_0_26_patch1/src/LJMet/Com/PuppiSoftdropMassCorr/weights/puppiCorr.root";

    if(mPset.exists("isMc")) isMc = mPset.getParameter<bool>("isMc");
    else isMc = false;

    if(mPset.exists("JECup")) JECup = mPset.getParameter<bool>("JECup");
    else JECup = false;

    if(mPset.exists("JECdown")) JECdn = mPset.getParameter<bool>("JECdown");
    else JECdn = false;

    if(mPset.exists("JERup")) JERup = mPset.getParameter<bool>("JERup");
    else JERup = false;

    if(mPset.exists("JERdown")) JERdn = mPset.getParameter<bool>("JERdown");
    else JERdn = false;

    if(useL2L3Mass){
      cout << "JetSubCalc: using L2+L3 corrected groomed masses" << endl;
      if(mPset.exists("MCL2JetParAK8")) MCL2 = mPset.getParameter<std::string>("MCL2JetParAK8");
      else MCL2 = "/uscms_data/d3/jmanagan/CMSSW_7_4_14/src/LJMet/Com/data/Summer15_25nsV5_MC_L1FastJet";
      if(mPset.exists("MCL3JetParAK8")) MCL3 = mPset.getParameter<std::string>("MCL3JetParAK8");
      else MCL3 = "/uscms_data/d3/jmanagan/CMSSW_7_4_14/src/LJMet/Com/data/Summer15_25nsV5_MC_L1FastJet";
      if(mPset.exists("MCSF")) MCSF = mPset.getParameter<std::string>("MCSF");
      else MCSF = "/uscms_data/d3/jmanagan/CMSSW_7_4_14/src/LJMet/Com/data/Summer15_25nsV5_MC_L1FastJet";

      if(mPset.exists("DataL2JetParAK8")) DataL2 = mPset.getParameter<std::string>("DataL2JetParAK8");
      else DataL2 = "/uscms_data/d3/jmanagan/CMSSW_7_4_14/src/LJMet/Com/data/Summer15_25nsV5_Data_L1FastJet";
      if(mPset.exists("DataL3JetParAK8")) DataL3 = mPset.getParameter<std::string>("DataL3JetParAK8");
      else DataL3 = "/uscms_data/d3/jmanagan/CMSSW_7_4_14/src/LJMet/Com/data/Summer15_25nsV5_Data_L1FastJet";
      if(mPset.exists("DataL2L3JetParAK8")) DataL2L3 = mPset.getParameter<std::string>("DataL2L3JetParAK8");
      else DataL2L3 = "/uscms_data/d3/jmanagan/CMSSW_7_4_14/src/LJMet/Com/data/Summer15_25nsV5_Data_L1FastJet";
 
      std::string strL2BCD = DataL2;
      std::string strL2EF = strL2BCD; boost::replace_first(strL2EF,"BCD","EF");
      std::string strL2G = strL2BCD; boost::replace_first(strL2G,"BCD","G");
      std::string strL2H = strL2BCD; boost::replace_first(strL2H,"BCD","H");  

      std::string strL3BCD = DataL3;
      std::string strL3EF = strL3BCD; boost::replace_first(strL3EF,"BCD","EF");
      std::string strL3G = strL3BCD; boost::replace_first(strL3G,"BCD","G");
      std::string strL3H = strL3BCD; boost::replace_first(strL3H,"BCD","H");  

      std::string strL2L3BCD = DataL2L3;
      std::string strL2L3EF = strL2L3BCD; boost::replace_first(strL2L3EF,"BCD","EF");
      std::string strL2L3G = strL2L3BCD; boost::replace_first(strL2L3G,"BCD","G");
      std::string strL2L3H = strL2L3BCD; boost::replace_first(strL2L3H,"BCD","H");  
       
      if(isMc){
	L3JetParAK8MC  = new JetCorrectorParameters(MCL3);
	L2JetParAK8MC  = new JetCorrectorParameters(MCL2);
	vParAK8MC.push_back(*L2JetParAK8MC);
	vParAK8MC.push_back(*L3JetParAK8MC);
      }else{
	ResJetParAK8BCD = new JetCorrectorParameters(DataL2L3); 
	L3JetParAK8BCD  = new JetCorrectorParameters(DataL3);
	L2JetParAK8BCD  = new JetCorrectorParameters(DataL2);
	vParAK8BCD.push_back(*L2JetParAK8BCD);
	vParAK8BCD.push_back(*L3JetParAK8BCD);
	vParAK8BCD.push_back(*ResJetParAK8BCD);

	ResJetParAK8EF = new JetCorrectorParameters(strL2L3EF); 
	L3JetParAK8EF  = new JetCorrectorParameters(strL3EF);
	L2JetParAK8EF  = new JetCorrectorParameters(strL2EF);
	vParAK8EF.push_back(*L2JetParAK8EF);
	vParAK8EF.push_back(*L3JetParAK8EF);
	vParAK8EF.push_back(*ResJetParAK8EF);

	ResJetParAK8G = new JetCorrectorParameters(strL2L3G); 
	L3JetParAK8G  = new JetCorrectorParameters(strL3G);
	L2JetParAK8G  = new JetCorrectorParameters(strL2G);
	vParAK8G.push_back(*L2JetParAK8G);
	vParAK8G.push_back(*L3JetParAK8G);
	vParAK8G.push_back(*ResJetParAK8G);

	ResJetParAK8H = new JetCorrectorParameters(strL2L3H); 
	L3JetParAK8H  = new JetCorrectorParameters(strL3H);
	L2JetParAK8H  = new JetCorrectorParameters(strL2H);
	vParAK8H.push_back(*L2JetParAK8H);
	vParAK8H.push_back(*L3JetParAK8H);
	vParAK8H.push_back(*ResJetParAK8H);
      }
      
      if(isMc) jecak8 = new FactorizedJetCorrector(vParAK8MC);
      jecUnc = new JetCorrectionUncertainty(mPset.getParameter<std::string>("UncertaintyAK8"));

      resolution_SF = JME::JetResolutionScaleFactor(MCSF);    
    }

    TFile* file = TFile::Open(puppiCorrPath.c_str(),"READ");
    puppisd_corrGEN      = (TF1*)file->Get("puppiJECcorr_gen");
    puppisd_corrRECO_cen = (TF1*)file->Get("puppiJECcorr_reco_0eta1v3");
    puppisd_corrRECO_for = (TF1*)file->Get("puppiJECcorr_reco_1v3eta2v5");
    file->Close();
    

    return 0;
}

int JetSubCalc::AnalyzeEvent(edm::EventBase const & event, BaseEventSelector * selector)
{
    // ----- Get AK4 jet objects from the selector -----
    // This is updated -- original version used all AK4 jets without selection 
    std::vector<pat::Jet>                       const & theJets = selector->GetSelectedCorrJets();
    std::vector<std::pair<TLorentzVector,bool>> const & theCorrBtagJets = selector->GetCorrJetsWithBTags();

    // Old version
    //    edm::Handle<std::vector<pat::Jet> > theJets;
    //    event.getByLabel(slimmedJetColl_it, theJets);

    float subjetCSV;
    int CSVL, CSVM, CSVT;
    double theJetHT;
    
    // Available variables
    std::vector<double> theJetPt;
    std::vector<double> theJetEta;
    std::vector<double> theJetPhi;
    std::vector<double> theJetEnergy;
    std::vector<double> theJetCSV;

    std::vector<double> theJetCEmEnergy;
    std::vector<double> theJetNEmEnergy;
    std::vector<double> theJetCEmEFrac;
    std::vector<double> theJetNEmEFrac;
    std::vector<double> theJetCHadEnergy;
    std::vector<double> theJetNHadEnergy;
    std::vector<double> theJetCHadEFrac;
    std::vector<double> theJetNHadEFrac;
    std::vector<double> theJetMuonEFrac;

    // Additional variables related to the associated secondary vertex if there is one
    // Mass of the vertex
    std::vector<double> theJetVtxMass;
    // Number of tracks
    std::vector<double> theJetVtxNtracks;
    // Decay length value and significance
    std::vector<double> theJetVtx3DVal;
    std::vector<double> theJetVtx3DSig;
    
    // Discriminator for the MVA PileUp id.
    // NOTE: Training used is for ak5PFJetsCHS in CMSSW 5.3.X and Run 1 pileup
    std::vector<double> theJetPileupJetId;
    
    //Identity
    std::vector<int> theJetIndex;
    std::vector<int> theJetnDaughters;
    
    //Daughter four std::vector and index
    std::vector<double> theJetDaughterPt;
    std::vector<double> theJetDaughterEta;
    std::vector<double> theJetDaughterPhi;
    std::vector<double> theJetDaughterEnergy;
    
    std::vector<int> theJetDaughterMotherIndex;
    std::vector<int> theJetCSVLSubJets;
    std::vector<int> theJetCSVMSubJets;
    std::vector<int> theJetCSVTSubJets;

    std::vector<int> theJetPFlav;
    std::vector<int> theJetHFlav;
    std::vector<int> theJetBTag;
    std::vector<int> theJetBTag_bSFup;
    std::vector<int> theJetBTag_bSFdn;
    std::vector<int> theJetBTag_lSFup;
    std::vector<int> theJetBTag_lSFdn;
    
    double theVtxMass, theVtxNtracks, theVtx3DVal, theVtx3DSig, thePileupJetId;

    for (std::vector<pat::Jet>::const_iterator ijet = theJets.begin(); ijet != theJets.end(); ijet++) {
      int index = (int)(ijet-theJets.begin());

      if(killHF && fabs(ijet->eta()) > 2.4) continue;

      theVtxNtracks  = -std::numeric_limits<double>::max();
      theVtxNtracks  = (double)ijet->userFloat("vtxNtracks");
				
      if (theVtxNtracks > 0) {
	theVtxMass     = -std::numeric_limits<double>::max();
	theVtx3DVal    = -std::numeric_limits<double>::max();
	theVtx3DSig    = -std::numeric_limits<double>::max();
	
	theVtxMass     = (double)ijet->userFloat("vtxMass");
	theVtx3DVal    = (double)ijet->userFloat("vtx3DVal");
	theVtx3DSig    = (double)ijet->userFloat("vtx3DSig");
        
	theJetVtxNtracks.push_back(theVtxNtracks);
	theJetVtxMass.push_back(theVtxMass);
	theJetVtx3DVal.push_back(theVtx3DVal);
	theJetVtx3DSig.push_back(theVtx3DSig);
      }
      
      thePileupJetId = -std::numeric_limits<double>::max();
      thePileupJetId = (double)ijet->userFloat("pileupJetId:fullDiscriminant");
      theJetPileupJetId.push_back(thePileupJetId);

      theJetPt     . push_back(ijet->pt());
      theJetEta    . push_back(ijet->eta());
      theJetPhi    . push_back(ijet->phi());
      theJetEnergy . push_back(ijet->energy());
      
      theJetCSV.push_back(ijet->bDiscriminator( bDiscriminant ));
      theJetBTag.push_back(selector->isJetTagged(*ijet, event, true, 0));
      theJetBTag_bSFup.push_back(selector->isJetTagged(*ijet, event, true, 1));
      theJetBTag_bSFdn.push_back(selector->isJetTagged(*ijet, event, true, 2));
      theJetBTag_lSFup.push_back(selector->isJetTagged(*ijet, event, true, 3));
      theJetBTag_lSFdn.push_back(selector->isJetTagged(*ijet, event, true, 4));
      theJetPFlav.push_back(abs(ijet->partonFlavour()));
      theJetHFlav.push_back(abs(ijet->hadronFlavour()));

      theJetCEmEnergy.push_back(ijet->chargedEmEnergy());
      theJetNEmEnergy.push_back(ijet->neutralEmEnergy());
      theJetCEmEFrac.push_back(ijet->chargedEmEnergyFraction());
      theJetNEmEFrac.push_back(ijet->neutralEmEnergyFraction());	    

      theJetCHadEnergy.push_back(ijet->chargedHadronEnergy());
      theJetNHadEnergy.push_back(ijet->neutralHadronEnergy());
      theJetCHadEFrac.push_back(ijet->chargedHadronEnergyFraction());
      theJetNHadEFrac.push_back(ijet->neutralHadronEnergyFraction());      
      theJetMuonEFrac.push_back(ijet->muonEnergyFraction());

      theJetIndex.push_back(index);
      theJetnDaughters.push_back((int)ijet->numberOfDaughters());
      
      //HT
      theJetHT += ijet->pt(); 

    }
    
    double leading_pt = -999.;
    for (std::vector<pat::Jet>::const_iterator ijet = theJets.begin(); ijet != theJets.end(); ijet++) { 

      if(killHF && fabs(ijet->eta()) > 2.4) continue;
      if (ijet->pt() > leading_pt){leading_pt = ijet->pt();}
    }

    double second_leading_pt =-999.;
    for (std::vector<pat::Jet>::const_iterator ijet = theJets.begin(); ijet != theJets.end(); ijet++) { 

      if(killHF && fabs(ijet->eta()) > 2.4) continue;
      if(ijet->pt() > second_leading_pt && ijet->pt() < leading_pt){
	second_leading_pt = ijet->pt();
      }
    }

    SetValue("theJetPt",     theJetPt);
    SetValue("theJetEta",    theJetEta);
    SetValue("theJetPhi",    theJetPhi);
    SetValue("theJetEnergy", theJetEnergy);
    SetValue("theJetCSV",    theJetCSV);
    SetValue("theJetPFlav",  theJetPFlav);
    SetValue("theJetHFlav",  theJetHFlav);
    SetValue("theJetBTag",   theJetBTag);
    SetValue("theJetBTag_bSFup",   theJetBTag_bSFup);
    SetValue("theJetBTag_bSFdn",   theJetBTag_bSFdn);
    SetValue("theJetBTag_lSFup",   theJetBTag_lSFup);
    SetValue("theJetBTag_lSFdn",   theJetBTag_lSFdn);

    SetValue("theJetCEmEnergy", theJetCEmEnergy); 
    SetValue("theJetNEmEnergy", theJetNEmEnergy); 
    SetValue("theJetCEmEFrac",  theJetCEmEFrac);  
    SetValue("theJetNEmEFrac",  theJetNEmEFrac);  
    SetValue("theJetCHadEnergy",theJetCHadEnergy);
    SetValue("theJetNHadEnergy",theJetNHadEnergy);
    SetValue("theJetCHadEFrac", theJetCHadEFrac); 
    SetValue("theJetNHadEFrac", theJetNHadEFrac); 
    SetValue("theJetMuonEFrac", theJetMuonEFrac);

    SetValue("theJetHT", theJetHT);    
    SetValue("theJetLeadPt", leading_pt);
    SetValue("theJetSubLeadPt", second_leading_pt);

    SetValue("theJetVtxMass",     theJetVtxMass);
    SetValue("theJetVtxNtracks",  theJetVtxNtracks);
    SetValue("theJetVtx3DVal",    theJetVtx3DVal);
    SetValue("theJetVtx3DSig",    theJetVtx3DSig);
    SetValue("theJetPileupJetId", theJetPileupJetId);
    SetValue("theJetnDaughters", theJetnDaughters);

    // Load in AK8 jets (no selection performed on these)
    edm::Handle<std::vector<pat::Jet> > theAK8Jets;
    event.getByLabel(slimmedJetsAK8Coll_it, theAK8Jets);

    // Four std::vector
    std::vector<double> theJetAK8Pt;
    std::vector<double> theJetAK8Eta;
    std::vector<double> theJetAK8Phi;
    std::vector<double> theJetAK8Energy;
    std::vector<double> theJetAK8CSV;
    std::vector<double> theJetAK8DoubleB;
    std::vector<double> theJetAK8JetCharge;
    std::vector<double> theJetAK8GenPt;
    std::vector<double> theJetAK8GenDR;
    std::vector<double> theJetAK8GenMass;

    std::vector<double> theJetAK8CEmEnergy;
    std::vector<double> theJetAK8NEmEnergy;
    std::vector<double> theJetAK8CEmEFrac;
    std::vector<double> theJetAK8NEmEFrac;
    std::vector<double> theJetAK8CHadEnergy;
    std::vector<double> theJetAK8NHadEnergy;
    std::vector<double> theJetAK8CHadEFrac;
    std::vector<double> theJetAK8NHadEFrac;

    // PUPPI values
    std::vector<double> theJetAK8PUPPIPt;
    std::vector<double> theJetAK8PUPPIEta;
    std::vector<double> theJetAK8PUPPIPhi;
    std::vector<double> theJetAK8PUPPIMass;
    std::vector<double> theJetAK8PUPPITau1;
    std::vector<double> theJetAK8PUPPITau2;
    std::vector<double> theJetAK8PUPPITau3;
    std::vector<double> theJetAK8PUPPISoftDropRaw;    
    std::vector<double> theJetAK8PUPPISoftDropCorr;    
    std::vector<double> theJetAK8PUPPISoftDrop;    
    std::vector<double> theJetAK8PUPPISoftDrop_JMSup;    
    std::vector<double> theJetAK8PUPPISoftDrop_JMSdn;    
    std::vector<double> theJetAK8PUPPISoftDrop_JMRup;
    std::vector<double> theJetAK8PUPPISoftDrop_JMRdn;    

    std::vector<double> theJetAK8PUPPISJPt;
    std::vector<double> theJetAK8PUPPISJEta;
    std::vector<double> theJetAK8PUPPISJPhi;
    std::vector<double> theJetAK8PUPPISJMass;
    std::vector<double> theJetAK8PUPPISJCSV;
    std::vector<int>    theJetAK8PUPPISJHFlav;
    std::vector<double> theJetAK8PUPPISJBTag;
    std::vector<int> theJetAK8PUPPISJIndex;
    std::vector<int> theJetAK8PUPPISJSize;
    
    // Pruned, trimmed and filtered masses available
    std::vector<double> theJetAK8PrunedMass;
    std::vector<double> theJetAK8PrunedMassWtagUncerts;
    std::vector<double> theJetAK8PrunedMassWtagUncerts_JMSup;
    std::vector<double> theJetAK8PrunedMassWtagUncerts_JMSdn;
    std::vector<double> theJetAK8PrunedMassWtagUncerts_JMRup;
    std::vector<double> theJetAK8PrunedMassWtagUncerts_JMRdn;
    std::vector<double> theJetAK8SoftDropMass;
    
    // n-subjettiness variables tau1, tau2, and tau3 available
    std::vector<double> theJetAK8NjettinessTau1;
    std::vector<double> theJetAK8NjettinessTau2;
    std::vector<double> theJetAK8NjettinessTau3;

    std::vector<double> theJetAK8Mass;
    std::vector<int>    theJetAK8Index;
    std::vector<int>    theJetAK8nDaughters;
    
    std::vector<double> theJetAK8SDSubjetPt;
    std::vector<double> theJetAK8SDSubjetEta;
    std::vector<double> theJetAK8SDSubjetPhi;
    std::vector<double> theJetAK8SDSubjetMass;
    std::vector<double> theJetAK8SDSubjetCSV;
    std::vector<int>    theJetAK8SDSubjetHFlav;
    std::vector<double> theJetAK8SDSubjetBTag;
    std::vector<double> theJetAK8SDSubjetDR;
    std::vector<int> theJetAK8SDSubjetIndex;
    std::vector<int> theJetAK8SDSubjetSize;
    std::vector<int> theJetAK8SDSubjetNCSVL;
    std::vector<int> theJetAK8SDSubjetNCSVMSF;
    std::vector<int> theJetAK8SDSubjetNCSVM_lSFup;
    std::vector<int> theJetAK8SDSubjetNCSVM_lSFdn;
    std::vector<int> theJetAK8SDSubjetNCSVM_bSFup;
    std::vector<int> theJetAK8SDSubjetNCSVM_bSFdn;
    
    double topMass, minMass, jetCharge;
    int nSubJets;
    double thePuppiSoftDrop;
    double thePrunedMass,theSoftDropMass;
    double theNjettinessTau1, theNjettinessTau2, theNjettinessTau3;
    double thePuppiTau1, thePuppiTau2, thePuppiTau3;

    double SDsubjetPt;
    double SDsubjetEta; 
    double SDsubjetPhi;      
    double SDsubjetMass;      
    double SDsubjetBdisc;     
    int    SDsubjetHFlav;
    double SDsubjetBTag;     
    double SDdeltaRsubjetJet; 

    int nSDSubJets;
    int nSDSubsCSVL;
    int nSDSubsCSVM;
    int nSDSubsCSVMSF;
    int nSDSubsCSVM_bSFup;
    int nSDSubsCSVM_bSFdn;
    int nSDSubsCSVM_lSFup;
    int nSDSubsCSVM_lSFdn;
    int SDSubJetIndex;

    double PUPPIsubjetPt;
    double PUPPIsubjetEta; 
    double PUPPIsubjetPhi;      
    double PUPPIsubjetMass;      
    double PUPPIsubjetBdisc;     
    int    PUPPIsubjetHFlav;
    double PUPPIsubjetBTag;     

    int nPUPPISubJets;
    int nPUPPISubsCSVL;
    int nPUPPISubsCSVM;
    int nPUPPISubsCSVMSF;
    int nPUPPISubsCSVM_bSFup;
    int nPUPPISubsCSVM_bSFdn;
    int nPUPPISubsCSVM_lSFup;
    int nPUPPISubsCSVM_lSFdn;
    int PUPPISubJetIndex;

    int iRun   = event.id().run();
    if(!isMc){
      delete jecak8;
      if(iRun <= 276811){
	jecak8 = new FactorizedJetCorrector(vParAK8BCD);
      }
      else if(iRun <= 278801){ 
	jecak8 = new FactorizedJetCorrector(vParAK8EF);
      }
      else if(iRun <= 280385){
	jecak8 = new FactorizedJetCorrector(vParAK8G);
      }
      else{
	jecak8 = new FactorizedJetCorrector(vParAK8H); 
      }
    }

    for (std::vector<pat::Jet>::const_iterator ijet = theAK8Jets->begin(); ijet != theAK8Jets->end(); ijet++) {
      int index = (int)(ijet-theAK8Jets->begin());

      pat::Jet rawJet = ijet->correctedJet(0);
      bool looseJetID = false;
      if(abs(rawJet.eta()) <= 2.7){
	looseJetID = (rawJet.neutralHadronEnergyFraction() < 0.99 && 
		      rawJet.neutralEmEnergyFraction() < 0.99 && 
		      (rawJet.chargedMultiplicity()+rawJet.neutralMultiplicity()) > 1) && 
	  ((abs(rawJet.eta()) <= 2.4 && 
	    rawJet.chargedHadronEnergyFraction() > 0 && 
	    rawJet.chargedEmEnergyFraction() < 0.99 && 
	    rawJet.chargedMultiplicity() > 0) || 
	   abs(rawJet.eta()) > 2.4);
      }else if(abs(rawJet.eta()) <= 3.0){
	looseJetID = rawJet.neutralEmEnergyFraction() > 0.01 && rawJet.neutralHadronEnergyFraction() < 0.98 && rawJet.neutralMultiplicity() > 2;
      }else{
	looseJetID = rawJet.neutralEmEnergyFraction() < 0.9 && rawJet.neutralMultiplicity() > 10;
      }
      if(!looseJetID) continue;	

      pat::Jet corrak8;
      if(doNewJEC){
	corrak8 = selector->correctJetReturnPatJet(*ijet, event, true);
      }else{
	corrak8 = *ijet;
      }      

      if(killHF && fabs(corrak8.eta()) > 2.4) continue;

      theJetAK8Pt    .push_back(corrak8.pt());
      theJetAK8Eta   .push_back(corrak8.eta());
      theJetAK8Phi   .push_back(corrak8.phi());
      theJetAK8Energy.push_back(corrak8.energy());
      theJetAK8Mass  .push_back(corrak8.mass());

      double thePuppiPt = -std::numeric_limits<double>::max();
      double thePuppiEta = -std::numeric_limits<double>::max();
      double thePuppiPhi = -std::numeric_limits<double>::max();
      double thePuppiMass = -std::numeric_limits<double>::max();
      thePuppiPt = corrak8.userFloat("ak8PFJetsPuppiValueMap:pt");  
      thePuppiEta = corrak8.userFloat("ak8PFJetsPuppiValueMap:eta"); 
      thePuppiPhi = corrak8.userFloat("ak8PFJetsPuppiValueMap:phi"); 
      thePuppiMass = corrak8.userFloat("ak8PFJetsPuppiValueMap:mass");
      theJetAK8PUPPIPt.push_back(thePuppiPt);
      theJetAK8PUPPIEta.push_back(thePuppiEta);
      theJetAK8PUPPIPhi.push_back(thePuppiPhi);
      theJetAK8PUPPIMass.push_back(thePuppiMass);

      double genDR = -99;
      double genpt = -99;
      double genmass = -99;
      TLorentzVector ak8jet;
      ak8jet.SetPtEtaPhiE(corrak8.pt(),corrak8.eta(),corrak8.phi(),corrak8.energy());
      const reco::GenJet * genJet = corrak8.genJet();
      if(genJet){
	TLorentzVector genP4;
	genP4.SetPtEtaPhiE(genJet->pt(),genJet->eta(),genJet->phi(),genJet->energy());
	genDR = ak8jet.DeltaR(genP4);	
	genpt = genJet->pt();
	genmass = genJet->mass();
      }
      theJetAK8GenPt.push_back(genpt);
      theJetAK8GenMass.push_back(genmass);
      theJetAK8GenDR.push_back(genDR);

      thePrunedMass   = -std::numeric_limits<double>::max();
      theSoftDropMass = -std::numeric_limits<double>::max();
      thePuppiSoftDrop = -std::numeric_limits<double>::max();

      double unc = 1.0;
      double unc_pruned_up = 1.0;
      double unc_pruned_dn = 1.0;
      double unc_softdrop_up = 1.0;
      double unc_softdrop_dn = 1.0;
      double ptscale_pruned = 1.0;
      double ptscale_pruned_up = 1.0;
      double ptscale_pruned_dn = 1.0;
      
      if(useL2L3Mass){
	edm::Handle<double> rhoHandle;
	edm::InputTag rhoSrc_("fixedGridRhoFastjetAll", "");
	event.getByLabel(rhoSrc_, rhoHandle);
	double rho = std::max(*(rhoHandle.product()), 0.0);

	pat::Jet l2l3jet = *ijet;
	jecak8->setJetEta(l2l3jet.correctedJet(0).eta());
	jecak8->setJetPt(l2l3jet.correctedJet(0).pt());
	jecak8->setJetE(l2l3jet.correctedJet(0).energy());
	jecak8->setJetA(l2l3jet.jetArea());
	jecak8->setRho(rho);
	double corr = jecak8->getCorrection();

	l2l3jet.scaleEnergy(corr);

	if(corr == 1.0) cout << "L2+L3 correction is 1.0" << endl;
	
	thePrunedMass   = corr*(double)l2l3jet.userFloat("ak8PFJetsCHSPrunedMass");
	theSoftDropMass = corr*(double)l2l3jet.userFloat("ak8PFJetsCHSSoftDropMass");		       

	// Apply JER uncertainty + W tagging uncertainty addition for pruned mass only
	// Talked to Jim -- they recommend mass as the smearing input with no gen info used.
	if(isMc){
	  //JME::JetParameters parameters;
	  //parameters.setJetPt(l2l3jet.pt());
	  //parameters.setJetEta(l2l3jet.eta());
	  //parameters.setRho(rho);
	  //Variation JERcentral = Variation::NOMINAL;
	  //Variation JERshifted = Variation::UP; // symmetric
	  //double uncert = fabs(resolution_SF.getScaleFactor(parameters,JERcentral) - resolution_SF.getScaleFactor(parameters,JERshifted));
	  //if(fabs(l2l3jet.eta()) > 2.5) uncert_pruned = sqrt(uncert*uncert + 0.18*0.18);

	  double res = 8.01/thePrunedMass;
	  double factor_pruned = 1.23;
	  double uncert_pruned = 0.18;
	  double factor_pruned_up = factor_pruned + uncert_pruned;
	  double factor_pruned_dn = factor_pruned - uncert_pruned;

	  if (factor_pruned>1) {
	    JERrand.SetSeed(abs(static_cast<int>(l2l3jet.phi()*1e4)));	   
	    ptscale_pruned = 1 + JERrand.Gaus(0,res)*sqrt(factor_pruned*factor_pruned - 1.0);
	  }
	  if (factor_pruned_up>1) {
	    JERrand.SetSeed(abs(static_cast<int>(l2l3jet.phi()*1e4)));	   
	    ptscale_pruned_up = 1 + JERrand.Gaus(0,res)*sqrt(factor_pruned_up*factor_pruned_up - 1.0);
	  }
	  if (factor_pruned_dn>1) {
	    JERrand.SetSeed(abs(static_cast<int>(l2l3jet.phi()*1e4)));	   
	    ptscale_pruned_dn = 1 + JERrand.Gaus(0,res)*sqrt(factor_pruned_dn*factor_pruned_dn - 1.0);
	  }

	  //jecUnc->setJetEta(l2l3jet.eta());
	  //jecUnc->setJetPt(l2l3jet.pt());
	  //unc = jecUnc->getUncertainty(true);
	  unc_pruned_up = 1.023; // + sqrt(unc*unc + 0.023*0.023);

	  //jecUnc->setJetEta(l2l3jet.eta());
	  //jecUnc->setJetPt(l2l3jet.pt());
	  //unc = jecUnc->getUncertainty(false);
	  unc_pruned_dn = 0.977; //1 - sqrt(unc*unc + 0.023*0.023);
	}
      }else{
	thePrunedMass   = (double)corrak8.userFloat("ak8PFJetsCHSPrunedMass");
	theSoftDropMass = (double)corrak8.userFloat("ak8PFJetsCHSSoftDropMass");
      }

      theNjettinessTau1 = -std::numeric_limits<double>::max();
      theNjettinessTau2 = -std::numeric_limits<double>::max();
      theNjettinessTau3 = -std::numeric_limits<double>::max();
      theNjettinessTau1 = (double)corrak8.userFloat("NjettinessAK8:tau1");
      theNjettinessTau2 = (double)corrak8.userFloat("NjettinessAK8:tau2");
      theNjettinessTau3 = (double)corrak8.userFloat("NjettinessAK8:tau3");

      thePuppiTau1 = -std::numeric_limits<double>::max();
      thePuppiTau2 = -std::numeric_limits<double>::max();
      thePuppiTau3 = -std::numeric_limits<double>::max();
      thePuppiTau1 = (double)corrak8.userFloat("ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau1");
      thePuppiTau2 = (double)corrak8.userFloat("ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau2");
      thePuppiTau3 = (double)corrak8.userFloat("ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau3");

      theJetAK8CSV.push_back(corrak8.bDiscriminator( bDiscriminant ));
      theJetAK8DoubleB.push_back(corrak8.bDiscriminator("pfBoostedDoubleSecondaryVertexAK8BJetTags"));

      theJetAK8CEmEnergy.push_back(corrak8.chargedEmEnergy());
      theJetAK8NEmEnergy.push_back(corrak8.neutralEmEnergy());
      theJetAK8CEmEFrac.push_back(corrak8.chargedEmEnergyFraction());
      theJetAK8NEmEFrac.push_back(corrak8.neutralEmEnergyFraction());	    

      theJetAK8CHadEnergy.push_back(corrak8.chargedHadronEnergy());
      theJetAK8NHadEnergy.push_back(corrak8.neutralHadronEnergy());
      theJetAK8CHadEFrac.push_back(corrak8.chargedHadronEnergyFraction());
      theJetAK8NHadEFrac.push_back(corrak8.neutralHadronEnergyFraction());
      
      theJetAK8PrunedMass.push_back(thePrunedMass); // JEC only
      theJetAK8SoftDropMass.push_back(theSoftDropMass); // JEC only
      theJetAK8PrunedMassWtagUncerts.push_back(thePrunedMass*ptscale_pruned); // JEC+JMR
      theJetAK8PrunedMassWtagUncerts_JMSup.push_back(thePrunedMass*ptscale_pruned*unc_pruned_up);
      theJetAK8PrunedMassWtagUncerts_JMSdn.push_back(thePrunedMass*ptscale_pruned*unc_pruned_dn);
      theJetAK8PrunedMassWtagUncerts_JMRup.push_back(thePrunedMass*ptscale_pruned_up);
      theJetAK8PrunedMassWtagUncerts_JMRdn.push_back(thePrunedMass*ptscale_pruned_dn);
      
      theJetAK8NjettinessTau1.push_back(theNjettinessTau1);
      theJetAK8NjettinessTau2.push_back(theNjettinessTau2);
      theJetAK8NjettinessTau3.push_back(theNjettinessTau3);
      theJetAK8PUPPITau1.push_back(thePuppiTau1);
      theJetAK8PUPPITau2.push_back(thePuppiTau2);
      theJetAK8PUPPITau3.push_back(thePuppiTau3);

      theJetAK8nDaughters.push_back((int)corrak8.numberOfDaughters());
      theJetAK8Index.push_back(index);

      //JetCharge calculation

      reco::Jet::Constituents constituents = corrak8.getJetConstituents();

      double sumWeightedCharge = 0.0;
      int con_charge = 0;
      double con_pt = 0.0;
      for(auto constituentItr=constituents.begin(); constituentItr!=constituents.end(); ++constituentItr){
	edm::Ptr<reco::Candidate> constituent=*constituentItr;

	con_charge = (int)constituent->charge();
	con_pt     = (double)constituent->pt();
	
	sumWeightedCharge = sumWeightedCharge + ( con_charge * pow(con_pt,kappa) );
	
      }

      jetCharge  = 1.0/( pow( (corrak8.pt()), kappa) ) * sumWeightedCharge;

      theJetAK8JetCharge.push_back(jetCharge);

      // Get Soft drop subjets for subjet b-tagging
      SDSubJetIndex = (int)theJetAK8SDSubjetPt.size();
      nSDSubJets  = std::numeric_limits<int>::min();
      nSDSubsCSVL = 0;
      nSDSubsCSVMSF = 0;
      nSDSubsCSVM_bSFup = 0;
      nSDSubsCSVM_bSFdn = 0;
      nSDSubsCSVM_lSFup = 0;
      nSDSubsCSVM_lSFdn = 0;
      double maxSubCSV = 0;

      auto const & sdSubjets = corrak8.subjets("SoftDrop");
      nSDSubJets = (int)sdSubjets.size();
      for ( auto const & it : sdSubjets ) {

	pat::Jet corrsubjet;
	if(doNewJEC){
	  corrsubjet = selector->correctJetReturnPatJet(*it, event, false);
	}else{
	  corrsubjet = *it;
	}

	SDsubjetPt        = -std::numeric_limits<double>::max();
	SDsubjetEta       = -std::numeric_limits<double>::max();
	SDsubjetPhi       = -std::numeric_limits<double>::max();
	SDsubjetMass      = -std::numeric_limits<double>::max();
	SDsubjetBdisc     = -std::numeric_limits<double>::max();
	SDdeltaRsubjetJet = std::numeric_limits<double>::max();
      
	SDsubjetPt        = corrsubjet.pt();
	SDsubjetEta       = corrsubjet.eta();
	SDsubjetPhi       = corrsubjet.phi();
	SDsubjetMass      = corrsubjet.mass();
	SDsubjetBdisc     = corrsubjet.bDiscriminator(bDiscriminant); 
	SDsubjetHFlav     = corrsubjet.hadronFlavour();
	SDsubjetBTag      = selector->isJetTagged(corrsubjet, event, true, 0, true);
	SDdeltaRsubjetJet = deltaR(corrak8.eta(), corrak8.phi(), SDsubjetEta, SDsubjetPhi);

	if(SDsubjetBdisc > 0.5426) nSDSubsCSVL++;
	if(SDsubjetBTag > 0) nSDSubsCSVMSF++;
	if(selector->isJetTagged(corrsubjet, event, true, 1, true) > 0) nSDSubsCSVM_bSFup++;
	if(selector->isJetTagged(corrsubjet, event, true, 2, true) > 0) nSDSubsCSVM_bSFdn++;
	if(selector->isJetTagged(corrsubjet, event, true, 3, true) > 0) nSDSubsCSVM_lSFup++;
	if(selector->isJetTagged(corrsubjet, event, true, 4, true) > 0) nSDSubsCSVM_lSFdn++;

	theJetAK8SDSubjetPt.push_back(SDsubjetPt);
	theJetAK8SDSubjetEta.push_back(SDsubjetEta);
	theJetAK8SDSubjetPhi.push_back(SDsubjetPhi);
	theJetAK8SDSubjetMass.push_back(SDsubjetMass);
	theJetAK8SDSubjetCSV.push_back(SDsubjetBdisc);
	theJetAK8SDSubjetHFlav.push_back(SDsubjetHFlav);
	theJetAK8SDSubjetBTag.push_back(SDsubjetBTag);
	theJetAK8SDSubjetDR.push_back(SDdeltaRsubjetJet);
      }

      theJetAK8SDSubjetIndex.push_back(SDSubJetIndex);
      theJetAK8SDSubjetSize.push_back(nSDSubJets);
      theJetAK8SDSubjetNCSVL.push_back(nSDSubsCSVL);
      theJetAK8SDSubjetNCSVMSF.push_back(nSDSubsCSVMSF);
      theJetAK8SDSubjetNCSVM_bSFup.push_back(nSDSubsCSVM_bSFup);
      theJetAK8SDSubjetNCSVM_bSFdn.push_back(nSDSubsCSVM_bSFdn);
      theJetAK8SDSubjetNCSVM_lSFup.push_back(nSDSubsCSVM_lSFup);
      theJetAK8SDSubjetNCSVM_lSFdn.push_back(nSDSubsCSVM_lSFdn);

      // Get PUPPI Soft drop subjets for subjet b-tagging
      PUPPISubJetIndex = (int)theJetAK8PUPPISJPt.size();
      nPUPPISubJets  = std::numeric_limits<int>::min();
      TLorentzVector puppi_sd, puppi_sd_subjet;
      puppi_sd.SetPtEtaPhiM(0,0,0,0);

      auto const & puppiSubjets = ijet->subjets("SoftDropPuppi");
      nPUPPISubJets = (int)puppiSubjets.size();
      for ( auto const & it : puppiSubjets ) {

	pat::Jet corrsubjet;
	corrsubjet = *it;

	PUPPIsubjetPt        = -std::numeric_limits<double>::max();
	PUPPIsubjetEta       = -std::numeric_limits<double>::max();
	PUPPIsubjetPhi       = -std::numeric_limits<double>::max();
	PUPPIsubjetMass      = -std::numeric_limits<double>::max();
	PUPPIsubjetBdisc     = -std::numeric_limits<double>::max();
      
	PUPPIsubjetPt        = corrsubjet.correctedP4(0).pt();
	PUPPIsubjetEta       = corrsubjet.correctedP4(0).eta();
	PUPPIsubjetPhi       = corrsubjet.correctedP4(0).phi();
	PUPPIsubjetMass      = corrsubjet.correctedP4(0).mass();
	PUPPIsubjetBdisc     = corrsubjet.bDiscriminator(bDiscriminant); 
	PUPPIsubjetHFlav     = corrsubjet.hadronFlavour();
	PUPPIsubjetBTag      = selector->isJetTagged(corrsubjet, event, true, 0, true);

	puppi_sd_subjet.SetPtEtaPhiM(PUPPIsubjetPt, PUPPIsubjetEta, PUPPIsubjetPhi, PUPPIsubjetMass);
	puppi_sd += puppi_sd_subjet;

	theJetAK8PUPPISJPt.push_back(SDsubjetPt);
	theJetAK8PUPPISJEta.push_back(SDsubjetEta);
	theJetAK8PUPPISJPhi.push_back(SDsubjetPhi);
	theJetAK8PUPPISJMass.push_back(SDsubjetMass);
	theJetAK8PUPPISJCSV.push_back(SDsubjetBdisc);
	theJetAK8PUPPISJHFlav.push_back(SDsubjetHFlav);
	theJetAK8PUPPISJBTag.push_back(SDsubjetBTag);

      }

      thePuppiSoftDrop = puppi_sd.M();

      double puppicorr = 1.0;
      if(isMc){
	float genCorr  = 1.;
	float recoCorr = 1.;
	float totalWeight = 1.;
	
	genCorr =  puppisd_corrGEN->Eval(corrak8.pt());
	if(fabs(corrak8.eta()) <= 1.3 ) recoCorr = puppisd_corrRECO_cen->Eval(corrak8.pt());
	else recoCorr = puppisd_corrRECO_for->Eval(corrak8.pt());
	
	puppicorr = genCorr * recoCorr;
      }
      double thePuppiSoftDropCorrected = thePuppiSoftDrop*puppicorr;

      double ptscale_puppisd = 1.0;
      double ptscale_puppisd_up = 1.0;
      double ptscale_puppisd_dn = 1.0;
      double unc_puppisd_up = 1.0;
      double unc_puppisd_dn = 1.0;
      if(isMc){
	double res = 10.1/thePuppiSoftDropCorrected;
	double factor_puppisd = 1;
	double uncert_puppisd = 0.20;
	double factor_puppisd_up = factor_puppisd + uncert_puppisd;
	double factor_puppisd_dn = factor_puppisd - uncert_puppisd;
	
	if (factor_puppisd>1) {
	  JERrand.SetSeed(abs(static_cast<int>(corrak8.phi()*1e4)));	   
	  ptscale_puppisd = 1 + JERrand.Gaus(0,res)*sqrt(factor_puppisd*factor_puppisd - 1.0);
	}
	if (factor_puppisd_up>1) {
	  JERrand.SetSeed(abs(static_cast<int>(corrak8.phi()*1e4)));	   
	  ptscale_puppisd_up = 1 + JERrand.Gaus(0,res)*sqrt(factor_puppisd_up*factor_puppisd_up - 1.0);
	}
	if (factor_puppisd_dn>1) {
	  JERrand.SetSeed(abs(static_cast<int>(corrak8.phi()*1e4)));	   
	  ptscale_puppisd_dn = 1 + JERrand.Gaus(0,res)*sqrt(factor_puppisd_dn*factor_puppisd_dn - 1.0);
	}
	unc_puppisd_up = 1.0094; // + sqrt(unc*unc + 0.023*0.023);
	unc_puppisd_dn = 0.9906; //1 - sqrt(unc*unc + 0.023*0.023);
      }

      theJetAK8PUPPISJIndex.push_back(PUPPISubJetIndex);
      theJetAK8PUPPISJSize.push_back(nPUPPISubJets);
      theJetAK8PUPPISoftDropRaw.push_back(thePuppiSoftDrop);
      theJetAK8PUPPISoftDropCorr.push_back(thePuppiSoftDropCorrected);
      theJetAK8PUPPISoftDrop.push_back(thePuppiSoftDropCorrected*ptscale_puppisd);
      theJetAK8PUPPISoftDrop_JMSup.push_back(thePuppiSoftDropCorrected*ptscale_puppisd*unc_puppisd_up);
      theJetAK8PUPPISoftDrop_JMSdn.push_back(thePuppiSoftDropCorrected*ptscale_puppisd*unc_puppisd_dn);
      theJetAK8PUPPISoftDrop_JMRup.push_back(thePuppiSoftDropCorrected*ptscale_puppisd_up);
      theJetAK8PUPPISoftDrop_JMRdn.push_back(thePuppiSoftDropCorrected*ptscale_puppisd_dn);

    }

    SetValue("theJetAK8Pt",     theJetAK8Pt);
    SetValue("theJetAK8Eta",    theJetAK8Eta);
    SetValue("theJetAK8Phi",    theJetAK8Phi);
    SetValue("theJetAK8Energy", theJetAK8Energy);
    SetValue("theJetAK8CSV",    theJetAK8CSV);
    SetValue("theJetAK8DoubleB",    theJetAK8DoubleB);
    SetValue("theJetAK8JetCharge", theJetAK8JetCharge);
    SetValue("theJetAK8GenPt",  theJetAK8GenPt);
    SetValue("theJetAK8GenDR",  theJetAK8GenDR);
    SetValue("theJetAK8GenMass",  theJetAK8GenMass);

    SetValue("theJetAK8PUPPIPt",     theJetAK8PUPPIPt);
    SetValue("theJetAK8PUPPIEta",    theJetAK8PUPPIEta);
    SetValue("theJetAK8PUPPIPhi",    theJetAK8PUPPIPhi);
    SetValue("theJetAK8PUPPIMass", theJetAK8PUPPIMass);
    SetValue("theJetAK8PUPPISoftDropRaw", theJetAK8PUPPISoftDropRaw);
    SetValue("theJetAK8PUPPISoftDropCorr", theJetAK8PUPPISoftDropCorr);
    SetValue("theJetAK8PUPPISoftDrop", theJetAK8PUPPISoftDrop);
    SetValue("theJetAK8PUPPISoftDrop_JMSup", theJetAK8PUPPISoftDrop_JMSup);
    SetValue("theJetAK8PUPPISoftDrop_JMSdn", theJetAK8PUPPISoftDrop_JMSdn);
    SetValue("theJetAK8PUPPISoftDrop_JMRup", theJetAK8PUPPISoftDrop_JMRup);
    SetValue("theJetAK8PUPPISoftDrop_JMRdn", theJetAK8PUPPISoftDrop_JMRdn);

    SetValue("theJetAK8CEmEnergy", theJetAK8CEmEnergy); 
    SetValue("theJetAK8NEmEnergy", theJetAK8NEmEnergy); 
    SetValue("theJetAK8CEmEFrac",  theJetAK8CEmEFrac);  
    SetValue("theJetAK8NEmEFrac",  theJetAK8NEmEFrac);  
    SetValue("theJetAK8CHadEnergy",theJetAK8CHadEnergy);
    SetValue("theJetAK8NHadEnergy",theJetAK8NHadEnergy);
    SetValue("theJetAK8CHadEFrac", theJetAK8CHadEFrac); 
    SetValue("theJetAK8NHadEFrac", theJetAK8NHadEFrac); 

    SetValue("theJetAK8PrunedMass",   theJetAK8PrunedMass);
    SetValue("theJetAK8PrunedMassWtagUncerts",   theJetAK8PrunedMassWtagUncerts);
    SetValue("theJetAK8PrunedMassWtagUncerts_JMSup",   theJetAK8PrunedMassWtagUncerts_JMSup);
    SetValue("theJetAK8PrunedMassWtagUncerts_JMSdn",   theJetAK8PrunedMassWtagUncerts_JMSdn);
    SetValue("theJetAK8PrunedMassWtagUncerts_JMRup",   theJetAK8PrunedMassWtagUncerts_JMRup);
    SetValue("theJetAK8PrunedMassWtagUncerts_JMRdn",   theJetAK8PrunedMassWtagUncerts_JMRdn);
    SetValue("theJetAK8SoftDropMass", theJetAK8SoftDropMass);
    
    SetValue("theJetAK8NjettinessTau1", theJetAK8NjettinessTau1);
    SetValue("theJetAK8NjettinessTau2", theJetAK8NjettinessTau2);
    SetValue("theJetAK8NjettinessTau3", theJetAK8NjettinessTau3);
    SetValue("theJetAK8PUPPITau1", theJetAK8PUPPITau1);
    SetValue("theJetAK8PUPPITau2", theJetAK8PUPPITau2);
    SetValue("theJetAK8PUPPITau3", theJetAK8PUPPITau3);

    SetValue("theJetAK8Mass",   theJetAK8Mass);
    SetValue("theJetAK8nDaughters", theJetAK8nDaughters);

    SetValue("theJetAK8SDSubjetPt",   theJetAK8SDSubjetPt);   
    SetValue("theJetAK8SDSubjetEta",  theJetAK8SDSubjetEta);  
    SetValue("theJetAK8SDSubjetPhi",  theJetAK8SDSubjetPhi);  
    SetValue("theJetAK8SDSubjetMass", theJetAK8SDSubjetMass); 
    SetValue("theJetAK8SDSubjetCSV",  theJetAK8SDSubjetCSV);  
    SetValue("theJetAK8SDSubjetHFlav", theJetAK8SDSubjetHFlav);
    SetValue("theJetAK8SDSubjetBTag",  theJetAK8SDSubjetBTag);  
    SetValue("theJetAK8SDSubjetDR",   theJetAK8SDSubjetDR);   
    SetValue("theJetAK8SDSubjetIndex",theJetAK8SDSubjetIndex);
    SetValue("theJetAK8SDSubjetSize", theJetAK8SDSubjetSize); 
    SetValue("theJetAK8SDSubjetNCSVL",theJetAK8SDSubjetNCSVL);
    SetValue("theJetAK8SDSubjetNCSVMSF",theJetAK8SDSubjetNCSVMSF);
    SetValue("theJetAK8SDSubjetNCSVM_bSFup",theJetAK8SDSubjetNCSVM_bSFup);
    SetValue("theJetAK8SDSubjetNCSVM_bSFdn",theJetAK8SDSubjetNCSVM_bSFdn);
    SetValue("theJetAK8SDSubjetNCSVM_lSFup",theJetAK8SDSubjetNCSVM_lSFup);
    SetValue("theJetAK8SDSubjetNCSVM_lSFdn",theJetAK8SDSubjetNCSVM_lSFdn);

    SetValue("theJetAK8PUPPISJPt",   theJetAK8PUPPISJPt);   
    SetValue("theJetAK8PUPPISJEta",  theJetAK8PUPPISJEta);  
    SetValue("theJetAK8PUPPISJPhi",  theJetAK8PUPPISJPhi);  
    SetValue("theJetAK8PUPPISJMass", theJetAK8PUPPISJMass); 
    SetValue("theJetAK8PUPPISJCSV",  theJetAK8PUPPISJCSV);  
    SetValue("theJetAK8PUPPISJHFlav", theJetAK8PUPPISJHFlav);
    SetValue("theJetAK8PUPPISJBTag",  theJetAK8PUPPISJBTag);  
    SetValue("theJetAK8PUPPISJIndex",theJetAK8PUPPISJIndex);
    SetValue("theJetAK8PUPPISJSize", theJetAK8PUPPISJSize); 


    //////////////// TRUE HADRONIC W/Z/H/Top decays //////////////////
    std::vector<int>    HadronicVHtID;
    std::vector<int>    HadronicVHtStatus;
    std::vector<double> HadronicVHtPt;
    std::vector<double> HadronicVHtEta;
    std::vector<double> HadronicVHtPhi;
    std::vector<double> HadronicVHtEnergy;
    std::vector<double> HadronicVHtD0Pt;
    std::vector<double> HadronicVHtD0Eta;
    std::vector<double> HadronicVHtD0Phi;
    std::vector<double> HadronicVHtD0E;
    std::vector<double> HadronicVHtD1Pt;
    std::vector<double> HadronicVHtD1Eta;
    std::vector<double> HadronicVHtD1Phi;
    std::vector<double> HadronicVHtD1E;
    std::vector<double> HadronicVHtD2Pt;
    std::vector<double> HadronicVHtD2Eta;
    std::vector<double> HadronicVHtD2Phi;
    std::vector<double> HadronicVHtD2E;
  
    // Get the generated particle collection
    edm::Handle<reco::GenParticleCollection> genParticles;
    if(isMc && event.getByLabel(genParticles_it, genParticles)){
      
      for(size_t i = 0; i < genParticles->size(); i++){
	const reco::GenParticle &p = (*genParticles).at(i);
	int id = p.pdgId();

	bool hasRadiation = false;
	bool hasLepton = false;
	  
	if(abs(id) == 23 || abs(id) == 24 || abs(id) == 25 || abs(id) == 6){
	    
	  size_t nDs = p.numberOfDaughters();
	  for(size_t j = 0; j < nDs; j++){
	    int dauId = (p.daughter(j))->pdgId();
	    const reco::Candidate *d = p.daughter(j);
	    if(d->pdgId() != dauId) std::cout << "making daughter GenParticle didn't work" << std::endl;
	    
	    if(abs(dauId) == abs(id)) hasRadiation = true;
	    else if(abs(dauId) == 24){  // check t->Wb->leptons and H->WW->leptons
	      while(d->numberOfDaughters() == 1) d = d->daughter(0);
	      if(abs(d->daughter(0)->pdgId()) > 10 && abs(d->daughter(0)->pdgId()) < 17) hasLepton = true;
	      if(abs(d->daughter(1)->pdgId()) > 10 && abs(d->daughter(1)->pdgId()) < 17) hasLepton = true;
	    }
	    else if(abs(dauId) == 23){  // check H->ZZ->leptons
	      while(d->numberOfDaughters() == 1) d = d->daughter(0);
	      if(abs(d->daughter(0)->pdgId()) > 10 && abs(d->daughter(0)->pdgId()) < 17) hasLepton = true;
	      if(abs(d->daughter(1)->pdgId()) > 10 && abs(d->daughter(1)->pdgId()) < 17) hasLepton = true;
	    }
	    else if(abs(dauId) > 10 && abs(dauId) < 17) hasLepton = true;	    
	    
	  }
	  
	  if(hasRadiation) continue;	  
	  if(hasLepton) continue;	  
	  if(p.pt() < 175) continue;
	  
	  if(abs(id) == 24){
	    double dRWb = 1000;
	    double dRWW = 1000;
	    
	    const reco::Candidate *mother = p.mother();
	    while(abs(mother->pdgId()) == 24) mother = mother->mother();
	    
	    if(abs(mother->pdgId()) == 6){
	      double dr = reco::deltaR(p.p4(),mother->daughter(1)->p4());
	      if(abs(mother->daughter(1)->pdgId()) == 24) dr = reco::deltaR(p.p4(),mother->daughter(0)->p4());
	      if(dr < dRWb) dRWb = dr;
	    }else if(abs(mother->pdgId()) == 25){
	      double dr = 1000;
	      if(p.pdgId()*mother->daughter(0)->pdgId() > 0){
		dr = reco::deltaR(p.p4(),mother->daughter(1)->p4());
	      }else{
		dr = reco::deltaR(p.p4(),mother->daughter(0)->p4());
	      }
	      if(dr < dRWW) dRWW = dr;
	    }		
	    
	    if(dRWW < 0.8) continue; // W from merged H
	    if(dRWb < 0.8) continue; // W from merged t
	  }
	  
	  if(abs(id) == 23){
	    double dRZZ = 1000;
	    
	    const reco::Candidate *mother = p.mother();
	    while(abs(mother->pdgId()) == 23) mother = mother->mother();
	    
	    if(abs(mother->pdgId()) == 25){
	      double dr = 1000;
	      if(p.pdgId()*mother->daughter(0)->pdgId() > 0){
		dr = reco::deltaR(p.p4(),mother->daughter(1)->p4());
	      }else{
		dr = reco::deltaR(p.p4(),mother->daughter(0)->p4());
	      }
	      if(dr < dRZZ) dRZZ = dr;
	    }
	    
	    if(dRZZ < 0.8) continue; // Z from merged H
	  }
	  
	  if(p.numberOfDaughters() < 2){
	    std::cout << p.numberOfDaughters() << " daughters from " << p.pdgId() << std::endl;
	    continue;
	  }

	  HadronicVHtStatus.push_back( p.status() );
	  HadronicVHtID.push_back( p.pdgId() );
	  HadronicVHtPt.push_back( p.pt() );
	  HadronicVHtEta.push_back( p.eta() );
	  HadronicVHtPhi.push_back( p.phi() );
	  HadronicVHtEnergy.push_back( p.energy() );
	  
	  if(abs(id) != 6){
	    HadronicVHtD0Pt.push_back( p.daughter(0)->pt());
	    HadronicVHtD0Eta.push_back( p.daughter(0)->eta());
	    HadronicVHtD0Phi.push_back( p.daughter(0)->phi());
	    HadronicVHtD0E.push_back( p.daughter(0)->energy());
	    HadronicVHtD1Pt.push_back( p.daughter(1)->pt());	    
	    HadronicVHtD1Eta.push_back( p.daughter(1)->eta());
	    HadronicVHtD1Phi.push_back( p.daughter(1)->phi());
	    HadronicVHtD1E.push_back( p.daughter(1)->energy());
	    HadronicVHtD2Pt.push_back(-99.9);
	    HadronicVHtD2Eta.push_back(-99.9);
	    HadronicVHtD2Phi.push_back(-99.9);
	    HadronicVHtD2E.push_back(-99.9);
	  }else{
	    const reco::Candidate *W = p.daughter(0);
	    const reco::Candidate *b = p.daughter(1);
	    if(fabs(W->pdgId()) != 24){
	      W = p.daughter(1);
	      b = p.daughter(0);
	    }
	    while(W->numberOfDaughters() == 1) W = W->daughter(0);
	    HadronicVHtD0Pt.push_back( b->pt());
	    HadronicVHtD0Eta.push_back( b->eta());
	    HadronicVHtD0Phi.push_back( b->phi());
	    HadronicVHtD0E.push_back( b->energy());
	    HadronicVHtD1Pt.push_back( W->daughter(0)->pt());
	    HadronicVHtD2Pt.push_back( W->daughter(1)->pt());
	    HadronicVHtD1Eta.push_back( W->daughter(0)->eta());
	    HadronicVHtD2Eta.push_back( W->daughter(1)->eta());
	    HadronicVHtD1Phi.push_back( W->daughter(0)->phi());
	    HadronicVHtD2Phi.push_back( W->daughter(1)->phi());
	    HadronicVHtD1E.push_back( W->daughter(0)->energy());
	    HadronicVHtD2E.push_back( W->daughter(1)->energy());
	  }
	}
      }
    }

    SetValue("HadronicVHtStatus",HadronicVHtStatus);
    SetValue("HadronicVHtID",HadronicVHtID);
    SetValue("HadronicVHtPt",HadronicVHtPt);
    SetValue("HadronicVHtEta",HadronicVHtEta);
    SetValue("HadronicVHtPhi",HadronicVHtPhi);
    SetValue("HadronicVHtEnergy",HadronicVHtEnergy);
    SetValue("HadronicVHtD0Pt",HadronicVHtD0Pt);
    SetValue("HadronicVHtD0Eta",HadronicVHtD0Eta);
    SetValue("HadronicVHtD0Phi",HadronicVHtD0Phi);
    SetValue("HadronicVHtD0E",HadronicVHtD0E);
    SetValue("HadronicVHtD1Pt",HadronicVHtD1Pt);
    SetValue("HadronicVHtD1Eta",HadronicVHtD1Eta);
    SetValue("HadronicVHtD1Phi",HadronicVHtD1Phi);
    SetValue("HadronicVHtD1E",HadronicVHtD1E);
    SetValue("HadronicVHtD2Pt",HadronicVHtD2Pt);
    SetValue("HadronicVHtD2Eta",HadronicVHtD2Eta);
    SetValue("HadronicVHtD2Phi",HadronicVHtD2Phi);
    SetValue("HadronicVHtD2E",HadronicVHtD2E);

    return 0;
}

int JetSubCalc::EndJob()
{
  delete jecUnc;
  delete jecak8;
  delete L3JetParAK8MC;
  delete L2JetParAK8MC;
  delete ResJetParAK8MC; 
  delete L3JetParAK8BCD;
  delete L2JetParAK8BCD;
  delete ResJetParAK8BCD; 
  delete L3JetParAK8EF;
  delete L2JetParAK8EF;
  delete ResJetParAK8EF; 
  delete L3JetParAK8G;
  delete L2JetParAK8G;
  delete ResJetParAK8G; 
  delete L3JetParAK8H;
  delete L2JetParAK8H;
  delete ResJetParAK8H; 
  return 0;
}
