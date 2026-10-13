#!/usr/bin/env python3
"""
Prepare Histograms for CombineHarvester C++ Code
==============================================

This script takes the histograms.root file from the plotter and creates
a ROOT file with the structure expected by the existing BsTauTau.cpp code:

Structure: $BIN/$PROCESS
- Each category gets its own directory
- data is renamed to data_obs
- bstautau is renamed to bstautau (signal)
- All other samples keep their original names

Categories from BsTauTau.cpp:

"""

import ROOT
import os, sys
import argparse
import utils.samples as samples

def get_arguments():
    
    _defaults = {
       "h_file"      : "histograms.root",
       "year"        : "2018",
       "output_dir"  : "$CMSSW_BASE/src/auxiliaries/shapes/"
    }
    parser = argparse.ArgumentParser(
        description="Prepare histograms for CombineHarvester C++ code.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--h_path",
                        type=str, required=True,
                        help="Path to the folder containing a .root file with the binned shapes."
                        )
    parser.add_argument("--h_file",
                        type=str,
                        help="Name of the .root file containing the binned shapes."
                        )
    parser.add_argument("-y", "--year",
                        type=str,
                        help="Year of the analysis (e.g., 2016, 2017, 2018)."
                        )
    parser.add_argument("--output_dir",
                        type=str,
                        help="Directory where the output bstautau.root file will be saved."
                        )
    parser.set_defaults(**_defaults)
    return parser.parse_args()

class HistogramPreparer:
    def __init__(self, folder_name, file_name, output_dir):
        """
        Initialize histogram preparer.
        
        Args:
            folder_name: Name of the folder containing histograms (e.g., "11Aug2025_15h37m07s")
            output_dir: Directory for output file (default matches C++ expectation)
        """
        # Construct path to histograms.root file
        self.input_file  = os.path.join(folder_name, file_name) 
        self.folder_name = os.path.abspath(folder_name)
        self.output_dir  = os.path.expandvars(output_dir)
        if not os.path.exists(self.folder_name):
            raise RuntimeError(f"Input folder not found: {self.folder_name}")
            sys.exit(1)
        print(f"[IN] {self.input_file}")
        print(f"[OUT] {self.output_dir}")

        # Define all channels and their corresponding categories
        # This maps channel -> {category_name: variable_name}
        # All channels use the same mapping of category_name -> variable_name
        base_categories = {
            '{channel}_tauhtaumu': 'btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaumu_frac_general_exclusive',
            '{channel}_tauhtauh': 'btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtauh_frac_general_exclusive',
            '{channel}_tauhtaue': 'btagged_loose_jets_pt_above_20_for_histo_ParTRawTauhtaue_frac_general_exclusive'
        }
        channels = ['e', 'mu', 'ee', 'emu', 'mumu'] #FIXME: Only emu for now, add others later
        print(f"\t ttbar channels : {channels}")
        self.channel_categories = {
            channel: {
                cat.format(channel=channel): var for cat, var in base_categories.items()
            } for channel in channels
        }
        print(f"\t ttbar-channels x categories : {len(channels) * len(base_categories)}")
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        # Open input file
        self.root_file = ROOT.TFile.Open(self.input_file, "READ")
        if not self.root_file or self.root_file.IsZombie():
            raise RuntimeError(f"Cannot open file: {self.input_file}")
    
    def get_histogram(self, channel, variable, sample):
        """Get histogram from ROOT file."""
        hist_path = f"{channel}/{variable}/bstautau_not_scaled/lin/{sample}"
        hist = self.root_file.Get(hist_path)
        
        if not hist:
            print(f"WARNING: Histogram not found: {hist_path}")
            print(f"         Channel: {channel}, Variable: {variable}, Sample: {sample}")
            return None
            
        # Clone to avoid ROOT ownership issues
        hist_clone = hist.Clone(f"{sample}_clone")
        hist_clone.SetDirectory(0)
        

        #scale_factor = 300.0 / 59
        scale_factor = 1.0
        # Data
        if sample == "data_obs":
            hist_clone.Scale(scale_factor)
            print(f"         Scaled {sample} by factor of {scale_factor:.4f}")
        # Signal
        elif sample == "bstautau":
            hist_clone.Scale(scale_factor * 0.1)
            print(f"         Scaled {sample} by factor of {scale_factor * 0.1:.4f}") # correct because the signal is 10x LHCb
        # Backgrounds
        else:
            hist_clone.Scale(scale_factor )
            print(f"         Scaled {sample} by factor of {scale_factor:.4f}")
        return hist_clone
    
    def create_bstautau_root_file(self):
        """
        Create the bstautau.root file with the structure expected by BsTauTau.cpp.
        
        Structure: $BIN/$PROCESS
        - Each category (bin) gets its own directory
        - data -> data_obs
        - bstautau -> bstautau (signal)
        - All other samples keep their names
        """
        output_filename = f"{self.output_dir}/bstautau.root"
        output_file = ROOT.TFile(output_filename, "RECREATE")
        
        # Get all samples
        all_samples = ["data_obs"] + samples.mc_samples_names
        
        total_categories = 0
        total_histograms = 0
        missing_histograms = 0
        
        # Process each channel
        for channel, categories in self.channel_categories.items():
            print(f"\n=== Processing channel: {channel} ===")
            
            for category_name, variable in categories.items():
                print(f"\nProcessing category: {category_name} (variable: {variable})")
                # Create directory for this category (bin)
                bin_dir = output_file.mkdir(category_name)
                bin_dir.cd()
                
                category_histograms = 0
                category_missing = 0
                
                for sample in all_samples:
                    hist = self.get_histogram(channel, variable, sample)
                    if hist:
                        # Determine process name for combine
                        process_name = sample  # Keep original sample name (including bstautau)
                        
                        # Rename and write in the category directory
                        hist.SetName(process_name)
                        hist.SetTitle(process_name)
                        hist.Write()
                        
                        category_histograms += 1
                        total_histograms    += 1
                    else:
                        category_missing    += 1
                        missing_histograms  += 1
                
                print(f"    -> {category_histograms} histograms written, {category_missing} missing in {category_name}")
                total_categories += 1
                
                # Go back to root directory for next category
                output_file.cd()
        
        output_file.Close()
        print(f"\n=== SUMMARY ===")
        print(f"Created: {output_filename}")
        print(f"Total categories: {total_categories}")
        print(f"Total histograms written: {total_histograms}")
        print(f"Total histograms missing: {missing_histograms}")
        if missing_histograms > 0:
            print(f"WARNING: {missing_histograms} histograms were not found in the input file!")
            print("Check the variable names and paths in your ROOT file.")
        print(f"Structure: $BIN/$PROCESS")
        print(f"Ready for BsTauTau.cpp!")
        
        return output_filename
    
    def run(self):
        """
        Run the histogram preparation.
        """
        print("\n=== BsTauTau Histogram Preparer ===")
        
        # Create the bstautau.root file
        output_file = self.create_bstautau_root_file()

        
        # Clean up
        self.root_file.Close()


if __name__ == "__main__":
    
    args = get_arguments()
    folder_name = args.h_path
    
    # Initialize and run histogram preparer
    preparer = HistogramPreparer(
        folder_name, 
        args.h_file, 
        args.output_dir)
    preparer.run()
