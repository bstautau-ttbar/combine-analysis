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
    parser.add_argument("-y", "--year",
                        type=str, choices=samples.luminosity_year.keys(),
                        help="Year of the analysis (e.g., 2016, 2017, 2018)."
                        )
    parser.add_argument("--channels",
                        nargs="+", choices=samples.channels,
                        help="List of channels to process."
                        )
    parser.add_argument("--output_dir",
                        type=str,
                        help="Directory where the output bstautau.root file will be saved."
                        )
    parser.add_argument("--test_samples",
                        action="store_true",
                        help="If set, only process a subset of samples for testing."
                        )
    parser.add_argument("--mc_only",
                        action="store_true",
                        help="If set, only process Monte Carlo samples."
                        )
    parser.set_defaults(**_defaults)
    return parser.parse_args()

class HistogramPreparer:
    def __init__(self, file_path, output_dir, year=2018, channels = samples.channels, **kwargs):
        """
        Initialize histogram preparer.
        
        Args:
            file_path: Path to the .root file containing the binned shapes.
            output_dir: Directory for output file (default matches C++ expectation)
        """
        # Construct path to histograms.root file
        self.input_file  = file_path 
        self.folder_name = os.path.abspath(os.path.dirname(file_path))
        self.output_dir  = os.path.expandvars(output_dir)
        if not os.path.exists(self.folder_name):
            raise RuntimeError(f"Input folder not found: {self.folder_name}")
            sys.exit(1)
        print(f"[IN] {self.input_file}")

        self.year = year
        print(f"[YEAR] {self.year}")
        
        # Define all channels and their corresponding categories
        # This maps channel -> {category_name: variable_name}
        # All channels use the same mapping of category_name -> variable_name
        base_categories = {
            #'{channel}_tauhtaumu'  : 'j_tauhtaumu_incl',
            #'{channel}_tauhtaue'   : 'j_tauhtaue_incl',
            #'{channel}_tauhtauh'   : 'j_tauhtauh_incl',
            '{channel}_tauhtaumu_sr'   : 'j_tauhtaumu_SR',
            '{channel}_tauhtaumu_cr'   : 'j_tauhtaumu_CR',
            '{channel}_tauhtauh_sr'    : 'j_tauhtauh_SR',
            '{channel}_tauhtauh_cr'    : 'j_tauhtauh_CR',
            '{channel}_tauhtaue_sr'    : 'j_tauhtaue_SR',
            '{channel}_tauhtaue_cr'    : 'j_tauhtaue_CR',
        }
        
        print(f"\t ttbar channels : {channels}")
        self.channel_categories = {
            channel: {
                cat.format(channel=channel): var for cat, var in base_categories.items()
            } for channel in channels
        }
        print(f"\t ttbar-channels x categories : {len(channels) * len(base_categories)}")
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"[OUT-DIRECTORY] {self.output_dir}")
        # Open input file
        self.root_file = ROOT.TFile.Open(self.input_file, "READ")
        if not self.root_file or self.root_file.IsZombie():
            raise RuntimeError(f"Cannot open file: {self.input_file}")
        
        # additional keyword arguments
        self.kwsettings = {
            "only_test_samples": kwargs.get("only_test_samples", False),
            "mc_only": kwargs.get("mc_only", False)
        }


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
            print(f"         Scaled {sample} by factor of {scale_factor:.2f}")
        # Signal
        elif sample == "bstautau":
            hist_clone.Scale(scale_factor * 0.1)
            print(f"         Scaled {sample} by factor of {scale_factor * 0.1:.2f}") # correct because the signal is 10x LHCb
        # Backgrounds
        else:
            hist_clone.Scale(scale_factor)
            print(f"         Scaled {sample} by factor of {scale_factor:.2f}")
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
        
        output_filename = f"{self.output_dir}/bstautau_{self.year}.root"
        output_file = ROOT.TFile(output_filename, "RECREATE")
        print(f"[OUT-FILE] {output_filename}")
        
        # Get all samples
        all_samples = []
        if self.kwsettings["mc_only"] and self.kwsettings["only_test_samples"]:
            all_samples = ["bstautau", "tt_fullylep", "tt_semilep", "tt_had"]
            print(f"[WARNING] mc_only & only_test_samples -- processing {all_samples}")
        elif self.kwsettings["mc_only"]:
            all_samples = samples.mc_samples_names
            print(f"[WARNING] mc_only -- processing {all_samples}")
        else:
            all_samples = ["data_obs"] + samples.mc_samples_names
            print(f"[INFO] processing {all_samples}")
        if not all_samples:
            raise RuntimeError("No samples to process. Check your settings.")
        
        
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

                # if MC-only generate a data_obs from the bkg-only sum of histograms
                if self.kwsettings["mc_only"]:
                    print(f"Generating data_obs histogram for category: {category_name} (MC-only mode)")
                    data_obs_hist = None
                    for sample in all_samples:
                        if 'bstautau' in sample: continue # skip signal
                        hist = self.get_histogram(channel, variable, sample)
                        if not hist:
                            print(f"WARNING: Missing histogram for sample {sample} in category {category_name}. Cannot generate data_obs.")
                            continue
                        if data_obs_hist is None:
                            data_obs_hist = hist.Clone("data_obs")
                            data_obs_hist.SetDirectory(0)
                        else:
                            data_obs_hist.Add(hist)
                    if data_obs_hist:
                        # poisson fluctuations
                        for bin_idx in range(1, data_obs_hist.GetNbinsX() + 1):
                            content = data_obs_hist.GetBinContent(bin_idx)
                            # Use PoissonD for double precision
                            fluctuated_content = ROOT.gRandom.Poisson(content) # N.B. This routine since is returning 32 bits integer will not work for values larger than 2*10**9 -> use ROOT.gRandom.PoissonD(content) for double precision
                            data_obs_hist.SetBinContent(bin_idx, fluctuated_content)
                        data_obs_hist.Write()
                        category_histograms += 1
                        total_histograms    += 1
                    else:
                        print(f"WARNING: Could not generate data_obs histogram for category {category_name}.")
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
    
    # Initialize and run histogram preparer
    preparer = HistogramPreparer(
        args.h_path, 
        args.output_dir,
        args.year,
        args.channels if args.channels else samples.channels,
        only_test_samples=args.test_samples,
        mc_only=args.mc_only
        )
    preparer.run()
