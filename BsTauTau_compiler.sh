#!/bin/bash
PWD=$(pwd)

cp BsTauTau.cpp $CMSSW_BASE/src/CombineHarvester/CombineTools/bin/
cd $CMSSW_BASE/src/
scram b -j 8
cd $PWD