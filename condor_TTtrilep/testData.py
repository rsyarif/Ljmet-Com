import FWCore.ParameterSet.Config as cms
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes
import os
# Define the base process
process = cms.Process("LJMetCom")

#Arguments from condor submit script which are used more than once
condorIsMC = bool(False)
relBase    = os.environ['CMSSW_BASE']
condorJSON = str('Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt')
############################################################
#
# FWLite application options
process.load('LJMet.Com.ljmet_cfi')
process.ljmet.isMc = cms.bool(condorIsMC)

# Exclude some unnecessary calculators from the process
process.ljmet.excluded_calculators = cms.vstring(
    'DeepAK8Calc',
    'BestCalc',
    'PileUpCalc',
    'BTagSFCalc',
    'TprimeCalc',
    'CATopoCalc',
    'DileptonCalc',
    'DileptonEventSelector',
    'StopCalc',
    'PdfCalc',
    'ChargedHiggsCalc',
    'LjetsTopoCalc',
    'WprimeCalc'
    ) 

# common calculator options
process.load('LJMet.Com.commonCalc_cfi')

# BestCalc options
process.load('LJMet.Com.BestCalc_cfi')
process.BestCalc.dnnFile = cms.string(relBase+'/src/LJMet/Com/data/BEST_mlp.json')

# singleLep calculator options
process.load('LJMet.Com.singleLepCalc_cfi')
process.singleLepCalc.isMc              = cms.bool(condorIsMC)
process.singleLepCalc.keepFullMChistory = cms.bool(condorIsMC)
process.singleLepCalc.UseElMVA          = cms.bool(True)
process.singleLepCalc.UseElIDV1         = cms.bool(False)
process.singleLepCalc.saveLooseLeps     = cms.bool(True)
process.singleLepCalc.saveGenHT     = cms.bool(False)
process.singleLepCalc.OverrideLHEWeights = cms.bool(True)
process.singleLepCalc.triggerCollection = cms.InputTag("TriggerResults::HLT")

# Jet substructure calculator options
process.load('LJMet.Com.JetSubCalc_cfi')
process.JetSubCalc.killHF = cms.bool(False)
process.JetSubCalc.isMc = cms.bool(condorIsMC)


############################################################
#
# Event selector options
#
process.event_selector = cms.PSet(
    
    selection = cms.string('singleLepSelector'),
    
    # Define cuts -- variable names are strings searched by src/singleLepEventSelector.cc
    
    debug  = cms.bool(True),
    
    isMc  = cms.bool(condorIsMC),
    keepFullMChistory = cms.bool(condorIsMC),
    doLaserCalFilt  = cms.bool(False),
    
    # Trigger cuts
    trigger_cut  = cms.bool(True),
    dump_trigger = cms.bool(True),

    trigger_path_el = cms.vstring(        
        'HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf_v',            
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v', #exists in 2017        
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v',  #exists in 2017    
        'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v',        
        'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_v',           
        'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT300_v',    
        'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT250_v',    
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v',   #exists in 2017 
		'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ', #exists in 2017 
        'HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v',   
        'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v',  
        'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ_v',  
        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v', #exists in 2017  
        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v',  #exists in 2017 
        'HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v',  
        'HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v',                
        'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT300_v',      
        'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT250_v',      
        'HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v',            
        'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v',                 
        'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v',                  
        ),
    trigger_path_mu = cms.vstring(
        'HLT_DoubleIsoMu17_eta2p1_v',                         
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8', 
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v', #exists in 2017  (PreScaled!)               
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v',  #exists in 2017   (PreScaled!)               
        'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v',            
        'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v',               
        'HLT_Mu27_TkMu8_v',                                   
        'HLT_Mu30_TkMu11_v',                                  
        'HLT_Mu40_TkMu11_v',                                  
        'HLT_Mu17_Mu8_v',                                     
        'HLT_Mu17_Mu8_DZ_v',                                  
        'HLT_Mu17_Mu8_SameSign_DZ_v',                         
        'HLT_Mu20_Mu10_v',                                    
        'HLT_Mu20_Mu10_DZ_v',                                 
        'HLT_Mu20_Mu10_SameSign_DZ_v',                        
        'HLT_DoubleMu8_Mass8_PFHT300_v',                      
        'HLT_DoubleMu8_Mass8_PFHT250_v',                      
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v',   #exists in 2017 (PreScaled!)
		'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ', #exists in 2017 
        'HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v',   
        'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v',  
        'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ_v',  
        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v',  #exists in 2017 
        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v',  #exists in 2017 
        'HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v',  
        'HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v',                
        'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT300_v',      
        'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT250_v',      
        'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v',                 
        'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v',                  
        'HLT_TripleMu_12_10_5_v',
        ),
    
    mctrigger_path_el = cms.vstring(''),
    mctrigger_path_mu = cms.vstring(''),   
    
    # PV cuts
    pv_cut         = cms.bool(True),
    flag_tag       = cms.InputTag('TriggerResults::RECO'),
    metfilters     = cms.bool(True),
    
    # Jet cuts
    jet_cuts                 = cms.bool(True),
    jet_minpt                = cms.double(30.0),
    jet_maxeta               = cms.double(2.5),
    jet_minpt_AK8            = cms.double(200.0),
    jet_maxeta_AK8           = cms.double(2.4),
    min_jet                  = cms.int32(1),
    max_jet                  = cms.int32(4000),
    leading_jet_pt           = cms.double(30.0),

    # muon cuts
    muon_cuts                = cms.bool(True),
    min_muon                 = cms.int32(0),
    muon_minpt               = cms.double(20.0),
    muon_maxeta              = cms.double(2.4),
    muon_useMiniIso          = cms.bool(True),
    muon_miniIso             = cms.double(999.9),
    loose_muon_miniIso       = cms.double(999.9),
    loose_muon_minpt         = cms.double(20.0),
    loose_muon_maxeta        = cms.double(2.4),
    # specify IP cuts
    muon_dxy                 = cms.double(0.2),
    muon_dz                  = cms.double(0.5),
    loose_muon_dxy           = cms.double(999999.),
    loose_muon_dz            = cms.double(999999.),
 
    # electron cuts
    electron_cuts            = cms.bool(True),
    min_electron             = cms.int32(0),
    electron_minpt           = cms.double(20.0),
    electron_maxeta          = cms.double(2.4),
    electron_useMiniIso      = cms.bool(True),
    electron_miniIso         = cms.double(0.1),
    loose_electron_miniIso   = cms.double(0.4),
    loose_electron_minpt     = cms.double(20.0),
    loose_electron_maxeta    = cms.double(2.4),
    UseElMVA                 = cms.bool(True),
    UseElIDV1                = cms.bool(False),
 
    # more lepton cuts
    min_lepton               = cms.int32(0),    # checks (N tight mu + N tight el) >= cut
    max_lepton               = cms.int32(1000),    # checks (N tight mu + N tight el) <= cut
    min_loose_lepton         = cms.int32(3),
    max_loose_lepton         = cms.int32(1000),
    second_lepton_veto       = cms.bool(False),  #checks (N tight lep > 0) AND (N loose lep > 0), vetoes if there are loose leptons.
    tau_veto		     = cms.bool(False),
    
    # MET cuts
    met_cuts                 = cms.bool(True),
    min_met                  = cms.double(30.0),
    max_met                  = cms.double(99999999999.0),
    
    # Btagging cuts
    btagOP                   = cms.string('MEDIUM'),
    bdisc_min                = cms.double(0.4941),
    DeepCSVfile              = cms.string(relBase+'/src/LJMet/Com/data/DeepCSV_94XSF_V3_B_F.csv'),
    DeepCSVSubjetfile        = cms.string(relBase+'/src/LJMet/Com/data/subjet_DeepCSV_94XSF_V3_B_F.csv'),
    btag_cuts                = cms.bool(False),
    btag_1                   = cms.bool(False),
    btag_2                   = cms.bool(False),
    btag_3                   = cms.bool(False),
    
    # Define the branch names of object collections in the input miniAOD file
    trigger_collection       = cms.InputTag('TriggerResults::HLT'),
    pv_collection            = cms.InputTag('offlineSlimmedPrimaryVertices'),
    jet_collection           = cms.InputTag('slimmedJets'),
    slimmedJetsAK8           = cms.InputTag('packedJetsAK8Puppi'), #'slimmedJetsAK8'),#
    muon_collection          = cms.InputTag('slimmedMuons'),
    electron_collection      = cms.InputTag('slimmedElectrons::PATtest'), #'slimmedElectrons'), #
    tau_collection	     = cms.InputTag('slimmedTaus'),
    met_collection           = cms.InputTag('slimmedMETs'),
    
    # Jet corrections are read from txt files which need updating!
    JEC_txtfile = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFchs.txt'),
    JERSF_txtfile = cms.string(relBase+'/src/LJMet/Com/data/Fall17V3/Fall17_V3_MC_SF_AK4PFchs.txt'),
    JER_txtfile = cms.string(relBase+'/src/LJMet/Com/data/Fall17V3/Fall17_V3_MC_PtResolution_AK4PFchs.txt'),
    JERAK8_txtfile = cms.string(relBase+'/src/LJMet/Com/data/Fall17V3/Fall17_V3_MC_PtResolution_AK8PFPuppi.txt'),

    JECup                    = cms.bool(False),
    JECdown                  = cms.bool(False),
    JERup                    = cms.bool(False),
    JERdown                  = cms.bool(False),
    doNewJEC                 = cms.bool(True),
    doLepJetCleaning         = cms.bool(True),
    CleanLooseLeptons        = cms.bool(True),
    LepJetDR                 = cms.double(0.4),
    LepJetDRAK8              = cms.double(0.8),
    
    MCL1JetPar               = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017_V32_MC_L1FastJet_AK4PFchs.txt'),
    MCL2JetPar               = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017_V32_MC_L2Relative_AK4PFchs.txt'),
    MCL3JetPar               = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017_V32_MC_L3Absolute_AK4PFchs.txt'),

    MCL1JetParAK8            = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017_V32_MC_L1FastJet_AK8PFPuppi.txt'),
    MCL2JetParAK8            = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017_V32_MC_L2Relative_AK8PFPuppi.txt'),
    MCL3JetParAK8            = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017_V32_MC_L3Absolute_AK8PFPuppi.txt'),

    DataL1JetPar             = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L1FastJet_AK4PFchs.txt'),
    DataL2JetPar             = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L2Relative_AK4PFchs.txt'),
    DataL3JetPar             = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L3Absolute_AK4PFchs.txt'),
    DataResJetPar            = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L2L3Residual_AK4PFchs.txt'),

    DataL1JetParAK8          = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L1FastJet_AK8PFPuppi.txt'),
    DataL2JetParAK8          = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L2Relative_AK8PFPuppi.txt'),
    DataL3JetParAK8          = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L3Absolute_AK8PFPuppi.txt'),
    DataResJetParAK8         = cms.string(relBase+'/src/LJMet/Com/data/Fall17V32/Fall17_17Nov2017B_V32_DATA_L2L3Residual_AK8PFPuppi.txt'),

    # Unused parameters
    muon_reliso              = cms.double(0.2),
    muon_selector_medium     = cms.bool(False),
    loose_muon_selector_tight = cms.bool(False),
    loose_muon_reliso        = cms.double(0.4),
    BTagUncertUp             = cms.bool(False), # no longer needed
    BTagUncertDown           = cms.bool(False), # no longer needed
 
    )


#######################################################
#
# Input files
#

process.inputs = cms.PSet (
    nEvents    = cms.int32(5000),
#     nEvents    = cms.int32(-1),
    skipEvents = cms.int32(0),
    lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange()),
    fileNames  = cms.vstring(
		'root://cmsxrootd.fnal.gov//store/data/Run2017F/DoubleEG/MINIAOD/09May2018-v1/10000/444E03EB-B75F-E811-AFBA-F01FAFD8F16A.root',
		)

    )


# JSON
if (not process.ljmet.isMc==cms.bool(True)):
    JsonFile = relBase+'/src/LJMet/Com/data/json/'+condorJSON
    myList   = LumiList.LumiList(filename=JsonFile).getCMSSWString().split(',')
    process.inputs.lumisToProcess.extend(myList)
    
    
#######################################################
#
# Output
#
process.outputs = cms.PSet (
#     outputName = cms.string('testdata'),
    outputName = cms.string('DoubleEG_Run2017F_v2_testData'),
    treeName   = cms.string('ljmet'),
    )

#######################################################
#
# Object selector options
#
# Primary vertex
process.load('PhysicsTools.SelectorUtils.pvSelector_cfi')
process.pvSelector.pvSrc   = cms.InputTag('offlineSlimmedPrimaryVertices')
process.pvSelector.minNdof = cms.double(4.0)
process.pvSelector.maxZ    = cms.double(24.0)
process.pvSelector.maxRho  = cms.double(2.0)




