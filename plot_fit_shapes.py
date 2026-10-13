#!/usr/bin/env python3
"""
Plot pre-fit/post-fit shapes from a Combine FitDiagnostics output
===================================================================

Reads shapes_prefit/shapes_fit_b/shapes_fit_s from a fitDiagnostics*.root file
(produced with --saveShapes --saveWithUncertainties) and draws, per category,
a stacked-background + signal + data plot with a data/background ratio panel.
"""

import os
import argparse
import ROOT
import utils.samples as samples

ROOT.gROOT.SetBatch(True)

# -- Editable constants ------------------------------------------------------
# ch -> category label, verified against BsTauTau.cpp's bin-id -> name map
# and the datacard's "shapes" lines (bs_tautau_{1,2,3}_13TeV -> ch{1,2,3}).
CHANNEL_LABELS = {
    #"ch1": "emu_tauhtaue", "ch2": "emu_tauhtaumu", "ch3": "emu_tauhtauh",
    "ch1": "emu_tauhtauh_sr", "ch2": "emu_tauhtaumu_sr", "ch3": "emu_tauhtaue_sr",
    "ch4": "emu_tauhtauh_cr", "ch5": "emu_tauhtaumu_cr", "ch6": "emu_tauhtaue_cr",
}
BKG_PROCS = ["tt_fullylep", "tt_semilep", "tt_had"]  # stack order, bottom->top
SIG_PROC = "bstautau"
X_AXIS_TITLE = "max tag fit score"
FIT_LABELS = {
    "prefit": "Pre-fit",
    "fit_b": "Post-fit (b-only)",
    "fit_s": "Post-fit (s+b)",
}


def get_arguments():
    _defaults = {
        "fit_types": ["prefit", "fit_s"],
        "channels": list(CHANNEL_LABELS.keys()),
        "output_dir": "plots",
        "formats": ["pdf", "png"],
        "sig_scale": 1.0,
        "cms_label": "Work in progress",
        "lumi_label": "59.7 fb^{-1} (13 TeV)",
    }
    parser = argparse.ArgumentParser(
        description="Plot pre-fit/post-fit shapes from a Combine FitDiagnostics output.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("fitdiag_file", type=str,
                         help="Path to the fitDiagnostics*.root file.")
    parser.add_argument("--fit-types", nargs="+", choices=list(FIT_LABELS.keys()),
                         help="Which shapes_<type> directories to plot.")
    parser.add_argument("--channels", nargs="+", choices=list(CHANNEL_LABELS.keys()),
                         help="Which bins/categories to plot.")
    parser.add_argument("--output-dir", type=str,
                         help="Directory where plots are saved.")
    parser.add_argument("--formats", nargs="+",
                         help="Output file formats (e.g. pdf png).")
    parser.add_argument("--log-y", action="store_true",
                         help="Draw the upper pad with a log-scale y-axis.")
    parser.add_argument("--sig-scale", type=float,
                         help="Multiply the signal histogram by this factor for visibility only.")
    parser.add_argument("--cms-label", type=str, help="CMS label text.")
    parser.add_argument("--lumi-label", type=str, help="Luminosity label text.")
    parser.set_defaults(**_defaults)
    return parser.parse_args()


# -- Styling helpers ----------------------------------------------------------

def style_bkg_hist(h, proc):
    h.SetFillColor(samples.colours[proc])
    h.SetLineColor(ROOT.kBlack)
    h.SetLineWidth(1)
    h.SetTitle(samples.titles[proc])
    return h


def style_signal_hist(h, sig_scale):
    h.SetFillStyle(0)
    h.SetLineColor(samples.colours[SIG_PROC])
    h.SetLineWidth(3)
    label = samples.titles[SIG_PROC]
    if sig_scale != 1.0:
        label += f" (x{sig_scale:g})"
    h.SetTitle(label)
    return h


def style_data_graph(g):
    g.SetMarkerStyle(ROOT.kFullCircle)
    g.SetMarkerSize(0.9)
    g.SetMarkerColor(ROOT.kBlack)
    g.SetLineColor(ROOT.kBlack)
    g.SetTitle("Data")
    return g


# -- Histogram/graph builders --------------------------------------------------

def build_stack_and_band(shape_dir):
    stack = ROOT.THStack("stack", "")
    bkg_hists = []
    for proc in BKG_PROCS:
        h = shape_dir.Get(proc)
        if not h:
            raise RuntimeError(f"Missing background histogram '{proc}' in {shape_dir.GetPath()}")
        h = h.Clone(f"{proc}_clone")
        h.SetDirectory(0)
        style_bkg_hist(h, proc)
        stack.Add(h)
        bkg_hists.append(h)

    total_bkg = shape_dir.Get("total_background")
    if not total_bkg:
        raise RuntimeError(f"Missing 'total_background' in {shape_dir.GetPath()}")
    total_bkg = total_bkg.Clone("total_background_clone")
    total_bkg.SetDirectory(0)

    return stack, bkg_hists, total_bkg


def hist_to_band(h, scale=1.0):
    """TGraphAsymmErrors tracing h's content +/- bin error, for a shaded band."""
    g = ROOT.TGraphAsymmErrors(h.GetNbinsX())
    for i in range(1, h.GetNbinsX() + 1):
        x = h.GetBinCenter(i)
        hw = h.GetBinWidth(i) / 2.0
        y = h.GetBinContent(i) * scale
        ey = h.GetBinError(i) * scale
        g.SetPoint(i - 1, x, y)
        g.SetPointError(i - 1, hw, hw, ey, ey)
    g.SetFillColor(ROOT.kBlack)
    g.SetFillStyle(3004)
    g.SetLineWidth(0)
    g.SetMarkerSize(0)
    return g


def ratio_band(h):
    """Same shape as hist_to_band but normalized to y=1, for the ratio panel."""
    g = ROOT.TGraphAsymmErrors(h.GetNbinsX())
    for i in range(1, h.GetNbinsX() + 1):
        x = h.GetBinCenter(i)
        hw = h.GetBinWidth(i) / 2.0
        content = h.GetBinContent(i)
        frac_err = h.GetBinError(i) / content if content > 0 else 0.0
        g.SetPoint(i - 1, x, 1.0)
        g.SetPointError(i - 1, hw, hw, frac_err, frac_err)
    g.SetFillColor(ROOT.kBlack)
    g.SetFillStyle(3004)
    g.SetLineWidth(0)
    g.SetMarkerSize(0)
    return g


def data_over_bkg(g_data, h_bkg):
    """Data/background ratio graph, dividing data's asymmetric Poisson errors by bkg content."""
    g = ROOT.TGraphAsymmErrors(g_data.GetN())
    for i in range(g_data.GetN()):
        x = g_data.GetPointX(i)
        bin_idx = h_bkg.FindBin(x)
        bkg = h_bkg.GetBinContent(bin_idx)
        y = g_data.GetPointY(i) / bkg if bkg > 0 else 0.0
        eyl = g_data.GetErrorYlow(i) / bkg if bkg > 0 else 0.0
        eyh = g_data.GetErrorYhigh(i) / bkg if bkg > 0 else 0.0
        g.SetPoint(i, x, y)
        g.SetPointError(i, g_data.GetErrorXlow(i), g_data.GetErrorXhigh(i), eyl, eyh)
    style_data_graph(g)
    return g

def signal_over_bkg(h_sig, h_bkg, sig_scale):
    """Signal/background histogram, dividing signal content by bkg content."""
    h = h_sig.Clone("sig_over_bkg")
    h.SetDirectory(0)
    for i in range(1, h.GetNbinsX() + 1):
        sig = h_sig.GetBinContent(i)/sig_scale
        bkg = h_bkg.GetBinContent(i)
        ratio = (sig+bkg) / bkg if bkg > 0 else 0.0
        h.SetBinContent(i, ratio)
        ## propagate errors: (sig/bkg) * sqrt( (sig_err/sig)^2 + (bkg_err/bkg)^2 )
        #sig_err = h_sig.GetBinError(i)
        #bkg_err = h_bkg.GetBinError(i)
        #rel_err_sq = (sig_err / sig)**2 if sig > 0 else 0.0
        #rel_err_sq += (bkg_err / bkg)**2 if bkg > 0 else 0.0
        ratio_err = 0. #ratio * (rel_err_sq**0.5)
        h.SetBinError(i, ratio_err)
    
    return h


# -- Canvas / drawing -----------------------------------------------------------

def make_canvas_with_pads(name):
    c = ROOT.TCanvas(name, name, 800, 800)
    c.cd()

    pad_top = ROOT.TPad(f"{name}_top", "", 0.0, 0.30, 1.0, 1.0)
    pad_top.SetBottomMargin(0.025)
    pad_top.SetLeftMargin(0.12)
    pad_top.SetRightMargin(0.04)
    pad_top.SetTopMargin(0.08)
    pad_top.Draw()

    pad_bot = ROOT.TPad(f"{name}_bot", "", 0.0, 0.0, 1.0, 0.30)
    pad_bot.SetTopMargin(0.03)
    pad_bot.SetBottomMargin(0.35)
    pad_bot.SetLeftMargin(0.12)
    pad_bot.SetRightMargin(0.04)
    pad_bot.Draw()

    return c, pad_top, pad_bot


def draw_cms_labels(pad, cms_label, lumi_label):
    pad.cd()
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.045)
    latex.DrawLatex(0.12, 0.93, f"#bf{{CMS}} #it{{{cms_label}}}")
    latex.SetTextAlign(31)
    latex.DrawLatex(0.96, 0.93, lumi_label)


def plot_one(f, fit_type, ch, args):
    shape_dir = f.Get(f"shapes_{fit_type}/{ch}")
    if not shape_dir:
        raise RuntimeError(f"Missing directory shapes_{fit_type}/{ch} in {args.fitdiag_file}")

    stack, bkg_hists, total_bkg = build_stack_and_band(shape_dir)

    sig_hist = shape_dir.Get(SIG_PROC)
    if not sig_hist:
        raise RuntimeError(f"Missing signal histogram '{SIG_PROC}' in {shape_dir.GetPath()}")
    sig_hist = sig_hist.Clone(f"{SIG_PROC}_clone")
    sig_hist.SetDirectory(0)
    sig_hist.Scale(args.sig_scale)
    style_signal_hist(sig_hist, args.sig_scale)

    data_graph = shape_dir.Get("data")
    if not data_graph:
        raise RuntimeError(f"Missing 'data' graph in {shape_dir.GetPath()}")
    style_data_graph(data_graph)

    band        = hist_to_band(total_bkg)
    ratio_graph = data_over_bkg(data_graph, total_bkg)
    ratio_sig   = signal_over_bkg(sig_hist, total_bkg, args.sig_scale)
    r_band      = ratio_band(total_bkg)

    cat_label = CHANNEL_LABELS[ch]
    canvas_name = f"c_{cat_label}_{fit_type}"
    c, pad_top, pad_bot = make_canvas_with_pads(canvas_name)

    # -- upper pad --
    pad_top.cd()
    if args.log_y:
        pad_top.SetLogy(True)

    stack.Draw("HIST")
    stack.GetXaxis().SetLabelSize(0)
    stack.GetYaxis().SetTitle("Events")
    stack.GetYaxis().SetTitleSize(0.05)
    stack.GetYaxis().SetTitleOffset(1.1)
    stack.SetMaximum(1.5 * max(stack.GetMaximum(), data_graph.GetHistogram().GetMaximum()))
    if not args.log_y:
        stack.SetMinimum(0.0)

    band.Draw("2 SAME")
    sig_hist.Draw("HIST SAME")
    data_graph.Draw("P SAME")

    legend = ROOT.TLegend(0.60, 0.60, 0.94, 0.90)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.035)
    legend.AddEntry(data_graph, "Data", "pel")
    legend.AddEntry(sig_hist, sig_hist.GetTitle(), "l")
    for h in reversed(bkg_hists):
        legend.AddEntry(h, h.GetTitle(), "f")
    legend.AddEntry(band, "Bkg. unc.", "f")
    legend.Draw()

    draw_cms_labels(pad_top, args.cms_label, args.lumi_label)

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.04)
    latex.DrawLatex(0.15, 0.82, f"{cat_label}, {FIT_LABELS[fit_type]}")

    # -- lower pad: ratio --
    pad_bot.cd()
    ratio_graph.GetXaxis().SetLimits(total_bkg.GetXaxis().GetXmin(), total_bkg.GetXaxis().GetXmax())
    ratio_graph.SetMinimum(0.5)
    ratio_graph.SetMaximum(1.5)
    ratio_graph.GetXaxis().SetTitle(X_AXIS_TITLE)
    ratio_graph.GetYaxis().SetTitle("Data / Bkg.")
    ratio_graph.GetXaxis().SetTitleSize(0.11)
    ratio_graph.GetXaxis().SetLabelSize(0.09)
    ratio_graph.GetYaxis().SetTitleSize(0.11)
    ratio_graph.GetYaxis().SetTitleOffset(0.5)
    ratio_graph.GetYaxis().SetLabelSize(0.09)
    ratio_graph.GetYaxis().SetNdivisions(505)
    ratio_graph.Draw("AP")
    ratio_sig.Draw("HIST SAME")
    ratio_graph.Draw("P")

    r_band.Draw("2 SAME")

    line = ROOT.TLine(total_bkg.GetXaxis().GetXmin(), 1.0, total_bkg.GetXaxis().GetXmax(), 1.0)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw("SAME")

    ratio_graph.Draw("P SAME")

    out_base = os.path.join(args.output_dir, f"{cat_label}_{fit_type}")
    for fmt in args.formats:
        c.SaveAs(f"{out_base}.{fmt}")


def main():
    args = get_arguments()
    args.output_dir = os.path.expandvars(args.output_dir)
    os.makedirs(args.output_dir, exist_ok=True)

    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)

    f = ROOT.TFile.Open(args.fitdiag_file, "READ")
    if not f or f.IsZombie():
        raise RuntimeError(f"Cannot open file: {args.fitdiag_file}")

    for fit_type in args.fit_types:
        for ch in args.channels:
            plot_one(f, fit_type, ch, args)

    f.Close()
    print(f"[OUT-DIRECTORY] {args.output_dir}")


if __name__ == "__main__":
    main()
