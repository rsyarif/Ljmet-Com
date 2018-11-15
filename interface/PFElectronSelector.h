#ifndef PhysicsTools_PatUtils_interface_PFElectronSelector_h
#define PhysicsTools_PatUtils_interface_PFElectronSelector_h

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include <iostream>

class PFElectronSelector : public Selector<pat::Electron> {
    
public: // interface
    
    bool verbose_;
    
    enum Version_t { SPRING11, MOD, N_VERSIONS };
    
    PFElectronSelector() {}
    
    PFElectronSelector( edm::ParameterSet const & parameters ) {
        
        verbose_ = false;
        
        std::string versionStr = parameters.getParameter<std::string>("version");
        
        Version_t version = N_VERSIONS;
        
        if ( versionStr == "SPRING11" ) {
            version = SPRING11;
        }
        else if ( versionStr == "MOD" ) {
            version = MOD;
        }
        else {
            throw cms::Exception("InvalidInput") << "Expect version to be one of SPRING11, MOD" << std::endl;
        }
        
        
        initialize( version,
                   parameters.getParameter<double>("MVA"),
                   parameters.getParameter<double>("D0")  ,
                   parameters.getParameter<double>("DZ")  ,
                   parameters.getParameter<int>   ("MaxMissingHits"),
                   parameters.getParameter<double>   ("MaxSCEta"),
                   parameters.getParameter<double>   ("MinSCEta"),
                   parameters.getParameter<std::string> ("electronIDused"),
                   parameters.getParameter<bool>  ("ConversionRejection"),
                   parameters.getParameter<double>("PFIso")
                   );
        if ( parameters.exists("cutsToIgnore") )
            setIgnoredCuts( parameters.getParameter<std::vector<std::string> >("cutsToIgnore") );
        
        retInternal_ = getBitTemplate();
        
    }
    
    void initialize( Version_t version,
                    double mva = 0.4,
                    double d0 = 0.02,
                    double dZ = 0.1,
                    int nMissingHits = 1,
                    double maxsceta = 1.5660,
                    double minsceta = 1.4442,
                    std::string eidUsed = "eidTight",
                    bool convRej = true,
                    double pfiso = 0.15 )
    {
        version_ = version;
        
        //    size_t found;
        //    found = eidUsed.find("NONE");
        //  if ( found != std::string::npos)
        electronIDvalue_ = eidUsed;
        
        push_back("MVA",       mva   );
        push_back("D0",        d0     );
        push_back("DZ",        dZ     );
        push_back("MaxMissingHits", nMissingHits  );
        push_back("MaxSCEta", maxsceta  );
        push_back("MinSCEta", minsceta  );
        push_back("electronID");
        push_back("ConversionRejection" );
        push_back("PFIso",    pfiso );
        
        set("MVA");
        set("D0");
        set("DZ");
        set("MaxMissingHits");
        set("MaxSCEta");
        set("MinSCEta");
        set("electronID");
        set("ConversionRejection", convRej);
        set("PFIso");
        
        indexMVA_            = index_type(&bits_, "MVA"         );
        indexD0_             = index_type(&bits_, "D0"           );
        indexDZ_             = index_type(&bits_, "DZ"           );
        indexMaxMissingHits_ = index_type(&bits_, "MaxMissingHits" );
        indexMaxSCEta_       = index_type(&bits_, "MaxSCEta" );
        indexMinSCEta_       = index_type(&bits_, "MinSCEta" );
        indexElectronId_     = index_type(&bits_, "electronID" );
        indexConvRej_        = index_type(&bits_, "ConversionRejection" );
        indexPFIso_          = index_type(&bits_, "PFIso"       );
    }
    
    // Allow for multiple definitions of the cuts.
    bool operator()( const pat::Electron & electron, pat::strbitset & ret )
    {
        if (version_ == SPRING11 ) return spring11Cuts(electron, ret);
        else if (version_ == MOD ) return modCuts(electron, ret);
        else {
            return false;
        }
    }
    
    using Selector<pat::Electron>::operator();
    
    bool modCuts( const pat::Electron & electron, pat::strbitset & ret)
    {
        
        ret.set(false);
        
        double missingHits = electron.gsfTrack()->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);
        double sceta = fabs(electron.superCluster()->eta());
        bool passconversion = electron.passConversionVeto();
        double mva = electron.mva_e_pi();
        
        
        if ( missingHits   <= cut(indexMaxMissingHits_,  double()) || ignoreCut(indexMaxMissingHits_)   ) passCut(ret, indexMaxMissingHits_  );
        //else std::cout<<"fail missingHits "<<missingHits<<std::endl;
        if ( fabs(sceta) < cut(indexMinSCEta_,  double()) || fabs(sceta) > cut(indexMaxSCEta_, double()) || ( ignoreCut(indexMinSCEta_) && ignoreCut(indexMinSCEta_) ) ) {
            passCut(ret, indexMinSCEta_  );
            passCut(ret, indexMaxSCEta_  );
        }
        //else std::cout<<"fail SCEta "<<sceta<<std::endl;
        if ( passconversion                                        || ignoreCut(indexConvRej_)          ) passCut(ret, indexConvRej_     );
        //else std::cout<<"fail passconversion "<<passconversion<<std::endl;
        if ( mva           >  cut(indexMVA_,             double()) || ignoreCut(indexMVA_)              ) passCut(ret, indexMVA_ );
        //else std::cout<<"fail mva "<<mva<<std::endl;
        passCut(ret, indexD0_);
        passCut(ret, indexDZ_);
        passCut(ret, indexElectronId_);
        passCut(ret, indexPFIso_);
        setIgnored(ret);
        return (bool)ret;
    }
    
    // cuts based on top group L+J synchronization exercise
    bool spring11Cuts( const pat::Electron & electron, pat::strbitset & ret)
    {
        
        ret.set(false);
        
        double mva = electron.mva_e_pi();
        double missingHits = electron.gsfTrack()->hitPattern().numberOfAllHits(reco::HitPattern::MISSING_INNER_HITS);
        double corr_d0 = electron.dB();
        
        // in >= 39x conversion rejection variables are accessible from Gsf electron
        Double_t dist = electron.convDist(); // default value is -9999 if conversion partner not found
        Double_t dcot = electron.convDcot(); // default value is -9999 if conversion partner not found
        bool isNotConv = !(fabs(dist) < 0.02 && fabs(dcot) < 0.02);
        
        int bitWiseResults =  (int) electron.electronID( electronIDvalue_ );
        bool electronIDboolean = ((bitWiseResults & 1) == 1 );
        
        double chIso = electron.userIsolation(pat::PfChargedHadronIso);
        double nhIso = electron.userIsolation(pat::PfNeutralHadronIso);
        double gIso  = electron.userIsolation(pat::PfGammaIso);
        double et    = electron.et() ;
        
        double pfIso = (chIso + nhIso + gIso) / et;
        
        if ( missingHits   <= cut(indexMaxMissingHits_,  double()) || ignoreCut(indexMaxMissingHits_)   ) passCut(ret, indexMaxMissingHits_  );
        if ( fabs(corr_d0) <  cut(indexD0_,              double()) || ignoreCut(indexD0_)               ) passCut(ret, indexD0_     );
        if ( isNotConv                                             || ignoreCut(indexConvRej_)          ) passCut(ret, indexConvRej_     );
        if ( pfIso         <  cut(indexPFIso_,           double()) || ignoreCut(indexPFIso_)            ) passCut(ret, indexPFIso_ );
        if ( mva           >  cut(indexMVA_,             double()) || ignoreCut(indexMVA_)              ) passCut(ret, indexMVA_ );
        if ( electronIDboolean                                     || ignoreCut(indexElectronId_)       ) passCut(ret, indexElectronId_);
        setIgnored(ret);
        return (bool)ret;
    }
    
private: // member variables
    
    Version_t version_;
    
    index_type indexID;
    index_type indexMaxMissingHits_;
    index_type indexMaxSCEta_;
    index_type indexMinSCEta_;
    index_type indexD0_;
    index_type indexDZ_;
    index_type indexConvRej_;
    index_type indexPFIso_;
    index_type indexMVA_;
    index_type indexElectronId_;
    
    std::string electronIDvalue_;
};

#endif
