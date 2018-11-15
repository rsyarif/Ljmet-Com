import FWCore.ParameterSet.Config as cms
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes

# Define the base process
process = cms.Process("LJMetCom")

#Arguments from condor submit script which are used more than once
condorIsMC = bool(CONDOR_ISMC)
relBase    = str('CONDOR_RELBASE')
condorJSON = str('CONDOR_JSON')
############################################################
#
# FWLite application options
process.load('LJMet.Com.ljmet_cfi')
process.ljmet.isMc = cms.bool(condorIsMC)

# Exclude some unnecessary calculators from the process
process.ljmet.excluded_calculators = cms.vstring(
    'TpTpCalc',
    'JetSubCalc',
    'TTbarMassCalc',
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

# singleLep calculator options
process.load('LJMet.Com.singleLepCalc_cfi')
process.singleLepCalc.isMc              = cms.bool(condorIsMC)
process.singleLepCalc.keepFullMChistory = cms.bool(condorIsMC)
process.singleLepCalc.UseElMVA          = cms.bool(True)
process.singleLepCalc.saveLooseLeps     = cms.bool(False)

############################################################
#
# Event selector options
#
process.event_selector = cms.PSet(
    
    selection = cms.string('singleLepSelector'),
    
    # Define cuts -- variable names are strings searched by src/singleLepEventSelector.cc
    
    debug  = cms.bool(False),
    
    isMc  = cms.bool(condorIsMC),
    keepFullMChistory = cms.bool(condorIsMC),
    doLaserCalFilt  = cms.bool(False),
    
    # Trigger cuts
    trigger_cut  = cms.bool(True),
    dump_trigger = cms.bool(False),

    trigger_path_el = cms.vstring(
        'HLT_Ele32_eta2p1_WPTight_Gsf_v1', 'HLT_Ele32_eta2p1_WPTight_Gsf_v2', 'HLT_Ele32_eta2p1_WPTight_Gsf_v3', 
        'HLT_Ele32_eta2p1_WPTight_Gsf_v4', 'HLT_Ele32_eta2p1_WPTight_Gsf_v5', 'HLT_Ele32_eta2p1_WPTight_Gsf_v6', 
        'HLT_Ele32_eta2p1_WPTight_Gsf_v7', 'HLT_Ele32_eta2p1_WPTight_Gsf_v8', 
        'HLT_Ele32_WPTight_Gsf_v1', 'HLT_Ele32_WPTight_Gsf_v2', 'HLT_Ele32_WPTight_Gsf_v3', 
        'HLT_Ele32_WPTight_Gsf_v4', 'HLT_Ele32_WPTight_Gsf_v5', 'HLT_Ele32_WPTight_Gsf_v6', 
        'HLT_Ele32_WPTight_Gsf_v7', 'HLT_Ele32_WPTight_Gsf_v8', 
        'HLT_Ele30_WPTight_Gsf_v1', 'HLT_Ele30_WPTight_Gsf_v2', 'HLT_Ele30_WPTight_Gsf_v3', 
        'HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v1', 'HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v2', 'HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v3', 
        'HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v4', 'HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v5', 'HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v6', 
        'HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v7', 'HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v8', 'HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v9',
        'HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v10', 
        'HLT_Ele15_IsoVVVL_PFHT350_v1', 'HLT_Ele15_IsoVVVL_PFHT350_v2', 'HLT_Ele15_IsoVVVL_PFHT350_v3',
        'HLT_Ele15_IsoVVVL_PFHT350_v4', 'HLT_Ele15_IsoVVVL_PFHT350_v5', 'HLT_Ele15_IsoVVVL_PFHT350_v6',
        'HLT_Ele15_IsoVVVL_PFHT400_v1', 'HLT_Ele15_IsoVVVL_PFHT400_v2', 'HLT_Ele15_IsoVVVL_PFHT400_v3',
        'HLT_Ele15_IsoVVVL_PFHT400_v4', 'HLT_Ele15_IsoVVVL_PFHT400_v5', 'HLT_Ele15_IsoVVVL_PFHT400_v6',
        'HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v3', 'HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v4',
        'HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v5', 'HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v6',
        'HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v7', 'HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v8', 
        'HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v9',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v1', 'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v2', 'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v3',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v4', 'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v5', 'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v6',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v7',
        'HLT_PFHT900_v1', 'HLT_PFHT900_v2', 'HLT_PFHT900_v3', 'HLT_PFHT900_v4', 'HLT_PFHT900_v5', 'HLT_PFHT900_v6',
        'HLT_PFHT600_v3', 'HLT_PFHT600_v4', 'HLT_PFHT600_v5', 'HLT_PFHT600_v6', 'HLT_PFHT600_v7', 'HLT_PFHT600_v8',
        ),
    trigger_path_mu = cms.vstring(
        'HLT_IsoMu24_v1', 'HLT_IsoMu24_v2', 'HLT_IsoMu24_v3', 'HLT_IsoMu24_v4',
        'HLT_IsoTkMu24_v1', 'HLT_IsoTkMu24_v2', 'HLT_IsoTkMu24_v3', 'HLT_IsoTkMu24_v4',
        'HLT_IsoMu24_v3', 'HLT_IsoMu24_v4', 'HLT_IsoMu24_v5', 'HLT_IsoMu24_v6', 'HLT_IsoMu24_v7',
        'HLT_IsoTkMu24_v3', 'HLT_IsoTkMu24_v4', 'HLT_IsoTkMu24_v5', 'HLT_IsoTkMu24_v6', 'HLT_IsoTkMu24_v7',         
        'HLT_Mu50_v1', 'HLT_Mu50_v2', 'HLT_Mu50_v3', 'HLT_Mu50_v4', 'HLT_Mu50_v5',
        'HLT_TkMu50_v1', 'HLT_TkMu50_v2', 'HLT_TkMu50_v3', 'HLT_TkMu50_v4', 'HLT_TkMu50_v5',
        'HLT_Mu15_IsoVVVL_PFHT400_v1', 'HLT_Mu15_IsoVVVL_PFHT400_v2', 'HLT_Mu15_IsoVVVL_PFHT400_v3',
        'HLT_Mu15_IsoVVVL_PFHT400_v4', 'HLT_Mu15_IsoVVVL_PFHT400_v5', 'HLT_Mu15_IsoVVVL_PFHT400_v6',
        'HLT_Mu15_IsoVVVL_PFHT350_v1', 'HLT_Mu15_IsoVVVL_PFHT350_v2', 'HLT_Mu15_IsoVVVL_PFHT350_v3',
        'HLT_Mu15_IsoVVVL_PFHT350_v4', 'HLT_Mu15_IsoVVVL_PFHT350_v5', 'HLT_Mu15_IsoVVVL_PFHT350_v6',
        'HLT_Mu40_eta2p1_PFJet200_PFJet50_v1', 'HLT_Mu40_eta2p1_PFJet200_PFJet50_v2', 'HLT_Mu40_eta2p1_PFJet200_PFJet50_v3',
        'HLT_Mu40_eta2p1_PFJet200_PFJet50_v4', 'HLT_Mu40_eta2p1_PFJet200_PFJet50_v5', 'HLT_Mu40_eta2p1_PFJet200_PFJet50_v6',
        'HLT_Mu40_eta2p1_PFJet200_PFJet50_v7',
        'HLT_PFHT900_v1', 'HLT_PFHT900_v2', 'HLT_PFHT900_v3', 'HLT_PFHT900_v4', 'HLT_PFHT900_v5', 'HLT_PFHT900_v6',
        'HLT_PFHT600_v3', 'HLT_PFHT600_v4', 'HLT_PFHT600_v5', 'HLT_PFHT600_v6', 'HLT_PFHT600_v7', 'HLT_PFHT600_v8',
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
    jet_maxeta               = cms.double(2.4),
    min_jet                  = cms.int32(1),
    max_jet                  = cms.int32(4000),
    leading_jet_pt           = cms.double(30.0),

    # muon cuts
    muon_cuts                = cms.bool(True),
    muon_selector            = cms.bool(False),
    muon_selector_medium     = cms.bool(False),
    muon_reliso              = cms.double(0.2),
    muon_useMiniIso          = cms.bool(True),
    muon_miniIso             = cms.double(0.1),
    loose_muon_miniIso       = cms.double(0.4),
    muon_minpt               = cms.double(30.0),
    muon_maxeta              = cms.double(2.4),
    min_muon                 = cms.int32(0),
    loose_muon_selector      = cms.bool(False),
    loose_muon_selector_tight = cms.bool(False),
    loose_muon_reliso        = cms.double(0.4),
    loose_muon_minpt         = cms.double(10.0),
    loose_muon_maxeta        = cms.double(2.4),
    # specify IP cuts
    muon_dxy                 = cms.double(0.2),
    muon_dz                  = cms.double(0.5),
    loose_muon_dxy           = cms.double(999999.),
    loose_muon_dz            = cms.double(999999.),
 
    # electron cuts
    electron_cuts            = cms.bool(True),
    electron_minpt           = cms.double(30.0),
    electron_maxeta          = cms.double(2.5),
    electron_useMiniIso      = cms.bool(True),
    electron_miniIso         = cms.double(0.1),
    electron_CutsPlusMVA     = cms.bool(False),
    min_electron             = cms.int32(0),
    loose_electron_minpt     = cms.double(10.0),
    loose_electron_maxeta    = cms.double(2.5),
    loose_electron_miniIso   = cms.double(0.4),
    UseElMVA                 = cms.bool(True),
    UseElMVA_tight           = cms.bool(True),
    tight_electron_mva_cuts  = cms.vdouble(0.674,0.744,0.170),#0.967083,0.929117,0.726311), # ~80% el efficiency WP
    loose_electron_mva_cuts  = cms.vdouble(-0.041,0.383,-0.515),#0.913286,0.805013,0.358969), # ~90% el efficiency WP

    ElMVAweightFiles = cms.vstring(
        relBase+'/src/LJMet/Com/weights/EIDmva_EB1_10_oldNonTrigSpring15_ConvVarCwoBoolean_TMVA412_FullStatLowPt_PairNegWeightsGlobal_BDT.weights.xml',
        relBase+'/src/LJMet/Com/weights/EIDmva_EB2_10_oldNonTrigSpring15_ConvVarCwoBoolean_TMVA412_FullStatLowPt_PairNegWeightsGlobal_BDT.weights.xml',
        relBase+'/src/LJMet/Com/weights/EIDmva_EE_10_oldNonTrigSpring15_ConvVarCwoBoolean_TMVA412_FullStatLowPt_PairNegWeightsGlobal_BDT.weights.xml',
        ),

    ElMVAweightFiles_alt = cms.vstring(
        relBase+'/src/LJMet/Com/weights/electronID_mva_Spring16_GeneralPurpose_V1_EB1_10.weights.xml',
        relBase+'/src/LJMet/Com/weights/electronID_mva_Spring16_GeneralPurpose_V1_EB2_10.weights.xml',
        relBase+'/src/LJMet/Com/weights/electronID_mva_Spring16_GeneralPurpose_V1_EE_10.weights.xml',
        ),

    # more lepton cuts
    min_lepton               = cms.int32(1),    # checks (N tight mu + N tight el) >= cut
    max_lepton               = cms.int32(1000),    # checks (N tight mu + N tight el) <= cut
    min_loose_lepton         = cms.int32(0),
    max_loose_lepton         = cms.int32(1000),
    second_lepton_veto       = cms.bool(False),  #checks (N tight lep > 0) AND (N loose lep > 0), vetoes if there are loose leptons.
    tau_veto		     = cms.bool(False),
    
    # MET cuts
    met_cuts                 = cms.bool(True),
    min_met                  = cms.double(20.0),
    max_met                  = cms.double(99999999999.0),
    
    # Btagging cuts
    btagOP                   = cms.string('CSVM'),
    btag_min_discr           = cms.double(0.8484),
    btag_cuts                = cms.bool(False),
    btag_1                   = cms.bool(False),
    btag_2                   = cms.bool(False),
    btag_3                   = cms.bool(False),
    
    # Define the branch names of object collections in the input miniAOD file
    trigger_collection       = cms.InputTag('TriggerResults::HLT'),
    pv_collection            = cms.InputTag('offlineSlimmedPrimaryVertices'),
    jet_collection           = cms.InputTag('slimmedJets'),
    muon_collection          = cms.InputTag('slimmedMuons'),
    electron_collection      = cms.InputTag('slimmedElectrons'),
    tau_collection	     = cms.InputTag('slimmedTaus'),
    met_collection           = cms.InputTag('slimmedMETs'),
    
    # Jet corrections are read from txt files which need updating!
    JEC_txtfile = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016V3_MC_Uncertainty_AK4PFchs.txt'),
    JERSF_txtfile = cms.string(relBase+'/src/LJMet/Com/data/Spring16V10/Spring16_25nsV10_MC_SF_AK4PFchs.txt'),
    JER_txtfile = cms.string(relBase+'/src/LJMet/Com/data/Spring16V10/Spring16_25nsV10_MC_PtResolution_AK4PFchs.txt'),
    JERAK8_txtfile = cms.string(relBase+'/src/LJMet/Com/data/Spring16V10/Spring16_25nsV10_MC_PtResolution_AK8PFchs.txt'),

    BTagUncertUp             = cms.bool(False), # no longer needed
    BTagUncertDown           = cms.bool(False), # no longer needed
    JECup                    = cms.bool(False),
    JECdown                  = cms.bool(False),
    JERup                    = cms.bool(False),
    JERdown                  = cms.bool(False),
    doNewJEC                 = cms.bool(True),
    doLepJetCleaning         = cms.bool(True),
    CleanLooseLeptons        = cms.bool(False),
    LepJetDR                 = cms.double(0.4),
    
    MCL1JetPar               = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016V3_MC_L1FastJet_AK4PFchs.txt'),
    MCL2JetPar               = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016V3_MC_L2Relative_AK4PFchs.txt'),
    MCL3JetPar               = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016V3_MC_L3Absolute_AK4PFchs.txt'),

    MCL1JetParAK8            = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016V3_MC_L1FastJet_AK8PFchs.txt'),
    MCL2JetParAK8            = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016V3_MC_L2Relative_AK8PFchs.txt'),
    MCL3JetParAK8            = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016V3_MC_L3Absolute_AK8PFchs.txt'),

    DataL1JetPar             = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016BCDV3_DATA_L1FastJet_AK4PFchs.txt'),
    DataL2JetPar             = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016BCDV3_DATA_L2Relative_AK4PFchs.txt'),
    DataL3JetPar             = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016BCDV3_DATA_L3Absolute_AK4PFchs.txt'),
    DataResJetPar            = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016BCDV3_DATA_L2L3Residual_AK4PFchs.txt'),

    DataL1JetParAK8          = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016BCDV3_DATA_L1FastJet_AK8PFchs.txt'),
    DataL2JetParAK8          = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016BCDV3_DATA_L2Relative_AK8PFchs.txt'),
    DataL3JetParAK8          = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016BCDV3_DATA_L3Absolute_AK8PFchs.txt'),
    DataResJetParAK8         = cms.string(relBase+'/src/LJMet/Com/data/Summer16RRV3/Summer16_23Sep2016BCDV3_DATA_L2L3Residual_AK8PFchs.txt')

    )


#######################################################
#
# Input files
#

process.inputs = cms.PSet (
    nEvents    = cms.int32(-1),
    skipEvents = cms.int32(0),
    lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange()),
    fileNames  = cms.vstring(CONDOR_FILELIST)
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
    outputName = cms.string('CONDOR_OUTFILE'),
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

# jets
process.load('PhysicsTools.SelectorUtils.pfJetIDSelector_cfi') 
process.pfJetIDSelector.version = cms.string('FIRSTDATA')
process.pfJetIDSelector.quality = cms.string('LOOSE')

# Tight muon
process.load('LJMet.Com.pfMuonSelector_cfi') #not used

# Loose muon
process.LoosepfMuonSelector = process.pfMuonSelector.clone() #not used

# Tight electron for 25ns
process.load('LJMet.Com.TopElectronSelector_cfi')
process.TopElectronSelector.version = cms.string('NONE') #not used
                   	       
#Loose electron for 25ns
process.LooseTopElectronSelector = process.TopElectronSelector.clone()
process.LooseTopElectronSelector.version = cms.string('NONE') #not used
