# Run the binned maximum likelihod fit for $B_s\to\tau\tau$ shape analysis

Reference Combine setup : https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/v10.6.1/part2/settinguptheanalysis/#binned-shape-analyses 

## One-time setup
### Install Combine and Combine Harvester
```
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv
git -c advice.detachedHead=false clone --depth 1 --branch v10.2.1 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
scramv1 b clean; scramv1 b

##CombineHarvester
cd ../../
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
cd CombineHarvester
git checkout v3.0.0
scram b
```

### Get this repo and install $B_s\to\tau\tau$ commands
```bash
cd $CMSSW_BASE/src
git clone --recursive git@github.com:bstautau-ttbar/combine-analysis.git
cd combine-analysis
```
include the $B_s\to\tau\tau$ script to build the datacards into the CombineHarvester executables
```
cp BsTauTau.cpp $CMSSW_BASE/src/CombineHarvester/CombineTools/bin/.
```
Add `<bin file="BsTauTau.cpp" name="BsTauTau"></bin>` to `$CMSSW_BASE/src/CombineHarvester/CombineTools/bin/BuildFile.xml` file

```
cd $CMSSW_BASE/src
scram b -j 8
cmsenv
```

## Prepare histograms and run the fit
```
python3 prepare_histograms.py 12Aug2025_11h48m43s #folder name output of the plotter script
```
This should copy the datacard into `auxiliaries/shapes/bstautau.root`, if not, copyt it there.
```
BsTauTau # should dave .txt datacards into datacards fodler
combine_and_fit.sh
```
