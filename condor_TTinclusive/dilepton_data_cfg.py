import FWCore.ParameterSet.Config as cms
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes

process = cms.Process("LJMetCom")

#Common calculator options
process.load('LJMet.Com.commonCalc_cfi')

#Dilepton calculator options
process.load('LJMet.Com.DileptonCalc_cfi')
process.subProcesses = cms.PSet()

############################################################
#
# FWLite application options
#
process.ljmet = cms.PSet(
    isMc = cms.bool(False),
    runs = cms.vint32([])
)

process.ljmet.excluded_calculators = cms.vstring(
	'LjetsTopoCalcMinPz',
        'LjetsTopoCalcNew'
	'StopCalc',
	'PdfCalc',
	'ChargedHiggsCalc',
	'TprimeCalc',
	'TpTpCalc',
	'LjetsTopoCalc',
	'WprimeCalc',
        'WprimeBoostedCalc'
	'singleLepCalc',
        'BTagSFCalc',
        'CATopoCalc',
	) 


process.DileptonCalc.isMc     = process.ljmet.isMc
process.DileptonCalc.dataType = cms.string('All')

# Jet substructure calculator options -- see src/JetSubCalc.cc
process.load('LJMet.Com.JetSubCalc_cfi')
process.JetSubCalc.useHTT = cms.bool(False)
process.JetSubCalc.killHF = cms.bool(False)
process.JetSubCalc.doNewJEC = cms.bool(True)
process.JetSubCalc.useL2L3Mass = cms.bool(True)
process.JetSubCalc.isMc = process.ljmet.isMc
process.JetSubCalc.JECup = cms.bool(JECUNCERTUP)
process.JetSubCalc.JECdown = cms.bool(JECUNCERTDOWN)
process.JetSubCalc.MCL2JetParAK8 = cms.string('../data/Spring16_25nsV6_MC_L2Relative_AK8PFchs.txt')
process.JetSubCalc.MCL3JetParAK8 = cms.string('../data/Spring16_25nsV6_MC_L3Absolute_AK8PFchs.txt')
process.JetSubCalc.DataL2JetParAK8 = cms.string('../data/Spring16_25nsV6_DATA_L2Relative_AK8PFchs.txt')
process.JetSubCalc.DataL3JetParAK8 = cms.string('../data/Spring16_25nsV6_DATA_L3Absolute_AK8PFchs.txt')
process.JetSubCalc.DataL2L3JetParAK8 = cms.string('../data/Spring16_25nsV6_DATA_L2L3Residual_AK8PFchs.txt')
process.JetSubCalc.UncertaintyAK8 = cms.string('../data/Spring16_25nsV6_DATA_Uncertainty_AK8PFchs.txt')


############################################################
#
# Event selector options
#
process.event_selector = cms.PSet(

    selection = cms.string('DileptonSelector'),
    isMc              = cms.bool(False),
    keepFullMChistory = cms.bool(False),
    debug             = cms.bool(False),
    # cuts
    #HLT
    trigger_cut              = cms.bool(True),
    dump_trigger             = cms.bool(True),

    #Can use same trigger paths for data and MC since MC is always one of the data versions
    trigger_path_ee          = cms.vstring(
    'HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v1',
    'HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v2',
    'HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v3',
    'HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v4',
    'HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v5',
    'HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v6',
    'HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v7',
    'HLT_DoubleEle37_Ele27_CaloIdL_GsfTrkIdVL_v1',
    'HLT_DoubleEle37_Ele27_CaloIdL_GsfTrkIdVL_v2',
    'HLT_DoubleEle37_Ele27_CaloIdL_GsfTrkIdVL_v3',
    'HLT_DoubleEle37_Ele27_CaloIdL_GsfTrkIdVL_v4',
    'HLT_DoubleEle37_Ele27_CaloIdL_GsfTrkIdVL_v5',
    'HLT_DoubleEle37_Ele27_CaloIdL_GsfTrkIdVL_v6',
    'HLT_DoubleEle37_Ele27_CaloIdL_GsfTrkIdVL_v7',
    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v1',
    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v2',
    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v3',
    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v4',
    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v5',
    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v6',
    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v7'),
    
    trigger_path_em          = cms.vstring(
    'HLT_Mu37_Ele27_CaloIdL_GsfTrkIdVL_v1',
    'HLT_Mu37_Ele27_CaloIdL_GsfTrkIdVL_v2',
    'HLT_Mu37_Ele27_CaloIdL_GsfTrkIdVL_v3',
    'HLT_Mu37_Ele27_CaloIdL_GsfTrkIdVL_v4',
    'HLT_Mu37_Ele27_CaloIdL_GsfTrkIdVL_v5',
    'HLT_Mu27_Ele37_CaloIdL_GsfTrkIdVL_v1',
    'HLT_Mu27_Ele37_CaloIdL_GsfTrkIdVL_v2',
    'HLT_Mu27_Ele37_CaloIdL_GsfTrkIdVL_v3',
    'HLT_Mu27_Ele37_CaloIdL_GsfTrkIdVL_v4',
    'HLT_Mu27_Ele37_CaloIdL_GsfTrkIdVL_v5',
    'HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v1',
    'HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v2',
    'HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v3',
    'HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v4',
    'HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v5',
    'HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v6',
    'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v1',
    'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v2',
    'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v3',
    'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v4',
    'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v5',
    'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v6',
    'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v1',
    'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v2',
    'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v3',
    'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v4'),

    trigger_path_mm          = cms.vstring(
    'HLT_Mu30_TkMu11_v1',
    'HLT_Mu30_TkMu11_v2',
    'HLT_Mu30_TkMu11_v3',
    'HLT_Mu40_TkMu11_v1',
    'HLT_Mu40_TkMu11_v2',
    'HLT_Mu40_TkMu11_v3',),

    pv_cut                   = cms.bool(True),
    hbhe_cut                 = cms.bool(True),
    hbhe_cut_value           = cms.string("Run2Loose"),
    hbheiso_cut              = cms.bool(True),
    eesc_cut                 = cms.bool(True),
    ecalTP_cut               = cms.bool(True),
    goodVtx_cut              = cms.bool(True),
    badMuon_cut              = cms.bool(True),
    badChargedHadron_cut     = cms.bool(True),    			     
    flag_tag                 = cms.InputTag('FLAGTAG'),
    cscHalo_cut              = cms.bool(True),
    jet_cuts                 = cms.bool(False),
    jet_minpt                = cms.double(30.0),
    jet_maxeta               = cms.double(2.4),
    min_jet                  = cms.int32(4),
    max_jet                  = cms.int32(4000),

    muon_cuts                = cms.bool(True),
    min_muon                 = cms.int32(0),
    muon_minpt               = cms.double(10.0),
    muon_maxeta              = cms.double(2.4),
    max_muon                 = cms.int32(10),

    electron_cuts            = cms.bool(True),
    min_electron             = cms.int32(0),
    electron_minpt           = cms.double(10.0),
    electron_maxeta          = cms.double(2.4),
    max_electron             = cms.int32(10),
    UseElMVA                 = cms.bool(True),

    min_lepton               = cms.int32(2),

    met_cuts                 = cms.bool(False),
    min_met                  = cms.double(0.0),
    btag_cuts                = cms.bool(False),
     btagOP                  = cms.string("CSVM"),
    btag_1                   = cms.bool(True),
    btag_2                   = cms.bool(True),
    btag_3                   = cms.bool(False),

    trigger_collection       = cms.InputTag('TriggerResults::HLT'),
    pv_collection            = cms.InputTag('offlineSlimmedPrimaryVertices'),
    jet_collection           = cms.InputTag('slimmedJets'),
    muon_collection          = cms.InputTag('slimmedMuons'),
    electron_collection      = cms.InputTag('slimmedElectrons'),
    met_collection           = cms.InputTag('slimmedMETs'),


    #This is for uncertainty calculations   
    JECup      	             = cms.bool(JECUNCERTUP),
    JECdown                  = cms.bool(JECUNCERTDOWN),
    JERup                    = cms.bool(JERUNCERTUP),
    JERdown                  = cms.bool(JERUNCERTDOWN),

    JEC_txtfile              = cms.string('../data/Spring16_25nsV6_MC_Uncertainty_AK4PFchs.txt'),
    JERSF_txtfile            = cms.string('../data/Spring16_25nsV6_MC_SF_AK4PFchs.txt'),	
    JER_txtfile              = cms.string('../data/Spring16_25nsV6_MC_PtResolution_AK4PFchs.txt'),
    JERAK8_txtfile           = cms.string('../data/Spring16_25nsV6_MC_PtResolution_AK8PFchs.txt'),


    #new jet energy corrections
    doNewJEC                 = cms.bool(True),
    doLepJetCleaning         = cms.bool(True),


    MCL1JetPar               = cms.string("../data/Spring16_25nsV6_MC_L1FastJet_AK4PFchs.txt"),
    MCL2JetPar               = cms.string("../data/Spring16_25nsV6_MC_L2Relative_AK4PFchs.txt"),
    MCL3JetPar               = cms.string("../data/Spring16_25nsV6_MC_L3Absolute_AK4PFchs.txt"),

    MCL1JetParAK8            = cms.string("../data/Spring16_25nsV6_MC_L1FastJet_AK8PFchs.txt"),
    MCL2JetParAK8            = cms.string("../data/Spring16_25nsV6_MC_L2Relative_AK8PFchs.txt"),
    MCL3JetParAK8            = cms.string("../data/Spring16_25nsV6_MC_L3Absolute_AK8PFchs.txt"),


    DataL1JetPar               = cms.string("../data/Spring16_25nsV6_DATA_L1FastJet_AK4PFchs.txt"),
    DataL2JetPar               = cms.string("../data/Spring16_25nsV6_DATA_L2Relative_AK4PFchs.txt"),
    DataL3JetPar               = cms.string("../data/Spring16_25nsV6_DATA_L3Absolute_AK4PFchs.txt"),
    DataResJetPar               = cms.string("../data/Spring16_25nsV6_DATA_L3Absolute_AK4PFchs.txt"),

    DataL1JetParAK8            = cms.string("../data/Spring16_25nsV6_DATA_L1FastJet_AK8PFchs.txt"),
    DataL2JetParAK8            = cms.string("../data/Spring16_25nsV6_DATA_L2Relative_AK8PFchs.txt"),
    DataL3JetParAK8            = cms.string("../data/Spring16_25nsV6_DATA_L3Absolute_AK8PFchs.txt"),
    DataResJetParAK8               = cms.string("../data/Spring16_25nsV6_DATA_L3Absolute_AK8PFchs.txt"),


    #triggerstudy info
    doTriggerStudy           = cms.bool(True),
    TriggerBits              = cms.InputTag("TriggerResults","","HLT"),
    TriggerObjects           = cms.InputTag("selectedPatTrigger"),


)

#######################################################
#
# Input files
#


process.inputs = cms.PSet (
   nEvents    = cms.int32(EVENTSTOPROCESS),
   skipEvents = cms.int32(0),	
   lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange()),
       fileNames  = cms.vstring(
	INFILES
     ) 
)



# JSON
if (not process.ljmet.isMc==cms.bool(True)):
    JsonFile = JSONFILE
    myList   = LumiList.LumiList(filename=JsonFile).getCMSSWString().split(',')
    process.inputs.lumisToProcess.extend(myList)
       
        
        
#######################################################
#
# Output
#

import os
try: scratchDir=os.environ['_CONDOR_SCRATCH_DIR']
except: scratchDir='.'
if not os.path.isdir(scratchDir): os.system("mkdir -p "+scratchDir)
process.outputs = cms.PSet (
    #outputName = cms.string(scratchDir+'/PREFIX_JOBID'),
    outputName = cms.string('PREFIX_JOBID'),
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
