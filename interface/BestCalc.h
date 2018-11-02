#ifndef LJMet_Com_interface_BestCalc_h
#define LJMet_Com_interface_BestCalc_h

/*
 Best class for all calculators
 
 Author: Gena Kukartsev, 2012
 */

#include <iostream>
#include <vector>

#include "LJMet/Com/interface/BaseCalc.h"
#include "LJMet/Com/interface/LjmetEventContent.h"
#include "LJMet/Com/interface/LjmetFactory.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
//#include "LJMet/Com/interface/VVString.h"

#include <fstream>

// FASTJET
#include <fastjet/JetDefinition.hh>
#include <fastjet/PseudoJet.hh>
#include <fastjet/tools/Filter.hh>
#include <fastjet/ClusterSequence.hh>
#include <fastjet/GhostedAreaSpec.hh>
#include <fastjet/ClusterSequenceArea.hh>

// CMS
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "PhysicsTools/CandUtils/interface/EventShapeVariables.h"
#include "PhysicsTools/CandUtils/interface/Thrust.h"

// ROOT
#include "TLorentzRotation.h"
#include "TLorentzVector.h"
#include "TFile.h"

// lwtnn
#include "lwtnn/lwtnn/interface/LightweightNeuralNetwork.hh"
#include "lwtnn/lwtnn/interface/parse_json.hh"


using namespace std;

class LjmetFactory;

class BestCalc : public BaseCalc {
    //
    // Best class for all calculators
    //
    //

    
public:
    BestCalc();
    virtual ~BestCalc() { }
    BestCalc(const BestCalc &); // stop default
    std::string GetName() { return mName; }
    virtual int BeginJob();
    virtual int ProduceEvent(edm::EventBase const & event, BaseEventSelector * selector) { return 0; }
    virtual int AnalyzeEvent(edm::EventBase const & event, BaseEventSelector * selector);
    virtual int EndJob();
    
    std::map<std::string,double> execute( const pat::Jet& jet );

    void getJetValues( const pat::Jet& jet );

    void pboost( TVector3 pbeam, TVector3 plab, TLorentzVector &pboo );

    void FWMoments( std::vector<TLorentzVector> particles, double (&outputs)[5] );

    float LegP(float x, int order);

    unsigned int getParticleID();

    void setConfigurations(const std::vector<std::string>& configurations);

    void read_file( const std::string &file_name, std::vector<std::string> &values, const std::string &comment="#" );

    bool str2bool( const std::string value );

    std::string mName;
    std::string mLegend;
    
 private:
    // lwtnn
    lwt::LightweightNeuralNetwork* m_lwtnn;
    std::map<std::string,double> m_BESTvars;
    std::map<std::string,double> m_NNresults;

    std::string m_dnnFile;

    std::map<std::string,std::string> m_configurations; // map of configurations

    // kinematics
    float m_jetSoftDropMassMin; // [GeV] Jet soft drop mass minimum
    float m_jetPtMin;           // [GeV] Jet pT minimum
    unsigned int m_numSubjetsMin;    // minimum number of subjets
    unsigned int m_numDaughtersMin;  // minimum number of daughters

    // boosting to rest frames
    float m_radiusSmall;        // re-clustering jets
    float m_radiusLarge;        // re-clustering jets
    float m_reclusterJetPtMin;  // [GeV] re-clustering jet pT minimum

    float m_jetChargeKappa;     // weight for jet charge pT
    size_t m_maxJetSize;        // number of jets in re-clustering

    float m_Wmass = 80.4;       // W mass [GeV]
    float m_Zmass = 91.2;       // Z mass
    float m_Hmass = 125.;       // Higgs mass
    float m_Tmass = 172.5;      // Top mass

    std::map<std::string,std::string> m_defaultConfigs = {
      {"dnnFile",             "BESTAnalysis/BoostedEventShapeTagger/data/BEST_mlp.json"},
      {"radiusSmall",         "0.4"},
      {"radiusLarge",         "0.8"},
      {"reclusterJetPtMin",   "30.0"},
      {"jetSoftDropMassMin",  "40.0"},
      {"jetPtMin",            "500.0"},
      {"jetChargeKappa",      "0.6"},
      {"maxJetSize",          "4"},
      {"numSubjetsMin",       "2"},
      {"numDaughtersMin",     "2"} };    

};

#endif
