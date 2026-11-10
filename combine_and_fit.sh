#!/bin/bash

echo ""
echo "=== e CHANNEL ==="
combineCards.py datacards/bs_tautau_19_13TeV_.txt datacards/bs_tautau_20_13TeV_.txt datacards/bs_tautau_21_13TeV_.txt datacards/bs_tautau_22_13TeV_.txt datacards/bs_tautau_23_13TeV_.txt datacards/bs_tautau_24_13TeV_.txt > datacards/dacarard_bs_tautau_e_2018.txt
echo "✓ combined datacard created: datacards/dacarard_bs_tautau_e_2018.txt"
echo ""
text2workspace.py datacards/dacarard_bs_tautau_e_2018.txt
echo "✓ Workspace created: datacards/dacarard_bs_tautau_e_2018.root"
echo ""
combine -M AsymptoticLimits datacards/dacarard_bs_tautau_e_2018.root -n .bstautau_e.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== mu CHANNEL ==="
combineCards.py datacards/bs_tautau_25_13TeV_.txt datacards/bs_tautau_26_13TeV_.txt datacards/bs_tautau_27_13TeV_.txt datacards/bs_tautau_28_13TeV_.txt datacards/bs_tautau_29_13TeV_.txt datacards/bs_tautau_30_13TeV_.txt > datacards/dacarard_bs_tautau_mu_2018.txt
echo "✓ combined datacard created: datacards/dacarard_bs_tautau_mu_2018.txt"
echo ""
text2workspace.py datacards/dacarard_bs_tautau_mu_2018.txt
echo "✓ Workspace created: datacards/dacarard_bs_tautau_mu_2018.root"
echo ""
combine -M AsymptoticLimits datacards/dacarard_bs_tautau_mu_2018.root -n .bstautau_mu.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== ee CHANNEL ==="
combineCards.py datacards/bs_tautau_13_13TeV_.txt datacards/bs_tautau_14_13TeV_.txt datacards/bs_tautau_15_13TeV_.txt datacards/bs_tautau_16_13TeV_.txt datacards/bs_tautau_17_13TeV_.txt datacards/bs_tautau_18_13TeV_.txt > datacards/dacarard_bs_tautau_ee_2018.txt
echo "✓ combined datacard created: datacards/dacarard_bs_tautau_ee_2018.txt"
echo ""
text2workspace.py datacards/dacarard_bs_tautau_ee_2018.txt
echo "✓ Workspace created: datacards/dacarard_bs_tautau_ee_2018.root"
echo ""
combine -M AsymptoticLimits datacards/dacarard_bs_tautau_ee_2018.root -n .bstautau_ee.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== emu CHANNEL ==="
combineCards.py datacards/bs_tautau_1_13TeV_.txt datacards/bs_tautau_2_13TeV_.txt datacards/bs_tautau_3_13TeV_.txt datacards/bs_tautau_4_13TeV_.txt datacards/bs_tautau_5_13TeV_.txt datacards/bs_tautau_6_13TeV_.txt > datacards/dacarard_bs_tautau_emu_2018.txt
echo "✓ combined datacard created: datacards/dacarard_bs_tautau_emu_2018.txt"
echo ""
text2workspace.py datacards/dacarard_bs_tautau_emu_2018.txt
echo "✓ Workspace created: datacards/dacarard_bs_tautau_emu_2018.root"
echo ""
combine -M AsymptoticLimits datacards/dacarard_bs_tautau_emu_2018.root -n .bstautau_emu.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo ""
echo "=== mumu CHANNEL ==="
combineCards.py datacards/bs_tautau_7_13TeV_.txt datacards/bs_tautau_8_13TeV_.txt datacards/bs_tautau_9_13TeV_.txt datacards/bs_tautau_10_13TeV_.txt datacards/bs_tautau_11_13TeV_.txt datacards/bs_tautau_12_13TeV_.txt > datacards/dacarard_bs_tautau_mumu_2018.txt
echo "✓ combined datacard created: datacards/dacarard_bs_tautau_mumu_2018.txt"
echo ""
text2workspace.py datacards/dacarard_bs_tautau_mumu_2018.txt
echo "✓ Workspace created: datacards/dacarard_bs_tautau_mumu_2018.root"
echo ""
combine -M AsymptoticLimits datacards/dacarard_bs_tautau_mumu_2018.root -n .bstautau_mumu.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

echo "=== ALL CHANNELS ==="
combineCards.py datacards/*_13TeV_.txt > datacards/dacarard_bs_tautau_allch_2018.txt
echo "✓ combined datacard created: datacards/dacarard_bs_tautau_allch_2018.txt"
echo ""
text2workspace.py datacards/dacarard_bs_tautau_allch_2018.txt
echo "✓ Workspace created: datacards/dacarard_bs_tautau_allch_2018.root"
echo ""
combine -M AsymptoticLimits datacards/dacarard_bs_tautau_allch_2018.root -n .bstautau_allch.2018 -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

