#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"

using namespace std;

//FIXME
// - year info in channel name
// - create /datacard directory and save datacards there
// - better naming of bins

int main() {
  //! [part1]
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/shapes/";

  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  // Here we will just define two categories for an 13TeV analysis. Each entry in
  // the vector below specifies a bin name and corresponding bin_id.
  /*
  ch::Categories cats = {
      
      {4,  "mu_tauhtaue"},
      {5,  "mu_tauhtaumu"},
      {6,  "mu_tauhtauh"},
      {7,  "ee_tauhtaue"},
      {8,  "ee_tauhtaumu"},
      {9,  "ee_tauhtauh"},
      {10, "emu_tauhtaue"},
      {11, "emu_tauhtaumu"},
      {12, "emu_tauhtauh"},
      {13, "mumu_tauhtaue"},
      {14, "mumu_tauhtaumu"},
      {15, "mumu_tauhtauh"}
    };
    */

  ch::Categories cats = { 
      {1,  "emu_tauhtauh_sr"},
      {2,  "emu_tauhtaumu_sr"},
      {3,  "emu_tauhtaue_sr"},
      {4,  "emu_tauhtauh_cr"},
      {5,  "emu_tauhtaumu_cr"},
      {6,  "emu_tauhtaue_cr"},
      //{6, "mumu_tauhtaue_sr"},
      //{7, "mumu_tauhtaue_cr"},
      //{8, "mumu_tauhtaumu_sr"},
      //{9, "mumu_tauhtaumu_cr"},
      //{10, "mumu_tauhtauh_sr"},
      //{11, "mumu_tauhtauh_cr"},
      //{12, "mu_tauhtaue_sr"},
      //{13, "mu_tauhtaue_cr"},
      //{14, "mu_tauhtaumu_sr"},
      //{15, "mu_tauhtaumu_cr"},
      //{16, "mu_tauhtauh_sr"},
      //{17, "mu_tauhtauh_cr"}
    };

  vector<string> masses = {""};
  // observed number of events | AddObservations(masses, analyses, eras, channels, categories)
  cb.AddObservations({"*"}, {"bs"}, {"13TeV"}, {"tautau"}, cats);

  // signal and background processes | AddProcesses(masses, analyses, eras, channels, processes, categories, isSignal)
  vector<string> bkg_procs = {"tt_fullylep","tt_semilep","tt_had"};//{"tt_fullylep","tt_semilep","tt_had","ww","wz","zz","st_s","st_antit","st_tw","st_antitw","w","wext","dy"};
  vector<string> sig_procs = {"bstautau"};
  cb.AddProcesses({"*"}, {"bs"}, {"13TeV"}, {"tautau"}, bkg_procs, cats, false);
  cb.AddProcesses(masses, {"bs"}, {"13TeV"}, {"tautau"}, sig_procs, cats, true);


  //Some of the code for this is in a nested namespace, so
  // we'll make some using declarations first to simplify things a bit.
  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;

  // ------- SYSTEMATICS ------- //
  // N.B. placeholder values
  cb.cp().signals().AddSyst(cb, "signal_norm", "lnN", SystMap<>::init(1.01));
  cb.cp().process(ch::JoinStr({sig_procs, bkg_procs})).AddSyst(cb, "lumi_2018", "lnN", SystMap<>::init(1.026));

  // 2% uncertainty per muon
  //cb.cp().bin({"mu_tauhtaue","mu_tauhtaumu","mu_tauhtauh"}).process(ch::JoinStr({sig_procs, {"tt_fullylep","tt_semilep","tt_had","ww","wz","zz","st_s","st_antit","st_tw","st_antitw","w","wext","dy"}})).AddSyst(cb, "mu_eff", "lnN", SystMap<>::init(1.010));
  cb.cp().bin({"emu_tauhtaue_sr","emu_tauhtaumu_sr","emu_tauhtauh_sr", "emu_tauhtaue_cr","emu_tauhtaumu_cr","emu_tauhtauh_cr"}).process(ch::JoinStr({sig_procs, bkg_procs})).AddSyst(cb, "emu_eff", "lnN", SystMap<>::init(1.010));
  //cb.cp().bin({"mumu_tauhtaue","mumu_tauhtaumu","mumu_tauhtauh"}).process(ch::JoinStr({sig_procs, bkg_procs})).AddSyst(cb, "mumu_eff", "lnN", SystMap<>::init(1.020));


  // rateParam
  cb.cp().bin({"emu_tauhtaue_sr","emu_tauhtaumu_sr","emu_tauhtauh_sr", "emu_tauhtaue_cr","emu_tauhtaumu_cr","emu_tauhtauh_cr"}).process(bkg_procs).AddSyst(cb, "bkg_norm", "rateParam", SystMap<>::init(1.0)); // example of rateParam
  //cb.cp().bin({"stub4_bx1234"}).process({"Fake"}).AddSyst(cb, "CMS_EXO25010_normFake_stub4_bx1234", "rateParam", SystMap<>::init(1.0)); // example of rateParam
  //cb.cp().bin({"stub4_bx1234"}).process({"Fake"}).AddSyst(cb, "CMS_EXO25010_shape_stub4_bx1234", "shape", SystMap<>::init(1.00)); // example of shape uncertainty


  //! [part7]
  cb.cp().backgrounds().ExtractShapes(
      aux_shapes + "bstautau_2018.root",
      "$BIN/$PROCESS",
      "$BIN/$PROCESS_$SYSTEMATIC");
  cb.cp().signals().ExtractShapes(
      aux_shapes + "bstautau_2018.root", 
      "$BIN/$PROCESS$MASS",
      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
  //! [part7]

  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the bs analyses
  ch::SetStandardBinNames(cb);
  //! [part8]

  //! [part9]
  // First we generate a set of bin names:
  set<string> bins = cb.bin_set();
  // This method will produce a set of unique bin names by considering all
  // Observation, Process and Systematic entries in the CombineHarvester
  // instance.

  // We create the output root file that will contain all the shapes.
  TFile output("bs_tautau.input.root", "RECREATE");

  // Finally we iterate through each bin,mass combination and write a
  // datacard.
  for (auto b : bins) {
    for (auto m : masses) {
      cout << ">> Writing datacard for bin: " << b << " and mass: " << m
           << "\n";
      // We need to filter on both the mass and the mass hypothesis,
      // where we must remember to include the "*" mass entry to get
      // all the data and backgrounds.
      cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(
          b + "_" + m + ".txt", output);
    }
  }
  //! [part9]

}
