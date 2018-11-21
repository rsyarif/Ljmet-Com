import FWCore.ParameterSet.Config as cms
process = cms.Process("jectxt")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
# define your favorite global tag
process.GlobalTag.globaltag = '102X_dataRun2_Sep2018Rereco_v1'
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))
process.source = cms.Source("EmptySource")
process.readAK4PF    = cms.EDAnalyzer('JetCorrectorDBReader',  
      # below is the communication to the database 
      payloadName    = cms.untracked.string('AK4PFchs'),
      # this is used ONLY for the name of the printed txt files. You can use any name that you like, 
      # but it is recommended to use the GT name that you retrieved the files from.
      globalTag      = cms.untracked.string('102X_dataRun2_Sep2018Rereco_v1'),  
      printScreen    = cms.untracked.bool(False),
      createTextFile = cms.untracked.bool(True)
)
process.readAK8PF = process.readAK4PF.clone(payloadName = 'AK8PFPuppi')
process.p = cms.Path(process.readAK4PF * process.readAK8PF)
