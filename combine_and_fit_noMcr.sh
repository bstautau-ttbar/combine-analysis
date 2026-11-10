#!/bin/bash
echo "=== ALL CHANNELS ==="
combineCards.py datacards/*_13TeV_.txt > datacards/dacarard_bs_tautau_allch_2018.txt
echo "✓ combined datacard created: datacards/dacarard_bs_tautau_allch_2018.txt"
echo ""
text2workspace.py datacards/dacarard_bs_tautau_allch_2018.txt
echo "✓ Workspace created: datacards/dacarard_bs_tautau_allch_2018.root"
echo ""
combine -M AsymptoticLimits datacards/dacarard_bs_tautau_allch_2018.root -n .bstautau_allch.noMcr.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== mu CHANNEL ==="
combineCards.py datacards/bs_tautau_1_13TeV_.txt datacards/bs_tautau_2_13TeV_.txt datacards/bs_tautau_3_13TeV_.txt > datacards/dacarard_bs_tautau_mu_2018.txt
echo "✓ combined datacard created: datacards/dacarard_bs_tautau_mu_2018.txt"
echo ""
text2workspace.py datacards/dacarard_bs_tautau_mu_2018.txt
echo "✓ Workspace created: datacards/dacarard_bs_tautau_mu_2018.root"
echo ""
combine -M AsymptoticLimits datacards/dacarard_bs_tautau_mu_2018.root -n .bstautau_mu.noMcr.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== e CHANNEL ==="
combineCards.py datacards/bs_tautau_4_13TeV_.txt datacards/bs_tautau_5_13TeV_.txt datacards/bs_tautau_6_13TeV_.txt > datacards/dacarard_bs_tautau_e_2018.txt
echo "✓ combined datacard created: datacards/dacarard_bs_tautau_e_2018.txt"
echo ""
text2workspace.py datacards/dacarard_bs_tautau_e_2018.txt
echo "✓ Workspace created: datacards/dacarard_bs_tautau_e_2018.root"
echo ""
combine -M AsymptoticLimits datacards/dacarard_bs_tautau_e_2018.root -n .bstautau_e.noMcr.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== ee CHANNEL ==="
combineCards.py datacards/bs_tautau_7_13TeV_.txt datacards/bs_tautau_8_13TeV_.txt datacards/bs_tautau_9_13TeV_.txt > datacards/dacarard_bs_tautau_ee_2018.txt
echo "✓ combined datacard created: datacards/dacarard_bs_tautau_ee_2018.txt"
echo ""
text2workspace.py datacards/dacarard_bs_tautau_ee_2018.txt
echo "✓ Workspace created: datacards/dacarard_bs_tautau_ee_2018.root"
echo ""
combine -M AsymptoticLimits datacards/dacarard_bs_tautau_ee_2018.root -n .bstautau_ee.noMcr.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== emu CHANNEL ==="
combineCards.py datacards/bs_tautau_10_13TeV_.txt datacards/bs_tautau_11_13TeV_.txt datacards/bs_tautau_12_13TeV_.txt > datacards/dacarard_bs_tautau_emu_2018.txt
echo "✓ combined datacard created: datacards/dacarard_bs_tautau_emu_2018.txt"
echo ""
text2workspace.py datacards/dacarard_bs_tautau_emu_2018.txt
echo "✓ Workspace created: datacards/dacarard_bs_tautau_emu_2018.root"
echo ""
combine -M AsymptoticLimits datacards/dacarard_bs_tautau_emu_2018.root -n .bstautau_emu.noMcr.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== mumu CHANNEL ==="
combineCards.py datacards/bs_tautau_13_13TeV_.txt datacards/bs_tautau_14_13TeV_.txt datacards/bs_tautau_15_13TeV_.txt > datacards/dacarard_bs_tautau_mumu_2018.txt
echo "✓ combined datacard created: datacards/dacarard_bs_tautau_mumu_2018.txt"
echo ""
text2workspace.py datacards/dacarard_bs_tautau_mumu_2018.txt
echo "✓ Workspace created: datacards/dacarard_bs_tautau_mumu_2018.root"
echo ""
combine -M AsymptoticLimits datacards/dacarard_bs_tautau_mumu_2018.root -n .bstautau_mumu.noMcr.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

