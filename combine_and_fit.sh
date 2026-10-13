#!/bin/bash

#python3 prepare_histograms.py --h_path input_histogram/23Jul2026_combine-ref/ -y 2018
#BsTauTau

echo "=== ALL CHANNELS ==="
combineCards.py datacard/*.txt > datacard/dacarard_bs_tautau_allch_2018.txt
echo "✓ combined datacard created: datacard/dacarard_bs_tautau_allch_2018.txt"
echo ""
text2workspace.py datacard/dacarard_bs_tautau_allch_2018.txt
echo "✓ Workspace created: datacard/dacarard_bs_tautau_allch_2018.root"
echo ""
combine -M AsymptoticLimits datacard/dacarard_bs_tautau_allch_2018.root -n .bstautau_allch.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== e CHANNEL ==="
combineCards.py datacard/bs_tautau_1_13TeV_.txt datacard/bs_tautau_2_13TeV_.txt datacard/bs_tautau_3_13TeV_.txt > datacard/dacarard_bs_tautau_e_2018.txt
echo "✓ combined datacard created: datacard/dacarard_bs_tautau_e_2018.txt"
echo ""
text2workspace.py datacard/dacarard_bs_tautau_e_2018.txt
echo "✓ Workspace created: datacard/dacarard_bs_tautau_e_2018.root"
echo ""
combine -M AsymptoticLimits datacard/dacarard_bs_tautau_e_2018.root -n .bstautau_e.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== mu CHANNEL ==="
combineCards.py datacard/bs_tautau_4_13TeV_.txt datacard/bs_tautau_5_13TeV_.txt datacard/bs_tautau_6_13TeV_.txt > datacard/dacarard_bs_tautau_mu_2018.txt
echo "✓ combined datacard created: datacard/dacarard_bs_tautau_mu_2018.txt"
echo ""
text2workspace.py datacard/dacarard_bs_tautau_mu_2018.txt
echo "✓ Workspace created: datacard/dacarard_bs_tautau_mu_2018.root"
echo ""
combine -M AsymptoticLimits datacard/dacarard_bs_tautau_mu_2018.root -n .bstautau_mu.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== ee CHANNEL ==="
combineCards.py datacard/bs_tautau_7_13TeV_.txt datacard/bs_tautau_8_13TeV_.txt datacard/bs_tautau_9_13TeV_.txt > datacard/dacarard_bs_tautau_ee_2018.txt
echo "✓ combined datacard created: datacard/dacarard_bs_tautau_ee_2018.txt"
echo ""
text2workspace.py datacard/dacarard_bs_tautau_ee_2018.txt
echo "✓ Workspace created: datacard/dacarard_bs_tautau_ee_2018.root"
echo ""
combine -M AsymptoticLimits datacard/dacarard_bs_tautau_ee_2018.root -n .bstautau_ee.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== emu CHANNEL ==="
combineCards.py datacard/bs_tautau_10_13TeV_.txt datacard/bs_tautau_11_13TeV_.txt datacard/bs_tautau_12_13TeV_.txt > datacard/dacarard_bs_tautau_emu_2018.txt
echo "✓ combined datacard created: datacard/dacarard_bs_tautau_emu_2018.txt"
echo ""
text2workspace.py datacard/dacarard_bs_tautau_emu_2018.txt
echo "✓ Workspace created: datacard/dacarard_bs_tautau_emu_2018.root"
echo ""
combine -M AsymptoticLimits datacard/dacarard_bs_tautau_emu_2018.root -n .bstautau_emu.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"   

echo ""
echo "=== mumu CHANNEL ==="
combineCards.py datacard/bs_tautau_13_13TeV_.txt datacard/bs_tautau_14_13TeV_.txt datacard/bs_tautau_15_13TeV_.txt > datacard/dacarard_bs_tautau_mumu_2018.txt
echo "✓ combined datacard created: datacard/dacarard_bs_tautau_mumu_2018.txt"
echo ""
text2workspace.py datacard/dacarard_bs_tautau_mumu_2018.txt
echo "✓ Workspace created: datacard/dacarard_bs_tautau_mumu_2018.root"
echo ""
combine -M AsymptoticLimits datacard/dacarard_bs_tautau_mumu_2018.root -n .bstautau_mumu.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

#combine -M AsymptoticLimits workspace.root -t -1 --freezeParameters all --setParameters lumiscale=400.0/59.7
for cat in {1..15};
do
    echo ""
    echo "=== Running asymptotic limits for category $cat (blind) ==="
    text2workspace.py datacard/bs_tautau_${cat}_13TeV_.txt
    combine -M AsymptoticLimits datacard/bs_tautau_${cat}_13TeV_.root -t -1 --expectSignal=0 -n cat${cat}
    echo "✓ Asymptotic limits for category $cat completed"
done