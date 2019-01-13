import FWCore.ParameterSet.Config as cms
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes
import os

#Arguments from condor submit script which are used more than once
relBase    = os.environ['CMSSW_BASE']
condorJSON = str('none')

# Define the base process
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
    isMc = cms.bool(True),
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
        'WprimeBoostedCalc',
	'singleLepCalc',
        'BTagSFCalc',
        'CATopoCalc',
	)

# Jet substructure calculator options
process.load('LJMet.Com.JetSubCalc_cfi')
process.JetSubCalc.killHF = cms.bool(False)
process.JetSubCalc.isMc = cms.bool(True)

process.DileptonCalc.isMc     = process.ljmet.isMc
process.DileptonCalc.dataType = cms.string('ElMu')
process.DileptonCalc.UseElMVA = cms.bool(True)


# BestCalc options
process.load('LJMet.Com.BestCalc_cfi')
process.BestCalc.dnnFile = cms.string(relBase+'/src/LJMet/Com/data/BEST_mlp.json')

############################################################
#
# Event selector options
#
process.event_selector = cms.PSet(

    selection = cms.string('DileptonSelector'),
    isMc              = cms.bool(True),
    keepFullMChistory = cms.bool(True),
    debug             = cms.bool(True),
    # cuts
    #HLT
    trigger_cut              = cms.bool(True),
    dump_trigger             = cms.bool(True),

    #Can use same trigger paths for data and MC since MC is always one of the data versions
    trigger_path_ee          = cms.vstring(
    'HLT_DoubleEle33_CaloIdL_MW_v',
    'HLT_DoubleEle27_CaloIdL_MW_v',
    'HLT_DoubleEle25_CaloIdL_MW_v',
    'HLT_Ele27_Ele37_CaloIdL_MW_v',

    'HLT_DoubleEle24_eta2p1_WPTight_Gsf_v',
    'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v',
    'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v',
    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v',
    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v',

    ),
    
    trigger_path_em          = cms.vstring(
    'HLT_Mu37_Ele27_CaloIdL_MW_v',
    'HLT_Mu27_Ele37_CaloIdL_MW_v',

    'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ_v',
    'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v',
    'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_v',
    'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v',
    'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v',
    'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v',
    'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v',
    'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v',
    ),

    trigger_path_mm          = cms.vstring(
    'HLT_Mu37_TkMu27_v',
    'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8',
    ),

    pv_cut                   = cms.bool(True),
    hbhe_cut                 = cms.bool(True),
    hbhe_cut_value           = cms.string("Run2Loose"),
    hbheiso_cut              = cms.bool(True),
    eesc_cut                 = cms.bool(True),
    ecalTP_cut               = cms.bool(True),
    goodVtx_cut              = cms.bool(True),
    badMuon_cut              = cms.bool(True),
    badChargedHadron_cut     = cms.bool(True),
    flag_tag                 = cms.InputTag('TriggerResults::PAT'),
    cscHalo_cut              = cms.bool(True),

    metfilters     = cms.bool(True),

    jet_cuts                 = cms.bool(False),
    jet_minpt                = cms.double(30.0),
    jet_maxeta               = cms.double(5.0),
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
    tight_electron_mva_cuts  = cms.vdouble(0.96165,8.75794,3.13902,0.93193,8.84606,3.59851,0.88993,10.12423,4.35279), # Fall17 noiso WP90 c, tau, A for EB1, EB2, and then EE
    loose_electron_mva_cuts  = cms.vdouble(-0.86,-0.81,-0.72), # Fall17 noiso WP HZZ exact cuts
    #tight_electron_mva_cuts  = cms.vdouble(0.97177,8.91285,1.97124,0.945875,8.83104,2.40850,0.89791,9.81408,4.17158), # Fall17 iso WP90 c, tau, A for EB1, EB2, and then EE
    #loose_electron_mva_cuts  = cms.vdouble(-0.83,-0.77,-0.69), # Fall17 iso WP HZZ exact cuts

    ElMVAweightFiles = cms.vstring(
        relBase+'/src/LJMet/Com/weights/EIDmva_EB1_10_2017_puinfo_BDT.weights.xml',
        relBase+'/src/LJMet/Com/weights/EIDmva_EB2_10_2017_puinfo_BDT.weights.xml',
        relBase+'/src/LJMet/Com/weights/EIDmva_EE_10_2017_puinfo_BDT.weights.xml',
        ),

    ElMVAweightFiles_iso = cms.vstring(
        relBase+'/src/LJMet/Com/weights/EIDmva_EB1_10_2017_puinfo_iso_BDT.weights.xml',
        relBase+'/src/LJMet/Com/weights/EIDmva_EB2_10_2017_puinfo_iso_BDT.weights.xml',
        relBase+'/src/LJMet/Com/weights/EIDmva_EE_10_2017_puinfo_iso_BDT.weights.xml',
        ),

    min_lepton               = cms.int32(2),

    met_cuts                 = cms.bool(False),
    min_met                  = cms.double(0.0),

    # Btagging cuts
    btagOP                   = cms.string('MEDIUM'),
    bdisc_min                = cms.double(0.4941),
    DeepCSVfile              = cms.string(relBase+'/src/LJMet/Com/data/DeepCSV_94XSF_V3_B_F.csv'),
    DeepCSVSubjetfile        = cms.string(relBase+'/src/LJMet/Com/data/subjet_DeepCSV_94XSF_V3_B_F.csv'),
    btag_cuts                = cms.bool(False),
    btag_1                   = cms.bool(True),
    btag_2                   = cms.bool(True),
    btag_3                   = cms.bool(False),

    trigger_collection       = cms.InputTag('TriggerResults::HLT'),
    pv_collection            = cms.InputTag('offlineSlimmedPrimaryVertices'),
    jet_collection           = cms.InputTag('slimmedJets'),
    slimmedJetsAK8           = cms.InputTag('slimmedJetsAK8'),
    muon_collection          = cms.InputTag('slimmedMuons'),
    electron_collection      = cms.InputTag('slimmedElectrons'),
    met_collection           = cms.InputTag('slimmedMETs'),

    # Jet corrections are read from txt files which need updating!
    JEC_txtfile = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017_V6_MC_Uncertainty_AK4PFchs.txt'),
    JERSF_txtfile = cms.string(relBase+'/src/LJMet/Com/data/Spring16V10/Spring16_25nsV10_MC_SF_AK4PFchs.txt'),
    JER_txtfile = cms.string(relBase+'/src/LJMet/Com/data/Spring16V10/Spring16_25nsV10_MC_PtResolution_AK4PFchs.txt'),
    JERAK8_txtfile = cms.string(relBase+'/src/LJMet/Com/data/Spring16V10/Spring16_25nsV10_MC_PtResolution_AK8PFchs.txt'),

    JECup		     = cms.bool(False),
    JECdown                  = cms.bool(False),
    JERup                    = cms.bool(False),
    JERdown                  = cms.bool(False),

    #new jet energy corrections
    doNewJEC                 = cms.bool(True),
    doLepJetCleaning         = cms.bool(True),

    MCL1JetPar               = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017_V6_MC_L1FastJet_AK4PFchs.txt'),
    MCL2JetPar               = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017_V6_MC_L2Relative_AK4PFchs.txt'),
    MCL3JetPar               = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017_V6_MC_L3Absolute_AK4PFchs.txt'),

    MCL1JetParAK8            = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017_V6_MC_L1FastJet_AK8PFPuppi.txt'),
    MCL2JetParAK8            = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017_V6_MC_L2Relative_AK8PFPuppi.txt'),
    MCL3JetParAK8            = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017_V6_MC_L3Absolute_AK8PFPuppi.txt'),

    DataL1JetPar             = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017B_V6_DATA_L1FastJet_AK4PFchs.txt'),
    DataL2JetPar             = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017B_V6_DATA_L2Relative_AK4PFchs.txt'),
    DataL3JetPar             = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017B_V6_DATA_L3Absolute_AK4PFchs.txt'),
    DataResJetPar            = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017B_V6_DATA_L2L3Residual_AK4PFchs.txt'),

    DataL1JetParAK8          = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017B_V6_DATA_L1FastJet_AK8PFPuppi.txt'),
    DataL2JetParAK8          = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017B_V6_DATA_L2Relative_AK8PFPuppi.txt'),
    DataL3JetParAK8          = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017B_V6_DATA_L3Absolute_AK8PFPuppi.txt'),
    DataResJetParAK8         = cms.string(relBase+'/src/LJMet/Com/data/Fall17V6/Fall17_17Nov2017B_V6_DATA_L2L3Residual_AK8PFPuppi.txt'),


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
   nEvents    = cms.int32(500),
   skipEvents = cms.int32(0),
   lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange()),
       fileNames  = cms.vstring(
	                 'root://cmsxrootd.fnal.gov//store/mc/RunIIFall17MiniAODv2/TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/00000/8EA8FE89-254F-E811-835E-0090FAA58BF4.root',

     )
)



# JSON
if (not process.ljmet.isMc==cms.bool(True)):
    JsonFile = ''
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
    #outputName = cms.string(scratchDir+'/TprimeTprime_M-1500_13'),
    outputName = cms.string('TprimeTprime_M-1100_testMC'),
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